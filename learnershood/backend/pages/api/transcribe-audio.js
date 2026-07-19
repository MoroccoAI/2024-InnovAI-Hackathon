import { createReadStream } from "fs";
import { azureOpenaiWhisper } from "@/lib/openai";
import Cors from "cors";
import multer from "multer";
import initMiddleware from "@/lib/init-middleware";
import { unlinkSync } from "fs";

import ffmpeg from 'fluent-ffmpeg';

const cors = initMiddleware(
  Cors({
    methods: ["POST", "OPTIONS"],
    origin: "*",
  })
);

// Multer setup for file uploads
const upload = multer({ dest: "/tmp/" });
const multerMiddleware = initMiddleware(upload.single("file"));

export const config = {
  api: {
    bodyParser: false, // Disables Next.js body parsing so multer can handle it
  },
};

function convertToWav(inputPath, outputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg(inputPath)
      .output(outputPath)
      .audioCodec('pcm_s16le') // Standard codec for WAV
      .audioChannels(1)       // Mono
      .audioFrequency(16000)  // 16 kHz sample rate
      .on('end', resolve)
      .on('error', reject)
      .run();
  });
}

export default async function handler(req, res) {
  await cors(req, res);

  if (req.method !== "POST") {
    res.status(405).setHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  try {
    await multerMiddleware(req, res); // Handle the file upload

    const audioFilePath = req.file.path; // Access the uploaded file's path

    const convertedPath = `/tmp/${req.file.filename}.wav`;

    await convertToWav(req.file.path, convertedPath);
    const result = await azureOpenaiWhisper.audio.transcriptions.create({
      model: "",
      file: createReadStream(convertedPath),
    });
    
    unlinkSync(convertedPath);

    return res.status(200).json({
      status: true,
      data: result.text,
    });
  } catch (error) {
    console.error("Error occurred:", error);

    // Clean up the temporary file if an error occurred
    if (req.file && req.file.path) {
      unlinkSync(req.file.path);
    }

    res.status(400).json({
      status: false,
      error: "Error occurred! Please try again.",
    });
  }
}
