import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { getRecentStories } from '../utils/storage';
import { useEffect, useState } from 'react';
import { preloadImages } from '../utils/imageCache';

function RecentStories() {
  const [stories, setStories] = useState([]);

  useEffect(() => {
    const loadStories = async () => {
      const recentStories = getRecentStories();
      setStories(recentStories);

      // Preload thumbnails in the background
      const thumbnails = recentStories.map(story => story.images[0]);
      preloadImages(thumbnails).catch(console.error);
    };

    loadStories();
  }, []);

  if (stories.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No stories yet. Start exploring to create your first story!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {stories.map((story) => (
        <Link key={story._id} to={`/story/${story._id}`}>
          <motion.div
            whileTap={{ scale: 0.98 }}
            className="bg-white rounded-xl shadow-md overflow-hidden cursor-pointer"
          >
            <div className="flex items-center p-3">
              <div className="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                <img
                  src={story.images[0]}
                  alt={story.title}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="ml-4 flex-grow">
                <h3 className="text-lg font-semibold text-gray-800">{story.title}</h3>
                <span className="text-sm text-gray-500">
                  {new Date(story.createdAt).toLocaleDateString()}
                </span>
              </div>
            </div>
          </motion.div>
        </Link>
      ))}
    </div>
  );
}

export default RecentStories;