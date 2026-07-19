import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Explore() {
  const [searchQuery, setSearchQuery] = useState('');
  const [stories, setStories] = useState([]);

  const filteredStories = stories.filter(story =>
    story.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const initializeData = async () => {
    try {
      const url = `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/story/get`;

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

      const allStories = data.data.map((story) => {
        return {
          ...story,
          thumbnail: story.images[0],
          description: story.transcript.slice(0, 130),
          duration: "3 mins"
        }
      })

      setStories(allStories)

      return allStories;
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  useEffect(() => {
    initializeData()
  }, [])
  

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8"
    >
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold text-indigo-600 mb-8">
          Explore Stories
        </h1>

        <div className="relative mb-8">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search stories..."
            className="w-full px-6 py-4 text-lg rounded-full border-2 border-indigo-200 focus:border-indigo-600 focus:outline-none shadow-lg pr-12"
          />
          <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-400" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredStories.map((story) => (
            <Link key={story._id} to={`/story/${story._id}`}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="bg-white rounded-xl shadow-lg overflow-hidden cursor-pointer"
              >
                <div className="relative h-48">
                  <img
                    src={story.thumbnail}
                    alt={story.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
                    <span className="text-white text-sm">{story.duration}</span>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    {story.title}
                  </h3>
                  <p className="text-gray-600">{story.description}</p>
                </div>
              </motion.div>
            </Link>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

export default Explore;