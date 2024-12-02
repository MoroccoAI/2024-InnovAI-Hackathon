import React from 'react'
import ReactDOM from 'react-dom/client' // Import from 'react-dom/client'
import { Provider } from 'react-redux'
import App from './App'
import store from './store'

// Create a root using `createRoot`
const rootElement = document.getElementById('root') // Get the root element from the DOM

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement) // Create the root instance

  root.render(
    <Provider store={store}>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </Provider>
  )
} else {
  console.error('Root element not found') // Handle the case where root element is missing
}
