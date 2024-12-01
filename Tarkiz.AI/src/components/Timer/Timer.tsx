import React from 'react';
import { useTimer } from '../../hooks/useTimer';

export function Timer() {
  const { minutes, seconds, isRunning, toggleTimer, resetTimer } = useTimer(25);

  return (
    <div className="text-center mb-6">
      <div className="text-6xl font-bold text-gray-800 mb-4">
        {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
      </div>
      <div className="flex gap-2 justify-center">
        <button
          onClick={toggleTimer}
          className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
        >
          {isRunning ? 'Pause' : 'Start'}
        </button>
        <button
          onClick={resetTimer}
          className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
        >
          Reset
        </button>
      </div>
    </div>
  );
}