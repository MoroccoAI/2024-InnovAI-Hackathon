import { uploadFile } from '../../lib/upload-to-aws';
import * as AzureSpeechSdk from "microsoft-cognitiveservices-speech-sdk";
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

export default async function handler(req, res) {
  await cors(req, res);
  
  if (req.method !== "POST") {
    res.status(405).appendHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  const { transcript } = req.body;

  var audioFile = "story.mp3";
  const speechKey = process.env.AZURE_SPEECH_KEY;
  const speechRegion = process.env.AZURE_SPEECH_REGION;

  const speechConfig = AzureSpeechSdk.SpeechConfig.fromSubscription(
    speechKey,
    speechRegion
  );

  const audioConfig = AzureSpeechSdk.AudioConfig.fromAudioFileOutput(audioFile);

  speechConfig.speechSynthesisVoiceName = "en-NG-EzinneNeural";

  var synthesizer = new AzureSpeechSdk.SpeechSynthesizer(speechConfig, audioConfig);

  const generateAudio = async () => {
    return new Promise((resolve, reject) => {
      synthesizer.speakTextAsync(
        transcript,
        async function (result) {
          try {
            if (result.reason === AzureSpeechSdk.ResultReason.SynthesizingAudioCompleted) {
              const fileUploaded = await uploadFile(audioFile, result.audioData);
  
              resolve(fileUploaded); 
            } else {
              reject( result.errorDetails ); 
            }
          } catch (err) {
            reject(err);
          } finally {
            synthesizer.close();
            synthesizer = null;
          }
        },
        function (err) {
          synthesizer.close();
          synthesizer = null;
          reject(err); 
        }
      );
    });
  };
  
  try {
    const generatedAudio = await generateAudio();

    res.status(200).json({
      success: true,
      data: generatedAudio
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error,
    });
  }
}
