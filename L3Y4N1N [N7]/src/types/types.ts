export interface TranscriptSegment {
  start: number
  end: number
  text: string
}

export class Transcript {
  text: string
  segegments: TranscriptSegment[]

  constructor(text: string, segegments: TranscriptSegment[]) {
    this.segegments = segegments
    this.text = text
  }

  toText(): string {
    return this.segegments
      .map((segment, index) => {
        const start = new Date(segment.start * 1000).toISOString().substr(11, 12).replace('.', ',')
        const end = new Date(segment.end * 1000).toISOString().substr(11, 12).replace('.', ',')
        return `${index + 1}\n${start} --> ${end}\n${segment.text}\n`
      })
      .join('\n')
  }
}

export interface Question {
  difficulty: string
  skill: string
  prompt: string
}

export interface Quiz {
  questions: Question[]
}

export interface GrammarFeedback {
  original_text: string
  corrected_text: string
  feedback: {
    error: string
    type: string
    explanation: {
      problem: string
      rule: string
    }
  }[]
}

export interface FactCheckFeedback {
  grade: 'correct' | 'partially correct' | 'wrong'
  user_response: string
  feedback: {
    missed_part: string
    correct_info: string
    timestamp: number
    explanation: string
  }[]
}
