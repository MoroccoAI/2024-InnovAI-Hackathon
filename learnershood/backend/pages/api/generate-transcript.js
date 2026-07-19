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

const generateTranscript = async (req, res) => {
  await cors(req, res);
  
  if (req.method !== "POST") {
    res.status(405).appendHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  const { topic }  = req.body;

  try {
    const systemPrompt = 
      `You are a storyteller that skilled at tell stroy to the kid in a fun and engaging way. Your task is to create a lively and authentic transcript for the story.`;

    const prompt = `
      Topic: "${topic}"

      Write a detailed transcript for the story about the topic. The transcript should be mainly focus on the story and use the information below to guide it.

      Let the narrator's voice bring the story to life, reflecting the wisdom, and moral lessons of the tale. 

      Structure it to be suitable for young listeners, with a mix of humor, suspense, and engaging questions to keep children attentive.

      Your listeners are Africans looking to learn about African hero and story.

      You answer must strictly follow this JSON format like this:
      {
        title: "Title of the story"
        transcript: "The transcript should be inform of 4 long paragraphs."
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

    console.log({title: parsedContent.title})
    console.log(parsedContent.transcript)


    return res.status(200).json({
      status: true,
      data: parsedContent,
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

export default generateTranscript;

