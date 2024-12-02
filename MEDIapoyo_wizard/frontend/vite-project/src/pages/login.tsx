import React, { useState } from "react";
import "./pages.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const navigate = useNavigate();


  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>(""); // Pour afficher les erreurs de connexion


  const handleLoginClick = async (e: React.FormEvent) => {
    e.preventDefault();
    

    try {
    
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        username,
        password,
      });
      const token = response.data.access;
      const refreshToken = response.data.refresh;
localStorage.setItem("access_token", token);
localStorage.setItem("refresh_token", refreshToken);
      if (token) {
        localStorage.setItem("access_token", token);
        localStorage.setItem("refresh_token", refreshToken); // Stockage du token de rafraîchissement
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        console.log("Connexion réussie et token stocké.");
      }

      if (response.status === 200) {
        console.log("Login successful:", response.data);
     
        navigate("/annotation");
      }
    } catch (err) {
     
      if (axios.isAxiosError(err)) {
        setError(err.response?.data.detail || "Une erreur est survenue");
      } else {
        setError("Une erreur inconnue est survenue");
      }
    }
  };

  return (
    <div className="wrapper">
      <h1>Login</h1>
      <p>Welcome, please write your information</p>
      <form onSubmit={handleLoginClick}>
        <input
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error-message">{error}</p>}{" "}

        <p className="recover">
          <a href="#">Recover Password</a>
        </p>
        <button type="submit" className="btn2">
          Sign in
        </button>
      </form>
      <div className="icons">
        <i className="fab fa-google"></i>
        <i className="fab fa-github"></i>
        <i className="fab fa-facebook"></i>
      </div>
      <p className="or">----- or continue with -----</p>
      <div className="not-member">
        Not a member? <a href="/signin">Register Now</a>
      </div>
    </div>
  );
};

export default Login;

