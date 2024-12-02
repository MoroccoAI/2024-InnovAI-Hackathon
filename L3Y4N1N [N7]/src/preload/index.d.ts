import { ElectronAPI } from '@electron-toolkit/preload'
import {
  FactCheckRequestEvent,
  FactCheckResponseEvent,
  GrammarEvalResponseEvent
} from 'src/types/events'

declare global {
  interface Window {
    electron: ElectronAPI
    electronAPI: {
      getQuizzes: (transcript: string) => Promise<Quizzes>
    }
    api: {
      evalGrammar: (
        grammarEvalRequest: GrammarEvalRequestEvent
      ) => Promise<GrammarEvalResponseEvent>
      generateQuiz: (transcript: Transcript) => Promise<QuizResponseEvent>
      evalFactCheck: (factCheckRequest: FactCheckRequestEvent) => Promise<FactCheckResponseEvent>
    }
  }
}
