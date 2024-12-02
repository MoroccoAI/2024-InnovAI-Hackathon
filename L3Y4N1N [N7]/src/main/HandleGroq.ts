import { ipcMain } from "electron";
import Groq from "groq-sdk";
import dotenv from "dotenv";
import getAudioStream from "./getAudioStream";

dotenv.config();

interface TranscriptionResponse {
  text: string
}

async function getTranscriptionGenerator(videoId: string, env: NodeJS.ProcessEnv , start:number): Promise<TranscriptionResponse> {

  const audioFile = await getAudioStream(videoId,start);
  const groq = new Groq({ apiKey: env.FACT_API });
  if (!audioFile) {
    throw new Error("Audio file not found");
  }  
  try {
    const translation = await groq.audio.transcriptions.create({
      file: audioFile,
      model: "whisper-large-v3",
      response_format: "verbose_json",
    });
    return translation;
  } catch (error) {
    throw error;
  }
}

ipcMain.handle("get-transcription", async (_, videoId: string,start :number) => {
  try {
    const transcription = await getTranscriptionGenerator(videoId, process.env,start );
    return transcription;
  } catch (error) {
    throw error;
  }
});

async function getSynonymsAndAntonyms(word: string, env: NodeJS.ProcessEnv): Promise<JSON> {
  const groq = new Groq({ apiKey: env.FACT_API });
  const prompt = `You are a language expert. Provide synonyms, antonyms, and definition for the word "${word}" in the following JSON format:
  {
    "word": "${word}",
    "definition": "the meaning of the word",
    "synonyms": ["synonym1", "synonym2", ...],
    "antonyms": ["antonym1", "antonym2", ...],
    "usage": "Provide a sentence using the word ${word}."
  }`;

  try {
    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: prompt
        },
        {
          role: 'user',
          content: word
        }
      ],
      model: 'llama3-8b-8192',
      response_format: { type: 'json_object' }
    });

    const content = chatCompletion.choices[0]?.message?.content;
    return content ? JSON.parse(content) : null;
  } catch (error) {
    console.error('Error fetching chat completion:', error);
    return {} as JSON;
  }
}

ipcMain.handle("get-synonyms-antonyms", async (_, word: string) => {
  try {
    const result = await getSynonymsAndAntonyms(word, process.env as NodeJS.ProcessEnv);
    return result;
  } catch (error) {
    throw error;
  }
});

export { getTranscriptionGenerator, getSynonymsAndAntonyms };