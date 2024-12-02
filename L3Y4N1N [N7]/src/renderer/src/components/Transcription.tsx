// Transcription.tsx
import React from 'react'

interface TranscriptionProps {
  text: string // The text to display as a transcription
}

const Transcription: React.FC<TranscriptionProps> = ({ text }) => {
  return (
    <div>
      <h3>Transcription</h3>
      <p>{text}</p>
    </div>
  )
}

export default Transcription
