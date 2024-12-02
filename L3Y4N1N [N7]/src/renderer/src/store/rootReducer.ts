// src/store/rootReducer.ts

import { combineReducers } from '@reduxjs/toolkit'
import { quizReducer } from './reducers/quizReducer'
import { authReducer } from './reducers/authReducer'
import { QuizState } from './reducers/quizReducer'
import { AuthState } from './reducers/authReducer'

// Combine reducers into rootReducer
const rootReducer = combineReducers({
  quiz: quizReducer,
  auth: authReducer
})

// Define RootState type that represents the whole app state
export type RootState = {
  quiz: QuizState
  auth: AuthState
}

export default rootReducer
