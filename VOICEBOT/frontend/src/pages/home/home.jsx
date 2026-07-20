import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../chat/main.css";
import "./home.css";
import { BsStars } from "react-icons/bs";
import { FaUserFriends, FaChartLine, FaComments } from "react-icons/fa";

function Card({ to, title, description, Icon }) {
    return (
        <Link to={to} className="main-card no-underline mod-card">
            <p className="card-title">{title}</p>
            <p className="card-description">{description}</p>
            <Icon className="main-card-icon" />
        </Link>
    );
}

export default function Home() {
    const navigate = useNavigate();
    const [displayedText, setDisplayedText] = useState("");
    const fullText = "Transform Your Client Calls to Business Insight";

    useEffect(() => {
        let index = 0;
        const interval = setInterval(() => {
            setDisplayedText(fullText.slice(0, index + 1));
            index++;
            if (index === fullText.length) {
                clearInterval(interval);
            }
        }, 60); // Reduced interval time
        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <div className="main">
                <nav className="main-nav">
                    <p onClick={() => navigate("/")}>Home</p>
                </nav>
                <div className="main-container">
                    <div className="main-greet">
                        <p>
                            <span>Auralytics</span>
                        </p>
                        <p className="animated-text">{displayedText}</p> {/* Add class for animation */}
                    </div>
                    <div className="main-cards">
                        <Card to="/agent" title="Past Clients" description="" Icon={FaUserFriends} />
                        <Card to="/manager/1" title="Check your performance" description="" Icon={FaChartLine} />
                    </div>
                </div>
            </div>
        </>
    );
}
