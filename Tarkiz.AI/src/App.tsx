import React from 'react';
import TaskStats from './components/dashboard/TaskStats';
import ChatBot from './components/dashboard/ChatBot';
import RewardsBox from './components/dashboard/RewardsBox';
import TaskScheduler from './components/dashboard/TaskScheduler';
import MusicPlayer from './components/dashboard/MusicPlayer';
import TaskTimer from './components/dashboard/TaskTimer';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-transparent py-8">
      <div className="container mx-auto px-16">
        <div className="flex items-center mb-8">
          {/* Logo */}
          <img 
            src="/assets/logo.png" 
            alt="Tarkiz Logo" 
            className="h-25 w-40 mr-17" /* Increased size and spacing */
          />
          {/* Title */}
          <h1 className="text-5xl font-bold text-black neon-text">
            Tarkiz.ai
          </h1>
        </div>
        <div className="grid grid-cols-12 gap-6">
          {/* Left Column */}
          <div className="col-span-4 space-y-6">
            <TaskStats />
            <div className="chat-container h-96 overflow-y-auto border border-gray-300 rounded-lg p-4">
              <ChatBot />
            </div>
          </div>

          {/* Middle Column */}
          <div className="col-span-4 space-y-6">
            <TaskScheduler />
            <RewardsBox />
          </div>

          {/* Right Column */}
          <div className="col-span-4 space-y-6">
            <TaskTimer />
            <MusicPlayer />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
