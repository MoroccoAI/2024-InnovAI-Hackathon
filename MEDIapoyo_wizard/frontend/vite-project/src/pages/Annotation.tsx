import React, { useState } from 'react';
import './Annotation.css';

const Annotation = () => {
    const [messages, setMessages] = useState([
        { text: "Hello! How can I assist you today?", sender: "bot" }
    ]);
    const [input, setInput] = useState("");

    const handleSend = () => {
        if (input.trim() !== "") {
            setMessages([...messages, { text: input, sender: "user" }]);
            setInput("");
            setTimeout(() => {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: "This is a bot response.", sender: "bot" }
                ]);
            }, 1000); // Simulate bot response delay
        }
    };

    return (
        <div className="chatbot-container">
            <div className="chat-header">
                <h2>Chatbot</h2>
            </div>
            <div className="chat-body">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.sender === "bot" ? "bot-message" : "user-message"}`}
                    >
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="chat-footer">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
};

export default Annotation;
