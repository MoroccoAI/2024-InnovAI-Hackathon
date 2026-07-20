import { useState, useEffect, useRef } from "react";
import "./right_section.css";
import ButtonContainer from "../container_buttons/container_buttons";
import { FaStar, FaChevronDown, FaChevronUp } from 'react-icons/fa'; // Import star and chevron icons
import { BsStars } from "react-icons/bs";

function RenderBlock({ title, description }) {
    return (
        <div>
            <h3 className="right-section-container-h3">{title}</h3>
            <p className="right-section-container-p" dangerouslySetInnerHTML={{ __html: description }}></p>
        </div>
    );
}

function SummaryBlock({selectedItem}) {
    return (
        <div className="right-section-container">
            <div className="right-section-row">
                <div className="right-section-block">
                    <RenderBlock title="Demands" description={selectedItem.metadata.demands} />
                </div>
                <div className="right-section-block">
                    <RenderBlock title="Actions" description={selectedItem.metadata.actions} />
                </div>
            </div>
            <div className="right-section-row">
                <div className="right-section-block full-width">
                    <RenderBlock title="Conclusion" description={selectedItem.metadata.conclusion} />
                </div>
            </div>
            <div className="right-section-row">
                <div className="right-section-block full-width">
                    <RenderBlock title="Next Steps" description={selectedItem.metadata.next_steps} />
                </div>
            </div>
        </div>
    )
}

function TranscriptionBlock({ selectedItem, onBubbleClick, highlightedBubble, highlightedWord, scrollToEnd, expandedBubble, setExpandedBubble, currentTime }) {
    const containerRef = useRef(null);
    const [hoveredBubble, setHoveredBubble] = useState(null);

    useEffect(() => {
        if (highlightedBubble !== null) {
            const element = document.querySelector(`.transcription-chat-bubble[data-offset="${highlightedBubble}"]`);
            if (element && containerRef.current) {
                const containerTop = containerRef.current.getBoundingClientRect().top;
                const elementTop = element.getBoundingClientRect().top;
                const offset = elementTop - containerTop - 50; // Adjust 50 to the height of the header
                containerRef.current.scrollTo({ top: offset, behavior: "smooth" });
            }
        }
    }, [highlightedBubble]);

    useEffect(() => {
        if (scrollToEnd && containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [scrollToEnd]);

    const handleBubbleClick = (offset, duration) => {
        onBubbleClick(offset, duration);
        setExpandedBubble(expandedBubble === offset ? null : offset); // Toggle expanded state
    };

    const handleMouseEnter = (offset) => {
        setHoveredBubble(offset);
    };

    const handleMouseLeave = () => {
        setHoveredBubble(null);
    };

    const formatTime = (time) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    };

    return (
        <>
            <div className="transcription-chat-header">
                <div>Agent</div>
                <div>Client</div>
            </div>
            <div className="transcription-chat-container" ref={containerRef}>
                {selectedItem.transcriptions.map((message, index) => (
                    <div key={index}>
                        <div
                            className={`transcription-chat-bubble ${message.speaker === "Agent" ? "agent" : "client"} ${
                                highlightedBubble === message.offset ? "highlighted" : ""
                            } ${message.proposed_answer ? "has-proposed-answer" : ""}`} // Add class for proposed answer
                            onClick={() => handleBubbleClick(message.offset, message.duration)}
                            onMouseEnter={() => handleMouseEnter(message.offset)}
                            onMouseLeave={handleMouseLeave}
                            data-offset={message.offset}
                        >
                            {message.proposed_answer && <BsStars className="star-icon" />}
                            <div className="transcription-chat-text">
                                {message.text.split(" ").map((word, wordIndex) => (
                                    <span
                                        key={wordIndex}
                                        className={
                                            highlightedBubble === message.offset && highlightedWord >= wordIndex
                                                ? "highlighted-word"
                                                : hoveredBubble === message.offset ||
                                                  (currentTime >= message.offset &&
                                                      currentTime <= message.offset + message.duration)
                                                ? "current-word"
                                                : "default-word"
                                        }
                                    >
                                        {word}{" "}
                                    </span>
                                ))}
                            </div>
                            <div className="timestamp">{formatTime(message.offset)}</div> {/* Add timestamp */}
                            {message.proposed_answer && (
                                <button
                                    className="expand-button"
                                    onClick={(e) => {
                                        e.stopPropagation(); // Prevent bubble click
                                        setExpandedBubble(expandedBubble === message.offset ? null : message.offset);
                                    }}
                                >
                                    {expandedBubble === message.offset ? <FaChevronUp /> : <FaChevronDown />}
                                </button>
                            )}
                        </div>
                        {message.proposed_answer && expandedBubble === message.offset && (
                            <div className={`proposed-answer ${message.speaker === "Agent" ? "agent" : "client"}`}>
                                <div className="proposed-answer-text">{message.proposed_answer}</div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
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

export default function RightSection({ selectedItem, onBubbleClick, highlightedBubble, highlightedWord, scrollToEnd, expandedBubble, setExpandedBubble, currentTime }) {
    const [activeContainer, setActiveContainer] = useState("Transcription");

    console.log(selectedItem.metadata);

    return (
        <>
            <div>
                <div className="sticky-container">
                    <div className="buttons-container">
                        <ButtonContainer
                            activeContainer={activeContainer === "Summary"}
                            setActiveContainer={setActiveContainer}
                            name="Summary"
                        />
                        <ButtonContainer
                            activeContainer={activeContainer === "Transcription"}
                            setActiveContainer={setActiveContainer}
                            name="Transcription"
                        />
                    </div>
                </div>
                {activeContainer == "Summary" && <SummaryBlock selectedItem={selectedItem} />}
                {activeContainer == "Transcription" && <TranscriptionBlock selectedItem={selectedItem} onBubbleClick={onBubbleClick} highlightedBubble={highlightedBubble} highlightedWord={highlightedWord} scrollToEnd={scrollToEnd} expandedBubble={expandedBubble} setExpandedBubble={setExpandedBubble} currentTime={currentTime} />}
            </div>
        </>
    );
}
