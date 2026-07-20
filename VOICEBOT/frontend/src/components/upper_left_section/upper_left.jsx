import { Fragment, useState, useMemo, useEffect } from "react";
import WavesurferPlayer from "@wavesurfer/react";
import Timeline from "wavesurfer.js/dist/plugins/timeline.esm.js";
import { FaPlay, FaPause, FaForward, FaBackward } from "react-icons/fa";
import ButtonContainer from "../container_buttons/container_buttons";
import SentimentOverAudio from "../lower_left_section/sentiment_audio";
import LowerLeftSection from "../lower_left_section/lower_left";
import "./upper_left.css";

export default function UpperLeftSection({
    selectedItem,
    wavesurfer,
    setWavesurfer,
    isPlaying,
    setIsPlaying,
    volume,
    setVolume,
    currentTime,
    setCurrentTime,
    totalTime,
    setTotalTime,
    audioPosition,
    setAudioPosition,
    highlightedBubble,
    setHighlightedBubble,
}) {
    const [activeContainer, setActiveContainer] = useState("Audio");
    const topTimeline = Timeline.create({
        insertPosition: "beforebegin",
        height: 10,
        timeInterval: 50,
        primaryLabelInterval: 10,
        style: {
            fontSize: "10px",
            color: "#c35151",
        },
    });

    function onReady(wavesurferInstance) {
        setWavesurfer(wavesurferInstance);
        setIsPlaying(false);

        // Set total time on ready
        const duration = wavesurferInstance.getDuration();
        setTotalTime(duration);

        // Update current time and audio position as audio plays
        wavesurferInstance.on("audioprocess", () => {
            const currentTime = wavesurferInstance.getCurrentTime();
            setCurrentTime(currentTime);
            setAudioPosition(currentTime);
        });

        // Synchronize the audio slider with the audio position when clicking somewhere on the audio
        wavesurferInstance.on("seek", (progress) => {
            const newPosition = progress * totalTime;
            setCurrentTime(newPosition);
            setAudioPosition(newPosition);
        });

        // Reset current time when playback ends
        wavesurferInstance.on("finish", () => {
            setIsPlaying(false);
            setCurrentTime(0);
            setAudioPosition(0);
        });
    }

    function onPlayPause() {
        if (wavesurfer) {
            wavesurfer.playPause();
            setIsPlaying((prev) => !prev);
        }
    }

    function goBack() {
        if (wavesurfer) {
            wavesurfer.skip(-10);
            const newPosition = wavesurfer.getCurrentTime();
            setCurrentTime(newPosition);
            setAudioPosition(newPosition);
        }
    }

    function goForward() {
        if (wavesurfer) {
            wavesurfer.skip(10);
            const newPosition = wavesurfer.getCurrentTime();
            setCurrentTime(newPosition);
            setAudioPosition(newPosition);
        }
    }

    function handleVolumeChange(event) {
        const newVolume = event.target.value;
        setVolume(newVolume);
        if (wavesurfer) {
            wavesurfer.setVolume(newVolume);
        }
    }

    function handleAudioPositionChange(event) {
        const newPosition = event.target.value;
        setAudioPosition(newPosition);
        if (wavesurfer) {
            wavesurfer.seekTo(newPosition / totalTime);
        }

        // Highlight the corresponding chat bubble
        const transcription = selectedItem.transcriptions.find(
            (t) => newPosition >= t.offset && newPosition <= t.offset + t.duration
        );
        // if (transcription) {
        //     setHighlightedBubble(transcription.offset);
        // }
    }

    // Format time in mm:ss
    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }

    const [loading, setLoading] = useState(false);

    function sleep(ms) {
        setLoading(true);
        Promise((resolve) => setTimeout(resolve, ms));
        setLoading(false);
    }

    return (
        <>
            <div className="upper-left">
                <div className="buttons-container">
                    <ButtonContainer
                        activeContainer={activeContainer === "Audio"}
                        setActiveContainer={setActiveContainer}
                        name="Audio"
                    />
                </div>
                {activeContainer == "Audio" && (
                    <div>
                        <div className="wavesurfer-container">
                            <WavesurferPlayer
                                height={100}
                                waveColor="gray"
                                progressColor="#c35151"
                                url={selectedItem.audio_path}
                                onReady={onReady}
                                onPlay={() => setIsPlaying(true)}
                                onPause={() => setIsPlaying(false)}
                                barWidth={9}
                                barGap={1}
                                barRadius={50}
                                cursorColor="white"
                                plugins={useMemo(() => [topTimeline], [])}
                            />
                        </div>

                        <SentimentOverAudio
                            selectedItem={selectedItem}
                            wavesurfer={wavesurfer}
                            isUpperLeft={true}
                            highlightedBubble={highlightedBubble}
                        />

                        <div className="audio-position-control">
                            <input
                                type="range"
                                min="0"
                                max={totalTime}
                                step="0.01"
                                value={audioPosition}
                                onChange={handleAudioPositionChange}
                                className="audio-position-slider"
                            />
                        </div>

                        <div className="controls-container">
                            <div className="time-display">
                                <span>{formatTime(currentTime)}</span>/ <span>{formatTime(totalTime)}</span>
                            </div>
                            <div className="audio-controls">
                                <button onClick={goBack} className="audio-button">
                                    <FaBackward />
                                </button>
                                <button onClick={onPlayPause} className="audio-button">
                                    {isPlaying ? <FaPause /> : <FaPlay />}
                                </button>
                                <button onClick={goForward} className="audio-button">
                                    <FaForward />
                                </button>
                            </div>
                            <div className="volume-control">
                                <label htmlFor="volume" className="volume-label">
                                    Volume
                                </label>
                                <input
                                    id="volume"
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                    value={volume}
                                    onChange={handleVolumeChange}
                                    className="volume-slider"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
