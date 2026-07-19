import { createReadStream } from "fs";
import { azureOpenaiWhisper } from "@/lib/openai";
import Cors from 'cors';
import initMiddleware from '@/lib/init-middleware';

const cors = initMiddleware(
  Cors({
    methods: ['GET', 'POST', 'OPTIONS'], 
    origin: "*", 
  })
);

export default async function handler(req, res) {
  await cors(req, res);
  
  if (req.method !== "POST") {
    res.status(405).appendHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  try {
    const audioFilePath = "./public/record.m4a";
    
    const result = await azureOpenaiWhisper.audio.transcriptions.create({
      model: "",
      file: createReadStream(audioFilePath),
    });

    return res.status(200).json({
      status: true,
      data: result.text,
    });
  } catch (error) {
    console.log({ error })
    res
      .status(400)
      .json({ 
        status: false, 
        error: "Error occurred! Please try again." 
      });
  }
}