import { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';

interface AudioVisualizerProps {
  isPlaying: boolean;
  audioUrl: string;
  onReady: (duration: number) => void;
  onTimeUpdate: (currentTime: number) => void;
  onFinish: () => void;
}

function AudioVisualizer({ isPlaying, audioUrl, onReady, onTimeUpdate, onFinish }: AudioVisualizerProps) {
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<WaveSurfer | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  const [useFallback, setUseFallback] = useState(false);

  // Initialize and cleanup WaveSurfer
  useEffect(() => {
    let wavesurfer: WaveSurfer | null = null;
    let abortController: AbortController | null = null;

    const initWaveSurfer = async () => {
      if (!waveformRef.current) return;

      try {
        // Test audio availability
        const response = await fetch(audioUrl, { method: 'HEAD' });
        if (!response.ok) {
          setUseFallback(true);
          return;
        }

        // Create new WaveSurfer instance
        wavesurfer = WaveSurfer.create({
          container: waveformRef.current,
          waveColor: '#818CF8',
          progressColor: '#4F46E5',
          cursorColor: '#4F46E5',
          barWidth: 2,
          barGap: 3,
          height: 48,
          barRadius: 3,
          autoplay: false,
        });

        wavesurferRef.current = wavesurfer;
        abortController = new AbortController();

        // Set up event listeners
        wavesurfer.on('ready', () => {
          onReady(wavesurfer?.getDuration() || 0);
        });

        wavesurfer.on('audioprocess', () => {
          onTimeUpdate(wavesurfer?.getCurrentTime() || 0);
        });

        wavesurfer.on('finish', onFinish);

        wavesurfer.on('error', () => {
          setUseFallback(true);
          wavesurfer?.destroy();
        });

        // Load audio
        await wavesurfer.load(audioUrl);
      } catch (error) {
        console.error('WaveSurfer initialization error:', error);
        setUseFallback(true);
      }
    };

    initWaveSurfer();

    // Cleanup function
    return () => {
      abortController?.abort();
      if (wavesurferRef.current) {
        wavesurferRef.current.pause();
        wavesurferRef.current.destroy();
        wavesurferRef.current = null;
      }
    };
  }, [audioUrl]);

  // Handle play/pause
  useEffect(() => {
    if (useFallback) {
      if (audioRef.current) {
        if (isPlaying) {
          audioRef.current.play().catch(console.error);
        } else {
          audioRef.current.pause();
        }
      }
    } else {
      if (wavesurferRef.current) {
        if (isPlaying) {
          wavesurferRef.current.play().catch(console.error);
        } else {
          wavesurferRef.current.pause();
        }
      }
    }
  }, [isPlaying, useFallback]);

  // Fallback audio element handlers
  const handleFallbackTimeUpdate = () => {
    if (audioRef.current) {
      onTimeUpdate(audioRef.current.currentTime);
    }
  };

  const handleFallbackLoadedMetadata = () => {
    if (audioRef.current) {
      onReady(audioRef.current.duration);
    }
  };

  return (
    <div className="w-full rounded-lg bg-indigo-50 p-4">
      {useFallback ? (
        <div className="flex items-center justify-center h-12">
          <audio
            ref={audioRef}
            src={audioUrl}
            onTimeUpdate={handleFallbackTimeUpdate}
            onEnded={onFinish}
            onLoadedMetadata={handleFallbackLoadedMetadata}
          />
          <div className="h-2 w-full bg-indigo-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-600 transition-all duration-100"
              style={{
                width: `${((audioRef.current?.currentTime || 0) / (audioRef.current?.duration || 1)) * 100}%`
              }}
            />
          </div>
        </div>
      ) : (
        <div ref={waveformRef} />
      )}
    </div>
  );
}

export default AudioVisualizer;