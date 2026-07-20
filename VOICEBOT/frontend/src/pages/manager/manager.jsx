import { useOutletContext, useNavigate, useParams } from "react-router-dom";
import Box from "../../components/box/box";
// import "../../app.css";
import "./manager.css";
import { Doughnut } from "react-chartjs-2";
import { useEffect, useState } from "react";
import { LuPlus, LuMinus } from "react-icons/lu";

export default function ManagerUI() {
    const { agent_id } = useParams();
    const { data } = useOutletContext();
    const navigate = useNavigate();
    const [selectedAgent, setSelectedAgent] = useState(agent_id || "");
    const [isExpanded, setIsExpanded] = useState(false);

    const groupedData = data.reduce((acc, audio) => {
            if (!acc[audio.agent_id]) {
            acc[audio.agent_id] = [];
        }
        acc[audio.agent_id].push(audio);
        return acc;
    }, {});

    const calculateStats = (agentData) => {
        const totalClients = agentData.length;
        let positiveSentiment = 0;
        let negativeSentiment = 0;
        let neutralSentiment = 0;
        let resolvedProblems = 0;
        let unresolvedProblems = 0;

        agentData.forEach(audio => {
            audio.transcriptions.forEach(transcription => {
                if (transcription.sentiment === 'positif') {
                    positiveSentiment++;
                } else if (transcription.sentiment === 'negative') {
                    negativeSentiment++;
                } else if (transcription.sentiment === 'neutral') {
                    neutralSentiment++;
                }
            });
            if (audio.resolved) {
                resolvedProblems++;
            } else {
                unresolvedProblems++;
            }
        });

        const totalSentiments = positiveSentiment + negativeSentiment + neutralSentiment;

        return {
            totalClients,
            positiveSentiment: (positiveSentiment / totalSentiments) * 100,
            negativeSentiment: (negativeSentiment / totalSentiments) * 100,
            neutralSentiment: (neutralSentiment / totalSentiments) * 100,
            resolvedProblems: (resolvedProblems / totalClients) * 100,
            unresolvedProblems: (unresolvedProblems / totalClients) * 100,
        };
    };

    const getTags = (agentData) => {
        const tags = {};
        agentData.forEach(audio => {
            audio.transcriptions.forEach(transcription => {
                if (!tags[transcription.tag]) {
                    tags[transcription.tag] = 0;
                }
                tags[transcription.tag]++;
            });
        });
        return tags;
    };

    const handleAgentChange = (event) => {
        const newAgentId = event.target.value;
        setSelectedAgent(newAgentId);
        navigate(`/manager/${newAgentId}`);
    };

    const toggleExpand = () => {
        setIsExpanded(!isExpanded);
    };

    const stats = selectedAgent ? calculateStats(groupedData[selectedAgent]) : null;
    const tags = selectedAgent ? getTags(groupedData[selectedAgent]) : {};

    const doughnutDataSentiment = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
            {
                data: stats ? [stats.positiveSentiment, stats.negativeSentiment, stats.neutralSentiment] : [],
                backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
                hoverBackgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
            },
        ],
    };

    const doughnutDataProblems = {
        labels: ["Resolved", "Unresolved"],
        datasets: [
            {
                data: stats ? [stats.resolvedProblems, stats.unresolvedProblems] : [],
                backgroundColor: ["#4CAF50", "#F44336"],
                hoverBackgroundColor: ["#4CAF50", "#F44336"],
            },
        ],
    };

    const [expandedClients, setExpandedClients] = useState([]);
    const handleClientClick = (client_id, audio) => {
        if (audio && audio.metadata) {
            navigate(`/${client_id}`, { state: { audio } });
        } else {
            console.error("Audio or its metadata is undefined");
        }
    };

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
                <div className="manager-main-container">
                    <div className="main-greet">
                        <p>
                            <span>Performance</span>
                        </p>
                        <p className="animated-text">{displayedText}</p> {/* Add class for animation */}
                    </div>
                    <div className="upper-container">
                        <div className="stats-container">
                            <h3>Performance Stats</h3>
                            {groupedData[1] && (
                                <div>
                                    <p>Total Clients: {stats.totalClients}</p>
                                    <div className="doughnut-plots">
                                        <div className="doughnut-plot small">
                                            <h4>Overall sentiment of clients with the agent</h4>
                                            <Doughnut data={doughnutDataSentiment} />
                                        </div>
                                        <div className="doughnut-plot small">
                                            <h4>Percentage of resolved and unresolved problems</h4>
                                            <Doughnut data={doughnutDataProblems} />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                        <div className="tags-container">
                            <h3>Most Frequent Tags</h3>
                            {Object.keys(tags)
                                .filter((tag) => tag)
                                .map((tag, index) => (
                                    <button key={index} className="tag-button" title={`Dialogues: ${tags[tag]}`}>
                                        {tag}
                                    </button>
                                ))}
                        </div>
                    </div>
                    <div className="clients-container">
                        <h3>Client Interactions</h3>
                        {groupedData[1]?.map((audio, index) => (
                            <div key={index} className="client-item" onClick={() => handleClientClick(audio.id, audio)}>
                                <div className="client-content">
                                    <p>Agent Name: {audio.agent_name}</p>
                                    <p>Date: {audio.date}</p>
                                    <p>Title: {audio.title}</p>
                                    <p>Client Name: {audio.client_name}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}
