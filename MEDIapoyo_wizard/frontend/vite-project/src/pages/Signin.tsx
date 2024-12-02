import React, { useState } from "react";
import "./pages.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signin: React.FC = () => {
  const navigate = useNavigate();

  // États pour capturer les informations du formulaire
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>(""); // Pour afficher les erreurs

  // Fonction de gestion de la soumission du formulaire
  const handleSignUpClick = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Envoi des données de l'utilisateur à l'API Django
      const response = await axios.post(
        "http://127.0.0.1:8000/api/create-user/",
        {
          username,
          email,
          password,
        }
      );

      console.log("User created successfully:", response.data);

      // Rediriger l'utilisateur vers la page de connexion après la création du compte
      navigate("/login");
    } catch (err) {
      // Gestion des erreurs d'API
      if (axios.isAxiosError(err)) {
        setError(err.response?.data.detail || "Une erreur est survenue");
      } else {
        // Gestion des autres erreurs
        setError("Une erreur inconnue est survenue");
      }
    }
  };

  return (
    <div className="wrapper">
      <h1>Sign in</h1>
      <p>Welcome! Please fill in the details to register</p>
      <form onSubmit={handleSignUpClick}>
        <input
          type="text"
          placeholder="Enter username"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Enter email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="btn2">
          Sign Up
        </button>
      </form>
      {error && <p className="error-message">{error}</p>}{" "}
      {/* Afficher l'erreur si présente */}
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

export default Signin;
