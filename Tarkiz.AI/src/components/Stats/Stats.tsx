import React from 'react';

interface StatsProps {
  focusSessions: number;
  completedTasks: number;
}

export function Stats({ focusSessions, completedTasks }: StatsProps) {
  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
      <div className="text-center">
        <span className="block text-sm text-gray-500">Focus Sessions</span>
        <span className="text-2xl font-bold text-indigo-600">{focusSessions}</span>
      </div>
      <div className="text-center">
        <span className="block text-sm text-gray-500">Tasks Completed</span>
        <span className="text-2xl font-bold text-indigo-600">{completedTasks}</span>
      </div>
    </div>
  );
}