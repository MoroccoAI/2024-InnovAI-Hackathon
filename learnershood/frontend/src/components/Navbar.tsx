import { Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, Menu } from 'lucide-react';
import { motion } from 'framer-motion';

function Navbar() {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <motion.nav
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      className="fixed bottom-0 left-0 right-0 bg-white shadow-lg border-t border-gray-100 pb-safe z-50"
    >
      <div className="flex justify-around items-center h-4 mt-5">
        <Link
          to="/"
          className={`flex flex-col items-center space-y-1 px-6 py-2 ${
            isActive('/') ? 'text-indigo-600' : 'text-gray-600'
          }`}
        >
          <Home className="w-6 h-6" />
          <span className="text-xs">Home</span>
        </Link>

        <Link
          to="/explore"
          className={`flex flex-col items-center space-y-1 px-6 py-2 ${
            isActive('/explore') ? 'text-indigo-600' : 'text-gray-600'
          }`}
        >
          <BookOpen className="w-6 h-6" />
          <span className="text-xs">Explore</span>
        </Link>
      </div>
    </motion.nav>
  );
}

export default Navbar;