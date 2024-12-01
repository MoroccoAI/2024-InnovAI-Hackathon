import React from 'react';
import { Task } from '../types';
import { useStore } from '../store/useStore';
import { formatTime } from '../utils/helpers';

interface TaskItemProps {
  task: Task;
}

export default function TaskItem({ task }: TaskItemProps) {
  const toggleTask = useStore((state) => state.toggleTask);
  const startFocusSession = useStore((state) => state.startFocusSession);

  const priorityColors = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800'
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm">
      <div className="flex items-center space-x-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => toggleTask(task.id)}
          className="h-4 w-4 text-indigo-600 rounded"
        />
        <div>
          <p className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </p>
          <p className="text-xs text-gray-500">{formatTime(task.createdAt)}</p>
        </div>
      </div>
      <div className="flex items-center space-x-2">
        <span className={`px-2 py-1 rounded-full text-xs ${priorityColors[task.priority]}`}>
          {task.priority}
        </span>
        <button
          onClick={() => startFocusSession(25, task.id)}
          className="px-3 py-1 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          Focus
        </button>
      </div>
    </div>
  );
}