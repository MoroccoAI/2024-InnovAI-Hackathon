import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Play, Pause, NotepadText as QuizIcon } from 'lucide-react';
import StoryCarousel from '../components/StoryCarousel';
import AudioPlayer from '../components/AudioPlayer';
import Transcript from '../components/Transcript';

function Story() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [story, setStory] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  const initializeData = async () => {
    try {
      const url = `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/story/get/${id}`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      const story = {
        id: data.data._id,
        title: data.data.title,
        audioUrl: data.data.audio,
        transcript: data.data.transcript,
        visualScenes: data.data.images,
        createdAt: data.data.createdAt
      }

      setStory(story)

      return story;
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  useEffect(() => {
    initializeData()
  }, []);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (time) => {
    setCurrentTime(time);
  };

  if (!story) {
    navigate('/');
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 pb-24"
    >
      <div className="max-w-lg mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold text-indigo-600 mb-6">
          {story.title}
        </h1>

        <div className="space-y-6">
          <StoryCarousel
            scenes={story.visualScenes}
            currentTime={currentTime}
            duration={duration}
            isPlaying={isPlaying}
            onPlayPause={handlePlayPause}
          />
          
          <AudioPlayer
            isPlaying={isPlaying}
            audioUrl={story.audioUrl}
            onReady={setDuration}
            onTimeUpdate={setCurrentTime}
            onFinish={() => setIsPlaying(false)}
            onSeek={handleSeek}
          />

          <div className="flex justify-center space-x-4">
            <button
              onClick={handlePlayPause}
              className="flex items-center space-x-2 bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-colors active:scale-95"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5" />
              ) : (
                <Play className="w-5 h-5" />
              )}
              <span>{isPlaying ? 'Pause' : 'Play'}</span>
            </button>
            <button
              onClick={() => navigate(`/quiz/${id}`)}
              className="flex items-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition-colors active:scale-95"
            >
              <QuizIcon className="w-5 h-5" />
              <span>Take Quiz</span>
            </button>
          </div>

          <Transcript text={story.transcript} />
        </div>
      </div>
    </motion.div>
  );
}

export default Story;