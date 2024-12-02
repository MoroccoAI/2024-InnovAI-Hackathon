
import "./Navbar.css";
import e from "../../assets/MEDIapoyo-Transparent-05.png";
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
      const token = localStorage.getItem("access_token");
      if (token) {
        setIsAuthenticated(true); 
      } else {
        setIsAuthenticated(false); 
      }
    }, []);


    const handleLogout = () => {
   
      localStorage.removeItem("access_token");
      setIsAuthenticated(false); 
      navigate("/login"); 
    };


  return (
    <div className="nav">
      <div className="nav-logo">
        <img src={e} alt="Logo" />
      </div>
      <ul className="nav-menu">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/annotation">Chatbot</Link>
        </li>
        <li>
          <Link to="/Signin">Sign in</Link>
        </li>

        {!isAuthenticated && (
          <li className="nav-signup">
            <Link to="/login">Sign Up</Link>
          </li>
        )}

        {isAuthenticated && (
          <li className="nav-logout">
            <button onClick={handleLogout}>Logout</button>
          </li>
        )}
      </ul>
    </div>
  );
};

export default Navbar;
