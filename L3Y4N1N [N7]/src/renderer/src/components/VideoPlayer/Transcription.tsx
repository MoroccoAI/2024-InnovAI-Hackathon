import { useTranscription } from "@renderer/hooks/useTranscription";
import getTranscription from "@renderer/services/GetTranscription";
import { useEffect, useState } from "react";
import getDef from "@renderer/services/getDef";
import getSynAnt from "@renderer/services/GetSynAnt";
interface TranscriptionProps {
  currentTime: number
  id: string
}

const Transcription: React.FC<TranscriptionProps> = ({ currentTime, id }) => {
  const [transcriptionJSON, setTranscriptionJSON] = useState<JSON>()
  useEffect(() => {
    const storedTranscription = localStorage.getItem(`transcription_${id}`)
    if (storedTranscription) {
      setTranscriptionJSON(JSON.parse(storedTranscription))
    } else {
      setTranscriptionJSON(undefined)
      getTranscription(id).then((res) => {
        setTranscriptionJSON(res)
        localStorage.setItem(`transcription_${id}`, JSON.stringify(res))
      })
    }
  }, [id])
  const transcription = useTranscription(currentTime, transcriptionJSON)
  return (
    <div className="absolute transform -translate-x-1/2 bottom-20 left-1/2">
      <div className="px-4 py-2 text-lg text-white bg-black rounded bg-opacity-70">
        <p className="text-center select-text ">{transcription}</p>
      </div>
    </div>
  )
}

export default Transcription
