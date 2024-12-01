import React from 'react'
import { SignUp } from '@clerk/clerk-react';
import './Login.css';

function Signup() {
  return (
    <div className="login-container"> {/* Add a class name for styling */}
      <SignUp  signInUrl='/login'/>
    </div>

  )
}
export default Signup