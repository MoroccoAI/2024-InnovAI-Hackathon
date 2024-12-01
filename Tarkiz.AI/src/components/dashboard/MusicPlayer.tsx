import React, { useState } from 'react';
import { PlayIcon, PauseIcon, ForwardIcon, BackwardIcon } from '@heroicons/react/24/solid';

const playlists = [
  { id: '1', name: 'Deep Focus', duration: '2:30:00' },
  { id: '2', name: 'Ambient Music', duration: '1:45:00' },
  { id: '3', name: 'Nature Sounds', duration: '1:00:00' },
];

export default function MusicPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrack, setCurrentTrack] = useState(playlists[0]);

  return (
    <div className="dashboard-card p-6 h-[400px]">
      <h2 className="text-xl font-semibold mb-4 neon-text">Focus Music</h2>
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium text-white">{currentTrack.name}</h3>
            <p className="text-sm text-gray-300">{currentTrack.duration}</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="text-gray-300 hover:text-neon-green">
              <BackwardIcon className="h-5 w-5" />
            </button>
            <button 
              className="bg-neon-green bg-opacity-10 text-neon-green p-2 rounded-full hover:bg-opacity-20 transition-colors"
              onClick={() => setIsPlaying(!isPlaying)}
            >
              {isPlaying ? (
                <PauseIcon className="h-5 w-5" />
              ) : (
                <PlayIcon className="h-5 w-5" />
              )}
            </button>
            <button className="text-gray-300 hover:text-neon-green">
              <ForwardIcon className="h-5 w-5" />
            </button>
          </div>
        </div>

        <div className="space-y-2">
          <div className="bg-gray-700 rounded-full h-1">
            <div className="bg-neon-green h-1 rounded-full w-1/3"></div>
          </div>
          <div className="flex justify-between text-xs text-gray-300">
            <span>1:15</span>
            <span>{currentTrack.duration}</span>
          </div>
        </div>

        <div className="space-y-2 mt-6">
          {playlists.map((playlist) => (
            <button
              key={playlist.id}
              onClick={() => setCurrentTrack(playlist)}
              className={`w-full text-left p-2 rounded-lg transition-colors ${
                currentTrack.id === playlist.id
                  ? 'bg-neon-green bg-opacity-10 text-neon-green border border-neon-green'
                  : 'text-white hover:bg-white hover:bg-opacity-5'
              }`}
            >
              {playlist.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}