import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mic, History } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import RecentStories from '../components/RecentStories';
import VoiceRecordModal from '../components/VoiceRecordModal';

function Home() {
  const [isRecordModalOpen, setIsRecordModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (query) => {
    if (query.trim()) {
      navigate(`/loading?query=${query.trim()}`);
    }
  };

  const handleTranscription = (text) => {
    setSearchQuery(text);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8 pb-24"
    >
      <div className="max-w-2xl mx-auto text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-bold text-indigo-600 mb-4">
          Learnershood
        </h1>
        <p className="text-xl text-gray-600">
          Discover the magic of African stories
        </p>
      </div>

      <div className="max-w-xl mx-auto mb-12">
        <SearchBar onSearch={handleSearch} value={searchQuery} onChange={setSearchQuery} />
        <button
          onClick={() => setIsRecordModalOpen(true)}
          className="mt-4 p-4 rounded-full bg-indigo-600 text-white mx-auto block transition-all hover:scale-110"
        >
          <Mic className="w-6 h-6" />
        </button>
      </div>

      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
          <History className="w-6 h-6 mr-2" />
          Recent Stories
        </h2>
        <RecentStories />
      </div>

      <VoiceRecordModal
        isOpen={isRecordModalOpen}
        onClose={() => setIsRecordModalOpen(false)}
        onTranscription={handleTranscription}
      />
    </motion.div>
  );
}

export default Home;