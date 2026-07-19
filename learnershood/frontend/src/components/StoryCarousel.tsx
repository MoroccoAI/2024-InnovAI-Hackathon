import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Play } from 'lucide-react';
import { preloadImages } from '../utils/imageCache';

interface StoryCarouselProps {
  scenes: string[];
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  onPlayPause: () => void;
}

function StoryCarousel({ scenes, currentTime, duration, isPlaying, onPlayPause }: StoryCarouselProps) {
  const [currentScene, setCurrentScene] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadImages = async () => {
      try {
        await preloadImages(scenes);
        setIsLoading(false);
      } catch (error) {
        console.error('Error loading images:', error);
        setIsLoading(false);
      }
    };

    loadImages();
  }, [scenes]);

  useEffect(() => {
    if (duration) {
      const segmentDuration = duration / scenes.length;
      const newScene = Math.min(
        Math.floor(currentTime / segmentDuration),
        scenes.length - 1
      );
      setCurrentScene(newScene);
    }
  }, [currentTime, duration, scenes.length]);

  const nextScene = () => {
    setCurrentScene((prev) => (prev + 1) % scenes.length);
  };

  const prevScene = () => {
    setCurrentScene((prev) => (prev - 1 + scenes.length) % scenes.length);
  };

  return (
    <div className="relative aspect-[3/4] md:aspect-[4/3] rounded-2xl overflow-hidden shadow-xl bg-gray-100">
      <AnimatePresence mode="wait">
        <motion.img
          key={currentScene}
          src={scenes[currentScene]}
          alt={`Scene ${currentScene + 1}`}
          className="w-full h-full object-cover"
          initial={{ opacity: 0, scale: 1.1 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.5 }}
        />
      </AnimatePresence>

      {!isPlaying && (
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          onClick={onPlayPause}
          className="absolute inset-0 flex items-center justify-center bg-black/30 hover:bg-black/40 transition-colors group"
        >
          <div className="w-20 h-20 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform">
            <Play className="w-10 h-10 text-indigo-600 ml-2" />
          </div>
        </motion.button>
      )}

      <button
        onClick={prevScene}
        className="absolute left-4 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white/80 text-gray-800 hover:bg-white transition-colors"
      >
        <ChevronLeft className="w-6 h-6" />
      </button>

      <button
        onClick={nextScene}
        className="absolute right-4 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white/80 text-gray-800 hover:bg-white transition-colors"
      >
        <ChevronRight className="w-6 h-6" />
      </button>

      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {scenes.map((_, index) => (
          <div
            key={index}
            className={`w-2 h-2 rounded-full transition-all duration-300 ${
              index === currentScene ? 'bg-white w-4' : 'bg-white/50'
            }`}
          />
        ))}
      </div>
    </div>
  );
}

export default StoryCarousel;