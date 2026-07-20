export default function SentimentOverAudio({ selectedItem, wavesurfer, isUpperLeft }) {
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
                                className="sentiment-audio-dialog-block"
                                style={{
                                    left: `${(dialog.offset / maxTime) * 100}%`,
                                    width: `${(dialog.duration / maxTime) * 100}%`,
                                    backgroundColor: isUpperLeft
                                        ? speaker === "Client"
                                            ? "#0084ff"
                                            : "#c35151"
                                        : dialog.sentiment === "positif"
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
