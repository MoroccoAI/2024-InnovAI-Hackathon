import React from 'react';
import './pages.css';
import { useNavigate } from 'react-router-dom';

const CreateAccount = () => {
    const navigate = useNavigate();

    const handleSignUpClick = () => {
        navigate('/welcome'); // Redirect after account creation
    };

    return (
        <div className="wrapper">
            <h1>Create Account</h1>
            <p>Welcome! Please fill in the details to register</p>
            <form>
                <input type="text" placeholder="Enter username" required />
                <input type="email" placeholder="Enter email" required />
                <input type="password" placeholder="Password" required />
            </form>
            <button className="btn2" onClick={handleSignUpClick}>Sign Up</button>
            <div className="icons">
                <i className="fab fa-google"></i>
                <i className="fab fa-github"></i>
                <i className="fab fa-facebook"></i>
            </div>
            <p className="or">----- or sign up with -----</p>
            <div className="not-member">
                Already have an account? <a href="/login">Login</a>
            </div>
        </div>
    );
};

export default CreateAccount;
