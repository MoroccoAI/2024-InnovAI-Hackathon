import { useState } from "react";
import "./lower_left.css";
import ButtonContainer from "../container_buttons/container_buttons";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

function SentimentOverAudio({ selectedItem, wavesurfer, highlightedBubble }) {
    const channels = { Agent: [], Client: [] };

    // Organize the data into channels based on the speaker
    selectedItem.transcriptions.forEach((dialog) => {
        channels[dialog.speaker].push(dialog);
    });

    const maxTime = Math.max(...selectedItem.transcriptions.map((dialog) => dialog.offset + dialog.duration));

    const handleBlockClick = (offset) => {
        if (wavesurfer) {
            wavesurfer.seekTo(offset / wavesurfer.getDuration());
        }
    };

    return (
        <div className="sentiment-audio-visualizer-container">
            {Object.entries(channels).map(([speaker, dialogs]) => (
                <div key={speaker} className="sentiment-audio-channel-row">
                    <div className={`sentiment-audio-speaker-label ${speaker.toLowerCase()}`}></div>
                    <div className="sentiment-audio-timeline">
                        {dialogs.map((dialog, index) => (
                            <div
                                key={index}
                                className={`sentiment-audio-dialog-block ${
                                    highlightedBubble === dialog.offset ? "highlighted" : ""
                                }`}
                                style={{
                                    left: `${(dialog.offset / maxTime) * 100}%`,
                                    width: `${(dialog.duration / maxTime) * 100}%`,
                                    backgroundColor:
                                        dialog.sentiment === "positif"
                                            ? "green"
                                            : dialog.sentiment === "negative"
                                            ? "red"
                                            : "gray",
                                }}
                                title={`Sentiment: ${dialog.sentiment}\nOffset: ${dialog.offset}\nDuration: ${dialog.duration}`}
                                onClick={() => handleBlockClick(dialog.offset)}
                            ></div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}

function SatisfactionBlock({ selectedItem, wavesurfer }) {
    const computeSentimentPercentages = (transcriptions, speaker) => {
        const sentiments = transcriptions.filter((t) => t.speaker === speaker).map((t) => t.sentiment);
        const positive = sentiments.filter((s) => s === "positif").length / sentiments.length;
        const negative = sentiments.filter((s) => s === "negative").length / sentiments.length;
        const neutral = sentiments.filter((s) => s === "neutral").length / sentiments.length;
        return { positive, negative, neutral };
    };

    const sentimentDataAgent = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
            {
                // label: 'Agent',
                data: Object.values(computeSentimentPercentages(selectedItem.transcriptions, "Agent")),
                backgroundColor: ["rgba(0, 128, 0, 0.3)", "rgba(255, 0, 0, 0.3)", "rgba(128, 128, 128, 0.3)"], // Updated colors with opacity
            },
        ],
    };

    const sentimentDataClient = {
        labels: ["Positive", "Negative", "Neutral"],
        datasets: [
            {
                // label: "Client",
                data: Object.values(computeSentimentPercentages(selectedItem.transcriptions, "Client")),
                backgroundColor: ["rgba(0, 128, 0, 0.3)", "rgba(255, 0, 0, 0.3)", "rgba(128, 128, 128, 0.3)"], // Updated colors with opacity
            },
        ],
    };

    const options = {
        plugins: {
            legend: {
                display: true,
                position: "right",
            },
        },
    };

    return (
        <>
            <SentimentOverAudio selectedItem={selectedItem} wavesurfer={wavesurfer} />
            <div className="satisfaction-container">
                <div className="chart">
                    <h3>Agent</h3>
                    <p className="chart-text">{selectedItem.metadata.sentiment_desc_client}</p> {/* Added text */}
                    <Doughnut data={sentimentDataAgent} options={options} />
                </div>
                <div className="chart">
                    <h3>Client</h3>
                    <p className="chart-text">{selectedItem.metadata.sentiment_desc_agent}</p> {/* Added text */}
                    <Doughnut data={sentimentDataClient} options={options} />
                </div>
            </div>
        </>
    );
}

function DetailsBlock({ selectedItem }) {
    return (
        <>
            <div>sss</div>
        </>
    );
}

function TagsBlock({ selectedItem, wavesurfer, setHighlightedBubble, handleDialogClick }) {
    const [selectedTag, setSelectedTag] = useState(null);
    const [selectedDialog, setSelectedDialog] = useState(null); // Add state for selected dialog

    const tags = [...new Set(selectedItem.transcriptions.map((dialog) => dialog.tag))].filter(tag => tag);

    const handleTagClick = (tag) => {
        setSelectedTag(tag);
        const firstOccurrence = selectedItem.transcriptions.find((dialog) => dialog.tag === tag);
        if (firstOccurrence && wavesurfer) {
            wavesurfer.seekTo(firstOccurrence.offset / wavesurfer.getDuration());
            setHighlightedBubble(firstOccurrence.offset);
        }
    };

    const handleDialogItemClick = (dialog) => {
        setSelectedDialog(dialog.offset); // Set the selected dialog
        handleDialogClick(dialog.offset);
    };

    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    };

    const filteredDialogs = selectedItem.transcriptions.filter((dialog) => dialog.tag === selectedTag);

    return (
        <div className="tags-block-container">
            <div className="tags-list-container">
                <div className="tags-list">
                    {tags.length > 0 ? (
                        tags.map((tag, index) => (
                            <button
                                key={index}
                                className={`tag-item ${tag === selectedTag ? "active" : ""}`}
                                onClick={() => handleTagClick(tag)}
                            >
                                {tag}
                            </button>
                        ))
                    ) : (
                        <div>No clusters</div>
                    )}
                </div>
            </div>
            <div className="dialogs-list">
                {filteredDialogs.map((dialog, index) => (
                    <div
                        key={index}
                        className={`dialog-item ${selectedDialog === dialog.offset ? "active" : ""}`} // Add active class
                        onClick={() => handleDialogItemClick(dialog)}
                    >
                        <strong>{dialog.speaker}:</strong> {dialog.text} <em>({formatTime(dialog.offset)})</em>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default function LowerLeftSection({ selectedItem, wavesurfer, setHighlightedBubble, handleDialogClick }) {
    const [activeContainer, setActiveContainer] = useState("Satisfaction");

    return (
        <>
            <div className="lower-left">
                <div className="buttons-container">
                    <ButtonContainer
                        activeContainer={activeContainer === "Satisfaction"}
                        setActiveContainer={setActiveContainer}
                        name="Satisfaction"
                    />
                    {/* <ButtonContainer
                        activeContainer={activeContainer === "Details"}
                        setActiveContainer={setActiveContainer}
                        name="Details"
                    /> */}
                    <ButtonContainer
                        activeContainer={activeContainer === "Tags"}
                        setActiveContainer={setActiveContainer}
                        name="Tags"
                    />
                </div>

                {activeContainer == "Satisfaction" && (
                    <SatisfactionBlock selectedItem={selectedItem} wavesurfer={wavesurfer} />
                )}
                {/* {activeContainer == "Details" && <DetailsBlock selectedItem={selectedItem} />} */}
                {activeContainer == "Tags" && (
                    <TagsBlock
                        selectedItem={selectedItem}
                        wavesurfer={wavesurfer}
                        setHighlightedBubble={setHighlightedBubble}
                        handleDialogClick={handleDialogClick} // Pass the handleDialogClick function
                    />
                )}
            </div>
        </>
    );
}
