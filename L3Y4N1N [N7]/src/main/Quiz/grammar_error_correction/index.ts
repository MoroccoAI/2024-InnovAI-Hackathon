import Groq from 'groq-sdk'
import { readFileSync } from 'fs'
import prompt from '@resources/prompts/grammarErrorCorrection.md?asset'
import { GrammarFeedback } from '../../../types/types'

const groq = new Groq({ apiKey: process.env.GRAMMAR_API })

const evalGrammar = async (textToEval: string): Promise<GrammarFeedback | null> => {
  try {
    const grammarPrompt = readFileSync(prompt, 'utf8')

    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: grammarPrompt
        },
        {
          role: 'user',
          content: textToEval
        }
      ],
      model: 'llama3-8b-8192',
      response_format: { type: 'json_object' }
    })

    const feedback = chatCompletion.choices[0]?.message?.content
      ? (JSON.parse(chatCompletion.choices[0].message.content) as GrammarFeedback)
      : null

    return feedback
  } catch (error) {
    console.error('Error fetching chat completion:', error)
    return null
  }
}

export default evalGrammar
