// src/store/reducers/authReducer.ts

// Define the AuthState type (shape of your auth state)
export type AuthState = {
  isAuthenticated: boolean
  user: any // Replace `any` with a more specific type if you have a user model
}

// Initial state for authentication
const initialState: AuthState = {
  isAuthenticated: false,
  user: null // Set initial value for user
}

// The auth reducer that handles login and logout actions
export const authReducer = (state: AuthState = initialState, action: any): AuthState => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload
      }
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null
      }
    default:
      return state
  }
}
