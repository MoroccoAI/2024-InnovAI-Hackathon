import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import './Login.css';

function Login() {
  return (
      <div className="login-container"> {/* Add a class name for styling */}
        <SignIn  signUpUrl='/signup'/>
      </div>
  
  );
}

export default Login;
