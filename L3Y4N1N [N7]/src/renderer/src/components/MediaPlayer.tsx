import React from 'react'

interface MediaPlayerProps {
  src: string // The source of the media (audio or video)
}

const MediaPlayer: React.FC<MediaPlayerProps> = ({ src }) => {
  return (
    <div
      style={{
        backgroundColor: '#000', // Black background for the placeholder
        width: '100%',
        maxWidth: '600px', // Set max width for the media player
        height: '300px', // Fixed height for media player
        borderRadius: '10px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white', // White text color inside the player placeholder
        fontSize: '20px'
      }}
    >
      <p>Media Player Placeholder</p>
    </div>
  )
}

export default MediaPlayer
