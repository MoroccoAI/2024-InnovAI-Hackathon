import { FactCheckFeedback, GrammarFeedback, Question, Transcript } from './types'

class Event {}

export class QuizRequestEvent extends Event {
  static event = 'quiz-request'
  constructor(public transcript: Transcript) {
    super()
  }
}

export class QuizContentEvent extends Event {
  static event = 'quiz-response'
  constructor(public questions: Question[]) {
    super()
  }
}

export class QuizErrorEvent extends Event {
  static event = 'quiz-error'
  constructor(public error: string) {
    super()
  }
}

export type QuizResponseEvent = QuizContentEvent | QuizErrorEvent

export class GrammarEvalRequestEvent extends Event {
  static event = 'grammar-eval-request'
  constructor(public userResponse: string) {
    super()
  }
}

export class GrammarEvalFeedbackEvent extends Event {
  static event = 'grammar-eval-response'
  constructor(public feedback: GrammarFeedback) {
    super()
  }
}

export class GrammarEvalErrorEvent extends Event {
  static event = 'grammar-eval-error'
  constructor(public error: string) {
    super()
  }
}

export type GrammarEvalResponseEvent = GrammarEvalFeedbackEvent

export class FactCheckRequestEvent extends Event {
  static event = 'fact-check-request'
  constructor(
    public transcript: Transcript,
    public question: string,
    public userResponse: string
  ) {
    super()
  }
}

export class FactCheckFeedbackEvent extends Event {
  static event = 'fact-check-response'
  constructor(public feedback: FactCheckFeedback) {
    super()
  }
}

export class FactCheckErrorEvent extends Event {
  static event = 'fact-check-error'
  constructor(public error: string) {
    super()
  }
}

export type FactCheckResponseEvent = FactCheckFeedbackEvent
