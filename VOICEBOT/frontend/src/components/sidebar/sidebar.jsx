import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./sidebar.css";

export default function SideBar({ navigateToHome, currentPage, data }) {
    const navigate = useNavigate();
    const [expandedItems, setExpandedItems] = useState({});

    const groupedData = data.reduce((acc, audio) => {
        if (currentPage.includes("manager")) {
            if (!acc[audio.agent_id]) {
                acc[audio.agent_id] = [];
            }
            acc[audio.agent_id].push(audio);
        } else if (currentPage.includes("agent")) {
            if (!acc[audio.client_id]) {
                acc[audio.client_id] = [];
            }
            acc[audio.client_id].push(audio);
        }
        return acc;
    }, {});

    const toggleExpand = (id) => {
        setExpandedItems((prev) => ({
            ...prev,
            [id]: !prev[id],
        }));
    };

    return (
        <div className="sidebar-container">
            <div className="menu" onClick={navigateToHome}>
                Menu
            </div>
            <ul>
                {currentPage.includes("manager") &&
                    Object.keys(groupedData).map((agent_id) => (
                        <li key={agent_id}>
                            <div onClick={() => toggleExpand(agent_id)}>
                                Agent ID: {agent_id}
                            </div>
                            {expandedItems[agent_id] && (
                                <div className="expanded-content">
                                    {groupedData[agent_id].map(
                                        (audio, index) => (
                                            <div key={index} className="detail-item" onClick={() => navigate(`/audioDetail/${audio.audio_path}`)}>
                                                <p>
                                                    Audio Path:{" "}
                                                    {audio.audio_path}
                                                </p>
                                                <p>
                                                    Agent Name:{" "}
                                                    {audio.agent_name}
                                                </p>
                                                <p>Date: {audio.date}</p>
                                                <p>Title: {audio.title}</p>
                                                <p>
                                                    Client ID: {audio.client_id}
                                                </p>
                                                <p>
                                                    Client Name:{" "}
                                                    {audio.client_name}
                                                </p>
                                            </div>
                                        )
                                    )}
                                </div>
                            )}
                        </li>
                    ))}
                {currentPage.includes("agent") &&
                    Object.keys(groupedData).map((client_id) => (
                        <li key={client_id}>
                            <div onClick={() => toggleExpand(client_id)}>
                                Client ID: {client_id}
                            </div>
                            {expandedItems[client_id] && (
                                <div className="expanded-content">
                                    {groupedData[client_id].map(
                                        (audio, index) => (
                                            <div key={index} className="detail-item" onClick={() => navigate(`/audioDetail/${audio.audio_path}`)}>
                                                <p>
                                                    Audio Path:{" "}
                                                    {audio.audio_path}
                                                </p>
                                                <p>
                                                    Agent Name:{" "}
                                                    {audio.agent_name}
                                                </p>
                                                <p>Date: {audio.date}</p>
                                                <p>Title: {audio.title}</p>
                                                <p>
                                                    Client ID: {audio.client_id}
                                                </p>
                                                <p>
                                                    Client Name:{" "}
                                                    {audio.client_name}
                                                </p>
                                            </div>
                                        )
                                    )}
                                </div>
                            )}
                        </li>
                    ))}
            </ul>
        </div>
    );
}
