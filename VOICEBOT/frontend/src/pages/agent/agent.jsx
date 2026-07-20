import { useOutletContext, useNavigate, useParams } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import "./agent.css";
import "../../pages/chat/main.css"
import { LuPlus, LuMinus } from "react-icons/lu";
import { RiSendPlane2Line } from "react-icons/ri";

export default function AgentUI() {
    const { id } = useParams();
    const { data } = useOutletContext();
    const navigate = useNavigate();
    const [expandedClients, setExpandedClients] = useState([]);
    const [showPopup, setShowPopup] = useState(false);
    const popupRef = useRef(null);
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");

    const groupedData = data.reduce((acc, audio) => {
        if (!acc[audio.client_id]) {
            acc[audio.client_id] = { name: audio.client_name, audios: [], lastDate: audio.date };
        }
        acc[audio.client_id].audios.push(audio);
        if (new Date(audio.date) > new Date(acc[audio.client_id].lastDate)) {
            acc[audio.client_id].lastDate = audio.date;
        }
        return acc;
    }, {});

    const handleClientClick = (client_id) => {
        setExpandedClients((prev) =>
            prev.includes(client_id) ? prev.filter((id) => id !== client_id) : [...prev, client_id]
        );
    };

    const handleAudioClick = (audio) => {
        navigate(`/${audio.id}`, { state: { audio } });
    };

    const handleButtonClick = (event) => {
        event.stopPropagation();
        setShowPopup(true);
    };

    const handleOutsideClick = (event) => {
        if (popupRef.current && !popupRef.current.contains(event.target)) {
            setShowPopup(false);
        }
    };

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleSendMessage = () => {
        if (inputValue.trim()) {
            setMessages([...messages, inputValue]);
            setInputValue("");
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            handleSendMessage();
        }
    };

    useEffect(() => {
        if (showPopup) {
            document.addEventListener("mousedown", handleOutsideClick);
        } else {
            document.removeEventListener("mousedown", handleOutsideClick);
        }
        return () => {
            document.removeEventListener("mousedown", handleOutsideClick);
        };
    }, [showPopup]);

    return (
        <div className="agent-main">
            <nav className="main-nav">
                <p onClick={() => navigate("/")}>Home</p>
            </nav>
            <div className="main-container">
                <div className="main-greet">
                    <p>
                        <span>Hello,</span>
                    </p>
                    <p>These are your past clients</p>
                </div>
                <div className="agent-cards fixed-container">
                        {Object.keys(groupedData).map((client_id) => (
                            <div
                                key={client_id}
                                className="agent-card no-underline"
                                onClick={() => handleClientClick(client_id)}
                            >
                                <p className="agent-title">{groupedData[client_id].name}</p>
                                <p className="agent-description">Last interaction: {groupedData[client_id].lastDate}</p>
                                {expandedClients.includes(client_id) ? (
                                    <LuMinus className="agent-icon" />
                                ) : (
                                    <LuPlus className="agent-icon" />
                                )}
                                {expandedClients.includes(client_id) && (
                                    <div className="agent-audios">
                                        {groupedData[client_id].audios.map((audio, index) => (
                                            <div key={index} onClick={() => handleAudioClick(audio)}>
                                                <p>{audio.title}</p>
                                                <p>{audio.date}</p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                </div>
            </div>
        </div>
    );
}
