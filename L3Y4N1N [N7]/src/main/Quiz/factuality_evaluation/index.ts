import { readFileSync } from 'fs'
import Groq from 'groq-sdk'
import prompt from '@resources/prompts/factualityPrompt.md?asset'
import { FactCheckFeedback, Transcript } from '../../../types/types'
const groq = new Groq({ apiKey: process.env.FACT_API })

const evalFactuality = async (
  transcription: Transcript,
  question: string,
  response: string
): Promise<FactCheckFeedback | null> => {
  try {
    const factualityPrompt = readFileSync(prompt, 'utf8')

    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: factualityPrompt
        },
        {
          role: 'user',
          content: JSON.stringify({
            transcription: transcription,
            question: question,
            response: response
          })
        }
      ],
      model: 'llama3-8b-8192',
      response_format: { type: 'json_object' }
    })

    const feedback = chatCompletion.choices[0]?.message?.content
      ? (JSON.parse(chatCompletion.choices[0].message.content) as FactCheckFeedback)
      : null

    return feedback
  } catch (error) {
    console.error('Error fetching chat completion:', error)
    return null
  }
}

export default evalFactuality
