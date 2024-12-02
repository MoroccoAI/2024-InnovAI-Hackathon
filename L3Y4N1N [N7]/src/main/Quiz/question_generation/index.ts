import Groq from 'groq-sdk'
import dotenv from 'dotenv'
import { readFileSync } from 'fs'
import { Quiz, Transcript } from '../../../types/types'
import prompt from '@resources/prompts/quizGenerationPrompt.md?asset'

dotenv.config()

const QUIZ_GEN_API = process.env.QUIZ_GEN_API

if (!QUIZ_GEN_API) {
  throw new Error('Missing API key. Ensure QUIZ_GEN_API is set in the environment.')
}

const groq = new Groq({ apiKey: QUIZ_GEN_API })

export default async function getQuiz(transcript: Transcript): Promise<Quiz> {
  const systemMessage = readFileSync(prompt, 'utf8') + `\n\nTranscript: ${transcript.text}`

  try {
    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: systemMessage.trim()
        }
      ],
      model: 'llama-3.2-90b-vision-preview',
      response_format: { type: 'json_object' }
    })

    console.log('API response content:', chatCompletion.choices[0]?.message?.content) // Log the response to inspect its format

    const parsedResponse: Quiz = chatCompletion.choices[0]?.message?.content
      ? (JSON.parse(chatCompletion.choices[0].message.content) as Quiz)
      : { questions: [] }

    return parsedResponse
  } catch (error) {
    if (error instanceof Error) {
      console.error('Error generating questions:', error.message)
    }
    const fallbackResponse: Quiz = { questions: [] }
    return fallbackResponse
  }
}
