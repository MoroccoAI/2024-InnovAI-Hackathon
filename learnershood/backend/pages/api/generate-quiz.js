import { openai } from "@/lib/openai";
import Cors from 'cors';
import initMiddleware from '@/lib/init-middleware';

const cors = initMiddleware(
  Cors({
    methods: ['GET', 'POST', 'OPTIONS'], 
    origin: "*", 
  })
);

export const config = {
  maxDuration: 180,
};

const generateQuiz = async (req, res) => {
  await cors(req, res);
  
  if (req.method !== "POST") {
    res.status(405).appendHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  const { transcript, title }  = req.body;

  try {
    const systemPrompt = 
      `You are a learning assistant that helps student set practice questions to prepare exam.`;

    const prompt = `
      I just finished listening to a story about "${title}" and I want to test myself for want I have listen to. 
      <TRANSCRIPT>
        ${transcript}
      </TRANSCRIPT>
      Using the information in the TRANSCRIPT above to help me generate 20 quizzies tailored to story title: "${title}".  

      
      You answer must strictly follow this JSON format like this:
      {
        quiz: [{
          id: 0,
          question: "",
          options: ["Option 1", "Option 2", "Option 3", "Option 4"],
          correctAnswer: 0
        }]
      }
    `;

    const messages = [
      { role: "system", content: systemPrompt },
      { role: "user", content: prompt },
    ];
    
    const response = await openai.chat.completions.create({
      model: process.env.AZURE_OPENAI_DEPLOYMENT_MODEL,
      messages,
      temperature: 1,
      max_tokens: 4000,
      stream: false,
      response_format: { type: "json_object" },
    });

    const generatedResponse = response.choices.pop();
    const content = generatedResponse.message.content;
    const parsedContent = JSON.parse(content);

    return res.status(200).json({
      status: true,
      data: parsedContent.quiz,
    });
  } catch (error) {
    console.log({ error })
    res
      .status(500)
      .json({ 
        status: false, 
        error: "Error occurred! Please try again." 
      });
  }
};

export default generateQuiz;

