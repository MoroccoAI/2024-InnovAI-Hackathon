import OpenAI from "openai";
import { createAzure } from '@ai-sdk/azure';
import { AzureOpenAI } from "openai";

const resource = process.env.AZURE_OPENAI_RESOURCE_NAME;
const model = process.env.AZURE_OPENAI_DEPLOYMENT_MODEL; 
const apiVersion = process.env.AZURE_OPENAI_API_VERSION;
const apiKey = process.env.AZURE_OPENAI_API_KEY;

const whisperResource = process.env.AZURE_OPENAI_WHISPER_RESOURCE_NAME;
const whisperModel = process.env.AZURE_OPENAI_WHISPER_DEPLOYMENT_MODEL; 
const whisperApiVersion = process.env.AZURE_OPENAI_WHISPER_API_VERSION;
const whisperApiKey = process.env.AZURE_OPENAI_WHISPER_API_KEY;
const whisperEndpoint = `https://${whisperResource}.cognitiveservices.azure.com/openai/deployments/${whisperModel}/audio/translations?api-version=${whisperApiVersion}`;

export const openai = new OpenAI({
  apiKey,
  baseURL: `https://${resource}.openai.azure.com/openai/deployments/${model}`,
  defaultQuery: { 'api-version': apiVersion },
  defaultHeaders: { 'api-key': apiKey },
});

export const azureOpenai = createAzure({
  resourceName: resource,
  apiKey: apiKey,
});

function getAzureOpenAIWhisperClient() {
  return new AzureOpenAI({
    endpoint: whisperEndpoint,
    apiKey: whisperApiKey,
    apiVersion: whisperApiVersion,
    deployment: whisperModel,
  });
}

export const azureOpenaiWhisper = getAzureOpenAIWhisperClient()