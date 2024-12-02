import React, { useRef } from 'react'
import YouTube, { YouTubeProps, YouTubePlayer } from 'react-youtube'

interface StreamVideoProps {
  videoStreamlink: string
  onPlayerReady: (player: YouTubePlayer) => void
  onStateChange: YouTubeProps['onStateChange']
}

const StreamVideo: React.FC<StreamVideoProps> = ({
  videoStreamlink,
  onPlayerReady,
  onStateChange
}) => {
  const playerRef = useRef<YouTubePlayer | null>(null)

  const opts: YouTubeProps['opts'] = {
    height: '100%',
    width: '100%',
    playerVars: {
      autoplay: 1,
      controls: 0,
      cc_load_policy: 0,
      mute: 0
    }
  }

  const handleReady: YouTubeProps['onReady'] = (event) => {
    playerRef.current = event.target
    event.target.unMute()
    onPlayerReady(event.target)
  }

  return (
    <div className="w-full h-full">
      <YouTube
        className="w-full h-full"
        videoId={videoStreamlink}
        opts={opts}
        onReady={handleReady}
        onStateChange={onStateChange}
      />
    </div>
  )
}

export default StreamVideo
