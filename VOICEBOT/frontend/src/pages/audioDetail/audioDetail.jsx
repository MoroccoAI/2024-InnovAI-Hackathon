import { useOutletContext, useParams, useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import UpperLeftSection from "../../components/upper_left_section/upper_left.jsx";
import LowerLeftSection from "../../components/lower_left_section/lower_left.jsx";
import RightSection from "../../components/right_section/right_section.jsx";
import { Fragment, useState, useRef, useEffect } from "react";
// import "../../app.css";
import "./audioDetail.css";

function AudioPlayer({
    selectedItem,
    volume,
    setVolume,
    currentTime,
    setCurrentTime,
    totalTime,
    setTotalTime,
    wavesurfer,
    setWavesurfer,
    isPlaying,
    setIsPlaying,
    highlightedBubble,
    setHighlightedBubble,
    highlightedWord,
    setHighlightedWord,
    audioPosition,
    setAudioPosition,
    scrollToEnd,
    expandedBubble, // New state for expanded bubble
    setExpandedBubble, // Pass setExpandedBubble function
    loading,
    setLoading,
}) {
    function handleBubbleClick(offset, duration) {
        if (wavesurfer) {
            wavesurfer.seekTo(offset / wavesurfer.getDuration());
            setCurrentTime(offset); // Update the current time
            setHighlightedBubble(offset); // Update the highlighted bubble
            const currentBubble = selectedItem.transcriptions.find(
                (transcription) =>
                    offset >= transcription.offset && offset <= transcription.offset + transcription.duration
            );
            if (currentBubble) {
                const words = currentBubble.text.split(" ");
                const wordDuration = currentBubble.duration / words.length;
                const wordIndex = Math.floor((offset - currentBubble.offset) / wordDuration);
                setHighlightedWord(wordIndex);
            }
        }
    }

    function handleDialogClick(offset) {
        if (wavesurfer) {
            wavesurfer.seekTo(offset / wavesurfer.getDuration());
            setHighlightedBubble(offset);
            document.querySelector(".right").scrollTop = 0; // Reset scroll position in the right section
        }
    }

    function handleAudioClick(time) {
        if (wavesurfer) {
            wavesurfer.seekTo(time / wavesurfer.getDuration());
            setCurrentTime(time);
            setAudioPosition(time);
            const currentBubble = selectedItem.transcriptions.find(
                (transcription) =>
                    time >= transcription.offset &&
                    time <= transcription.offset + transcription.duration
            );
            setHighlightedBubble(currentBubble ? currentBubble.offset : null);
            if (currentBubble) {
                const words = currentBubble.text.split(" ");
                const wordDuration = currentBubble.duration / words.length;
                const wordIndex = Math.floor((time - currentBubble.offset) / wordDuration);
                setHighlightedWord(wordIndex);
            }
            document.querySelector(".right").scrollTop = 0; // Reset scroll position in the right section
        }
    }

    useEffect(() => {
        if (wavesurfer) {
            wavesurfer.on("audioprocess", () => {
                const currentTime = wavesurfer.getCurrentTime();
                setCurrentTime(currentTime);
                setAudioPosition(currentTime); // Update audio position
                const currentBubble = selectedItem.transcriptions.find(
                    (transcription) =>
                        currentTime >= transcription.offset &&
                        currentTime <= transcription.offset + transcription.duration
                );
                setHighlightedBubble(currentBubble ? currentBubble.offset : null);
                if (currentBubble) {
                    const words = currentBubble.text.split(" ");
                    const wordDuration = currentBubble.duration / words.length;
                    const wordIndex = Math.floor((currentTime - currentBubble.offset) / wordDuration);
                    setHighlightedWord(wordIndex);
                }
            });

            wavesurfer.on("seek", (progress) => {
                const time = progress * wavesurfer.getDuration();
                handleAudioClick(time);
            });

            wavesurfer.on("pause", () => {
                const time = wavesurfer.getCurrentTime();
                handleAudioClick(time);
            });
        }
    }, [wavesurfer, selectedItem]);

    return (
        <>
            <div className="detail-container">
                <div className="left">
                    <UpperLeftSection
                        selectedItem={selectedItem}
                        wavesurfer={wavesurfer}
                        setWavesurfer={setWavesurfer}
                        isPlaying={isPlaying}
                        setIsPlaying={setIsPlaying}
                        volume={volume}
                        setVolume={setVolume}
                        currentTime={currentTime}
                        setCurrentTime={setCurrentTime}
                        totalTime={totalTime}
                        setTotalTime={setTotalTime}
                        audioPosition={audioPosition}
                        setAudioPosition={setAudioPosition}
                        loading={loading}
                        setLoading={setLoading}
                    />
                    <LowerLeftSection
                        selectedItem={selectedItem}
                        wavesurfer={wavesurfer}
                        setHighlightedBubble={setHighlightedBubble}
                        handleDialogClick={handleDialogClick} // Pass the handleDialogClick function
                    />
                </div>
                <div className="right" id="right-section">
                    <RightSection
                        selectedItem={selectedItem}
                        onBubbleClick={handleBubbleClick}
                        highlightedBubble={highlightedBubble}
                        highlightedWord={highlightedWord}
                        scrollToEnd={scrollToEnd}
                        expandedBubble={expandedBubble} // Pass expandedBubble state
                        setExpandedBubble={setExpandedBubble} // Pass setExpandedBubble function
                        currentTime={currentTime} // Pass currentTime state
                    />
                </div>
            </div>
        </>
    );
}

export default function AudioDetail() {
    const { client_id } = useParams();
    const { data } = useOutletContext();
    const audio = data.find((audio) => audio.id == client_id);
    const navigate = useNavigate();

    const [volume, setVolume] = useState(1); // Default volume
    const [currentTime, setCurrentTime] = useState(0);
    const [totalTime, setTotalTime] = useState(0);
    const [wavesurfer, setWavesurfer] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [highlightedBubble, setHighlightedBubble] = useState(null);
    const [highlightedWord, setHighlightedWord] = useState(null);
    const [audioPosition, setAudioPosition] = useState(0);
    const [expandedBubble, setExpandedBubble] = useState(null); // New state for expanded bubble



    return (
        <>
            <div className="audiodetail-main">
                <nav className="main-nav">
                    <p onClick={() => navigate("/")}>Home</p>
                </nav>
                <div className="audio-detail-container">
                    <AudioPlayer
                        selectedItem={audio}
                        volume={volume}
                        setVolume={setVolume}
                        currentTime={currentTime}
                        setCurrentTime={setCurrentTime}
                        totalTime={totalTime}
                        setTotalTime={setTotalTime}
                        wavesurfer={wavesurfer}
                        setWavesurfer={setWavesurfer}
                        isPlaying={isPlaying}
                        setIsPlaying={setIsPlaying}
                        highlightedBubble={highlightedBubble}
                        setHighlightedBubble={setHighlightedBubble}
                        highlightedWord={highlightedWord}
                        setHighlightedWord={setHighlightedWord}
                        audioPosition={audioPosition}
                        setAudioPosition={setAudioPosition}
                        expandedBubble={expandedBubble} // Pass expandedBubble state
                        setExpandedBubble={setExpandedBubble} // Pass setExpandedBubble function
                    />
                </div>
            </div>
        </>
    );
}
