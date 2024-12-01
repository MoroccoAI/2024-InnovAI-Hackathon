import React, { useState } from 'react';
import { CalendarIcon, PlusIcon } from '@heroicons/react/24/outline';
import { format } from 'date-fns';

interface ScheduledTask {
  id: string;
  title: string;
  time: string;
  priority: 'low' | 'medium' | 'high';
}

export default function TaskScheduler() {
  const [tasks] = useState<ScheduledTask[]>([
    { id: '1', title: 'Team Meeting', time: '10:00 AM', priority: 'high' },
    { id: '2', title: 'Project Review', time: '2:00 PM', priority: 'medium' },
    { id: '3', title: 'Daily Planning', time: '4:30 PM', priority: 'low' },
  ]);

  const priorityColors = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800',
  };

  return (
    <div className="dashboard-card p-6 h-[450px]">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold neon-text">Task Scheduler</h2>
        <div className="flex items-center space-x-2">
          <span className="text-gray-300">{format(new Date(), 'MMMM d, yyyy')}</span>
          <CalendarIcon className="h-5 w-5 text-neon-green" />
        </div>
      </div>
      
      <div className="space-y-4 h-[calc(100%-4rem)] overflow-y-auto">
        {tasks.map((task) => (
          <div key={task.id} className="flex items-center justify-between p-3 bg-opacity-10 bg-white backdrop-blur-md rounded-lg border border-gray-700">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 rounded-full bg-neon-green"></div>
              <div>
                <p className="font-medium text-white">{task.title}</p>
                <p className="text-sm text-gray-300">{task.time}</p>
              </div>
            </div>
            <span className={`px-2 py-1 rounded-full text-xs ${priorityColors[task.priority]}`}>
              {task.priority}
            </span>
          </div>
        ))}
        <button className="flex items-center justify-center w-full p-2 text-neon-green hover:bg-white hover:bg-opacity-5 rounded-lg transition-colors border border-neon-green">
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Task
        </button>
      </div>
    </div>
  );
}