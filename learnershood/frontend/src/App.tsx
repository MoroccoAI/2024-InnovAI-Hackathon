import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Home from './pages/Home';
import Loading from './pages/Loading';
import Story from './pages/Story';
import Quiz from './pages/Quiz';
import Explore from './pages/Explore';
import Navbar from './components/Navbar';
import InstallPrompt from './components/InstallPrompt';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
        <Navbar />
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/loading" element={<Loading />} />
            <Route path="/story/:id" element={<Story />} />
            <Route path="/quiz/:id" element={<Quiz />} />
            <Route path="/explore" element={<Explore />} />
          </Routes>
        </AnimatePresence>
        <InstallPrompt />
      </div>
    </Router>
  );
}

export default App;