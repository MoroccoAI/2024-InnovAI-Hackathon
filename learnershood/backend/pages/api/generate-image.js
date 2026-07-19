import { openai } from "@/lib/openai";
import Together from "together-ai";
import { uploadMultipleFiles } from '../../lib/upload-to-aws';
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

const together = new Together({ apiKey: process.env.TOGETHER_AI_KEY });

const generateTranscript = async (req, res) => {
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
      `You are an image prompt generator that extract prompt from a story transcript to generate an illustration of the story`;

    const prompt = `
      Story Title: ${title}
      <TRANSCRIPT>
        ${transcript}
      </TRANSCRIPT>

      The transcript is a naration of the story to the kid but the story should not include those naration. 

      It should focus on the story "${title}" and remove other narative element that is not part of the core story 

      Help me write a prompt to generate an image to illustrate this story: "${title}". 

      The transcript of the story should be divided into six part and write a prompt for each part of the transcript.

      Each prompt should be different from each other since the image will be generate separately. 
      
      Therefore, each prompt should be detailed to capture the whole story.

      The prompt should explain each scene and it should be successive.

      Each prompt should include photo realistic image of the background of the story and should reflect that in the image.

      You answer must strictly follow this JSON format like this:
      {
        prompts: ["6 detailed prompts to illustrate the story."]
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
    const generatedPrompt = JSON.parse(content);

    console.log(generatedPrompt.prompts)

    // black-forest-labs/FLUX.1-schnell
    // black-forest-labs/FLUX.1-schnell-Free

    async function generateImage(imagePrompt) {
      const modPrompt = `
        Story title: "${title}"
        Visualize the scene based on the story title and use it to generate the image below:
        ${imagePrompt}
      `
      try {
        const response = await together.images.create({
          model: "black-forest-labs/FLUX.1-schnell",
          prompt: modPrompt,
          width: 768,
          height: 1024,
          steps: 12,
          n: 1,
          response_format: "b64_json",
          update_at: "2024-11-28T09:26:56.035Z"
        });
        return response.data[0].b64_json;
      } catch (error) {
        console.error(`Error generating image for prompt: ${imagePrompt}`, error);
        throw error;
      }
    }

    async function generateMultipleImages(prompts) {
      try {
        const generationPromises = prompts.map((prompt) => generateImage(prompt));
        return await Promise.all(generationPromises);
      } catch (error) {
        console.error("Error generating multiple images:", error);
        throw error;
      }
    }

    const images = await generateMultipleImages(generatedPrompt.prompts);

    const filesUploaded = await uploadMultipleFiles(images)
  

    return res.status(200).json({
      status: true,
      data: filesUploaded,
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

