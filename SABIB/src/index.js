import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './scss/main.scss';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { ClerkProvider, useUser } from '@clerk/clerk-react';
import Dashboard from './components/dashboard/Dashboard';
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';
import Loader from './components/UI/Dashboard/loader/Loader';

import firebase from 'firebase/compat/app'; // Import Firebase from compat module
import 'firebase/compat/auth';
import { firebaseConfig } from './config/firebase'; // Assuming firebaseConfig.js contains your Firebase config

const publishableKey = process.env.REACT_APP_CLERK_PUBLISHABLE_KEY;

// Initialize Firebase if not already initialized
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
} else {
  firebase.app();
}

const ClerkWithRoutes = () => {
  return (
    <ClerkProvider publishableKey={publishableKey}>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard/*" element={<Dashboard />}/>
      </Routes>
    </ClerkProvider>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <ClerkWithRoutes />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
