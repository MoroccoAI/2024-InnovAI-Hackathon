// src/store/reducers/quizReducer.ts

// Define the QuizState type (shape of your quiz state)
export type QuizState = {
  questionCount: number
  score: number
  // Add other properties if needed
}

// Initial state for the quiz
const initialState: QuizState = {
  questionCount: 0,
  score: 0
  // Set initial values for other properties
}

// The quiz reducer that handles actions and updates the state
export const quizReducer = (state: QuizState = initialState, action: any): QuizState => {
  switch (action.type) {
    case 'SET_QUESTION_COUNT':
      return {
        ...state,
        questionCount: action.payload
      }
    case 'SET_SCORE':
      return {
        ...state,
        score: action.payload
      }
    // Add other cases as needed
    default:
      return state
  }
}
