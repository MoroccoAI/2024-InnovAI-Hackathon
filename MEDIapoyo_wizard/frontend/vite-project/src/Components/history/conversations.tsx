import React, { useState, useEffect } from "react";
import axios from "axios";
import "./conversations.css"; // Ajoutez un fichier CSS pour le style

interface Conversation {
  id: number;
  title: string;
  lastMessage: string;
  updatedAt: string;
}

const Conversations: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/conversations/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setConversations(response.data);
      } catch (err) {
        setError("Failed to load conversations. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  if (loading) {
    return <div className="loading">Loading conversations...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="conversations">
      <h2>Conversation History</h2>
      <ul className="conversation-list">
        {conversations.map((conversation) => (
          <li key={conversation.id} className="conversation-item">
            <h3>{conversation.title}</h3>
            <p className="last-message">{conversation.lastMessage}</p>
            <span className="updated-at">
              {new Date(conversation.updatedAt).toLocaleString()}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Conversations;
