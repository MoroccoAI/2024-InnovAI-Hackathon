import { motion, AnimatePresence } from 'framer-motion';

interface StoryVisualProps {
  scenes: string[];
  currentTime: number;
}

function StoryVisual({ scenes, currentTime }: StoryVisualProps) {
  const currentScene = Math.min(
    Math.floor(currentTime / 10),
    scenes.length - 1
  );

  return (
    <div className="relative aspect-video rounded-2xl overflow-hidden shadow-xl bg-gray-100">
      <AnimatePresence mode="wait">
        <motion.img
          key={currentScene}
          src={scenes[currentScene]}
          alt={`Scene ${currentScene + 1}`}
          className="w-full h-full object-cover"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        />
      </AnimatePresence>
    </div>
  );
}

export default StoryVisual;