// src/store/store.ts

import { configureStore } from '@reduxjs/toolkit'
import rootReducer from './rootReducer'

// Create and configure the Redux store
const store = configureStore({
  reducer: rootReducer
})

export default store
