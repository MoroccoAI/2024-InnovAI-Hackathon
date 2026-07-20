import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import librosa
import requests

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
SAMPLE_RATE = 16000
gemini_api_key = 'GEMINI_API_KEY'

model_id = "distil-whisper/distil-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device,
)

def load_multichannel_audio(audio_file, channel):
  # we suppose tha the audio is multichannel the agent is in separated channel to the client
  waveform,sample_rate = librosa.load(audio_file, mono=False)
  if sample_rate != 16000:
    waveform = librosa.resample(waveform, sample_rate, 16000)
  return waveform[channel], sample_rate

def get_transcript(audio_file, channel):
  # transcribe the audio
  waveform,sample_rate = load_multichannel_audio(audio_file, channel)
  result = pipe(waveform, return_timestamps=True, batch_size=4)
  return result['text']
  return



def sort_discussion(audio_file):
  # get transcript per channel
  _, client_transcript = get_transcript(audio_file, 0)
  for chunk in client_transcript:
    chunk['channel'] = 'Client'
  _, agent_transcript = get_transcript(audio_file, 1)
  for chunk in agent_transcript:
    chunk['channel'] = 'Agent'

  #Combine the transcript and sort them
  combined_transcript = client_transcript + agent_transcript
  combined_transcript.sort(key=lambda x: x['timestamp'])
  transcript = []
  # recuperate the transcript in the ordre
  for chunk in combined_transcript:
    if chunk['channel'] == 'Client':
      transcript.append(f'Client: {chunk["text"]}')
    else:
      transcript.append(f'Agent: {chunk["text"]}')
    transcript.append(f'Agent: {chunk["text"]}')
  return '\n'.join(transcript)



def get_summary(transcript):
  #Import the prompt
  with open('prompt_summary.txt', 'r', encoding='utf-f') as prompt_file:
    summary_prompt = prompt_file.read()
  prompt = summary_prompt + f' voici la discussion : {transcript}'
  headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json",
    }
  data = {
        "model": "gemini-pro",
        "prompt": prompt,
        "temperature": 0.05,  # deterministic answers
        "max_tokens": 256  #
    }
  # Call the API
  response = requests.post("https://api.google.com/v1/chat/completions", headers=headers, json=data)

  if response.status_code == 200:
        return response.json()["choices"][0]["text"]

def get_sentiment_and_tags(transcript):
  #Import the prompt
  with open('prompt_semtiment_tags.txt', 'r', encoding='utf-f') as prompt_file:
    sentiment_prompt = prompt_file.read()
  prompt = sentiment_prompt + f' voici la discussion : {transcript}'
  headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json",
    }
  data = {
        "model": "gemini-pro",
        "prompt": prompt,
        "temperature": 0.05,  # deterministic answers
        "max_tokens": 256  #
    }
  # Call the API
  response = requests.post("https://api.google.com/v1/chat/completions", headers=headers, json=data)

  if response.status_code == 200:
        return response.json()["choices"][0]["text"]
  return

