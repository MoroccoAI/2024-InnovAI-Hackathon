import { useEffect, useState, useRef } from 'react'
import { icons } from '@renderer/constants/icons'
import StreamVideo from './StreamVideo'
import Transcription from './Transcription'
import { VideoPLayerProps } from '@renderer/types/types'
import type { YouTubePlayer } from 'react-youtube'

const VideoPlayer: React.FC<VideoPLayerProps> = ({ videoStreamlink, linkType }) => {
  const [player, setPlayer] = useState<YouTubePlayer | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(100)
  const [showTranscription, setShowTranscription] = useState(true)
  const [isLoading, setIsLoading] = useState(true)
  const containerRef = useRef<HTMLDivElement>(null)
  const [currentID, setId] = useState<string>(videoStreamlink)

  useEffect(() => {
    setId(videoStreamlink)
  }, [videoStreamlink])
  useEffect(() => {
    if (player) {
      const timeUpdateInterval = setInterval(() => {
        const time = player.getCurrentTime()
        const dur = player.getDuration()
        setCurrentTime(Number(time))
        setDuration(Number(dur))
      }, 1000)

      return () => clearInterval(timeUpdateInterval)
    }
  }, [player])

  useEffect(() => {
    const checkTranscription = () => {
      const savedTranscription = localStorage.getItem(`transcription_${currentID}`)
      if (!savedTranscription) {
        setIsLoading(true)
      } else {
        setIsLoading(false)
      }
    }

    checkTranscription()
    const interval = setInterval(checkTranscription, 1000)
    return () => clearInterval(interval)
  }, [currentID])

  const handlePlayerReady = (player: YouTubePlayer) => {
    setPlayer(player)
    setDuration(player.getDuration())
  }

  const handleStateChange = (event: { data: number }) => {
    setIsPlaying(event.data === 1)
  }

  const togglePlay = () => {
    if (isPlaying) {
      player?.pauseVideo()
    } else {
      player?.playVideo()
    }
    setIsPlaying(!isPlaying)
  }

  const toggleMute = () => {
    if (isMuted) {
      player?.unMute()
      player?.setVolume(volume)
    } else {
      player?.mute()
    }
    setIsMuted(!isMuted)
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseInt(e.target.value)
    setVolume(newVolume)
    player?.setVolume(newVolume)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = Number(e.target.value)
    player?.seekTo(time, true)
    setCurrentTime(time)
  }

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = Math.floor(seconds % 60)
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const toggleFullScreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen()
    } else {
      document.exitFullscreen()
    }
  }
  const IsLoading = () => {
    return (
      <div className="relative container w-[600px] h-[400px] bg-black flex items-center justify-center">
        <div className="text-white">Loading transcription...</div>
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      className="relative container w-[600px] h-[400px] bg-black group rouneded-md border-2 border-orange-500 lg:w-[900px] lg:h-[600px] xl:w-[1200px] xl:h-[800px]"
    >
      {isLoading ? (
        <IsLoading />
      ) : (
        <StreamVideo
          videoStreamlink={videoStreamlink}
          linkType={linkType}
          onPlayerReady={handlePlayerReady}
          onStateChange={handleStateChange}
        />
      )}

      <div className="absolute bottom-0 left-0 right-0 transition-opacity duration-300 opacity-0 group-hover:opacity-100">
        <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/90 via-black/50 to-transparent">
          <div className="flex flex-col gap-3">
            <div className="relative w-full h-1 cursor-pointer group/progress">
              <input
                type="range"
                min={0}
                max={duration}
                value={currentTime}
                onChange={handleSeek}
                className="absolute z-10 w-full h-1 opacity-0 cursor-pointer"
              />
              <div className="absolute w-full h-1 bg-gray-600 rounded-full">
                <div
                  className="absolute h-full bg-red-500 rounded-full"
                  style={{ width: `${(currentTime / duration) * 100}%` }}
                />
              </div>
              <div
                className="absolute w-3 h-3 transition-opacity -translate-y-1 bg-red-500 rounded-full opacity-0 group-hover/progress:opacity-100"
                style={{ left: `${(currentTime / duration) * 100}%` }}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <button
                  onClick={togglePlay}
                  className="p-1 text-white transition-colors hover:text-red-500"
                >
                  {isPlaying ? icons.PauseIcon() : icons.PlayIcon()}
                </button>

                <div className="flex items-center gap-2 group/volume">
                  <button
                    onClick={toggleMute}
                    className="p-1 text-white transition-colors hover:text-red-500"
                  >
                    {isMuted ? icons.MuteIcon() : icons.VolumeIcon()}
                  </button>
                  <div className="w-0 overflow-hidden transition-all duration-300 group-hover/volume:w-20">
                    <input
                      type="range"
                      min={0}
                      max={100}
                      value={volume}
                      onChange={handleVolumeChange}
                      className="w-20 accent-red-500"
                    />
                  </div>
                </div>

                <button
                  onClick={() => setShowTranscription(!showTranscription)}
                  className={`p-1 transition-colors ${
                    showTranscription ? 'text-red-500' : 'text-white hover:text-red-500'
                  }`}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    <line x1="9" y1="10" x2="15" y2="10" />
                    <line x1="9" y1="14" x2="15" y2="14" />
                  </svg>
                </button>

                <button
                  onClick={toggleFullScreen}
                  className="p-1 text-white transition-colors hover:text-red-500"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3" />
                  </svg>
                </button>

                <span className="text-sm font-medium text-white">
                  {formatTime(currentTime)} / {formatTime(duration)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {showTranscription && <Transcription currentTime={currentTime} id={currentID} />}
    </div>
  )
}

export default VideoPlayer
