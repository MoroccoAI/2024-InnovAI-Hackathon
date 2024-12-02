
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
const LogoutButton = () => {
 
   const token = localStorage.getItem("access_token");

  

  if (!token) {
    console.warn("No token found in localStorage.");
    return <button disabled>Déconnexion (non connecté)</button>;
  }

 const handleLogout = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    console.log("Aucun jeton trouvé dans le stockage local.");
    return;
  }

  try {
    
    const response = await axios.post(
      "http://127.0.0.1:8000/api/logout/",
      {}, 
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    console.log("Déconnexion réussie", response.data);
  } catch (error) {
    console.error("Erreur lors de la déconnexion", error);
  }
};

  return <button onClick={handleLogout}>Déconnexion</button>;
};

export default LogoutButton;
