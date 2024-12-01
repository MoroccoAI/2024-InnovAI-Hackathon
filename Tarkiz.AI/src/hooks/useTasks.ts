import { useState } from 'react';
import { useStorage } from './useStorage';

interface Task {
  id: number;
  text: string;
  completed: boolean;
}

export function useTasks() {
  const { tasks, saveTasks } = useStorage();
  const [newTask, setNewTask] = useState('');

  const addTask = () => {
    if (newTask.trim()) {
      const updatedTasks = [
        { id: Date.now(), text: newTask, completed: false },
        ...tasks
      ];
      saveTasks(updatedTasks);
      setNewTask('');
    }
  };

  const toggleTask = (id: number) => {
    const updatedTasks = tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    );
    saveTasks(updatedTasks);
  };

  const deleteTask = (id: number) => {
    const updatedTasks = tasks.filter(task => task.id !== id);
    saveTasks(updatedTasks);
  };

  return {
    tasks,
    newTask,
    setNewTask,
    addTask,
    toggleTask,
    deleteTask
  };
}