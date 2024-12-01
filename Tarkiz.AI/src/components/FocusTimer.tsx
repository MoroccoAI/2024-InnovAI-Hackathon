import React, { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';

export default function FocusTimer() {
  const currentSession = useStore((state) => state.currentSession);
  const endFocusSession = useStore((state) => state.endFocusSession);
  const [timeLeft, setTimeLeft] = useState(0);

  useEffect(() => {
    if (!currentSession) return;

    const endTime = new Date(currentSession.startTime.getTime() + currentSession.duration * 60000);
    const updateTimer = () => {
      const now = new Date();
      const diff = Math.max(0, Math.floor((endTime.getTime() - now.getTime()) / 1000));
      setTimeLeft(diff);

      if (diff === 0) {
        endFocusSession();
      }
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  }, [currentSession, endFocusSession]);

  if (!currentSession) return null;

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  return (
    <div className="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">Focus Session</h3>
      <div className="text-3xl font-mono text-indigo-600">
        {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
      </div>
      <button
        onClick={endFocusSession}
        className="mt-2 w-full px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700"
      >
        End Session
      </button>
    </div>
  );
}