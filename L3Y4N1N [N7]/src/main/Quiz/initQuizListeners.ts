import { ipcMain } from 'electron'
import {
  QuizRequestEvent,
  QuizContentEvent,
  QuizErrorEvent,
  GrammarEvalRequestEvent,
  GrammarEvalFeedbackEvent,
  GrammarEvalErrorEvent,
  FactCheckRequestEvent,
  FactCheckFeedbackEvent,
  FactCheckErrorEvent
} from '../../types/events'
import getQuiz from './question_generation'
import evalGrammar from './grammar_error_correction'
import evalFactuality from './factuality_evaluation'
import { Transcript } from '../../types/types'

export function initQuizListeners(): void {
  // Handle QuizRequestEvent
  ipcMain.handle(QuizRequestEvent.event, async (_event, arg) => {
    const transcript: Transcript = arg

    try {
      const quiz = await getQuiz(transcript)
      return new QuizContentEvent(quiz.questions)
    } catch (error) {
      if (error instanceof Error) {
        return new QuizErrorEvent(error.message)
      } else {
        return new QuizErrorEvent('Unknown error occurred')
      }
    }
  })

  // Handle GrammarEvalRequestEvent
  ipcMain.handle(GrammarEvalRequestEvent.event, async (_event, arg) => {
    console.log('GrammarEvalRequestEvent', arg)
    const userResponse: string = arg

    try {
      const feedback = await evalGrammar(userResponse)
      if (feedback) {
        return new GrammarEvalFeedbackEvent(feedback)
      } else {
        return new GrammarEvalErrorEvent('No feedback received')
      }
    } catch (error) {
      if (error instanceof Error) {
        return new GrammarEvalErrorEvent(error.message)
      } else {
        return new GrammarEvalErrorEvent('Unknown error occurred')
      }
    }
  })

  // Handle FactCheckRequestEvent
  ipcMain.handle(FactCheckRequestEvent.event, async (_event, arg) => {
    console.log('FactCheckRequestEvent', arg)
    const { transcript, question, userResponse } = arg

    try {
      const feedback = await evalFactuality(transcript, question, userResponse)
      if (feedback) {
        return new FactCheckFeedbackEvent(feedback)
      } else {
        return new FactCheckErrorEvent('No feedback received')
      }
    } catch (error) {
      if (error instanceof Error) {
        return new FactCheckErrorEvent(error.message)
      } else {
        return new FactCheckErrorEvent('Unknown error occurred')
      }
    }
  })
}
