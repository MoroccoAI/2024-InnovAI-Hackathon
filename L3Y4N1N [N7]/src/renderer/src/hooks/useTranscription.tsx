import { useEffect, useState, useMemo } from "react";

interface TranscriptionSegment {
  start: number;
  end: number;
  text: string;
}

function useTranscription(currentTime: number, transcriptionJSON: any): string {
    const [transcriptionData, setTranscriptionData] = useState<TranscriptionSegment[]>([]);
        
    useEffect(() => {
      if (transcriptionJSON) {
        try {
          const segments = transcriptionJSON.segments || [];
          setTranscriptionData(segments);
        } catch (error) {
          console.error('Error parsing transcription:', error);
          setTranscriptionData([]);
        }
      }
    }, [transcriptionJSON]);

    const currentTranscription = useMemo(() => {
        return transcriptionData.find(
            t => currentTime >= t.start && currentTime <= t.end
        );
    }, [transcriptionData, currentTime]);

    return currentTranscription?.text ?? '';
}

export { useTranscription };