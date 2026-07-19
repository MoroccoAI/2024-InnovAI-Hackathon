import { useEffect, useRef } from 'react';

interface AudioPlayerProps {
  isPlaying: boolean;
  audioUrl: string;
  onReady: (duration: number) => void;
  onTimeUpdate: (currentTime: number) => void;
  onFinish: () => void;
  onSeek?: (time: number) => void;
}

function AudioPlayer({ isPlaying, audioUrl, onReady, onTimeUpdate, onFinish, onSeek }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    // Preload audio when component mounts
    if (audioRef.current) {
      audioRef.current.load();
    }
  }, [audioUrl]);

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        const playPromise = audioRef.current.play();
        if (playPromise !== undefined) {
          playPromise.catch(error => {
            console.error('Error playing audio:', error);
          });
        }
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current) return;

    const bounds = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - bounds.left;
    const width = bounds.width;
    const percentage = x / width;
    const newTime = percentage * audioRef.current.duration;

    audioRef.current.currentTime = newTime;
    onSeek?.(newTime);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="w-full rounded-lg bg-indigo-50 p-4">
      <audio
        ref={audioRef}
        src={audioUrl}
        preload="auto"
        onTimeUpdate={() => audioRef.current && onTimeUpdate(audioRef.current.currentTime)}
        onEnded={onFinish}
        onLoadedMetadata={() => audioRef.current && onReady(audioRef.current.duration)}
      />
      <div 
        className="h-2 w-full bg-indigo-200 rounded-full overflow-hidden cursor-pointer"
        onClick={handleSeek}
      >
        <div
          className="h-full bg-indigo-600 transition-all duration-100"
          style={{
            width: `${((audioRef.current?.currentTime || 0) / (audioRef.current?.duration || 1)) * 100}%`
          }}
        />
      </div>
      <div className="flex justify-between mt-2 text-sm text-gray-600">
        <span>{formatTime(audioRef.current?.currentTime || 0)}</span>
        <span>{formatTime(audioRef.current?.duration || 0)}</span>
      </div>
    </div>
  );
}

export default AudioPlayer;