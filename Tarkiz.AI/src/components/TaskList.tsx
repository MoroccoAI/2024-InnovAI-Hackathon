import React from 'react';
import { useStore } from '../store/useStore';
import TaskItem from './TaskItem';

export default function TaskList() {
  const tasks = useStore((state) => state.tasks);
  
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">Tasks</h2>
      <div className="space-y-2">
        {tasks.map((task) => (
          <TaskItem key={task.id} task={task} />
        ))}
        {tasks.length === 0 && (
          <p className="text-gray-500 text-sm">No tasks yet. Add one to get started!</p>
        )}
      </div>
    </div>
  );
}