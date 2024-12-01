import { StateCreator } from 'zustand';
import { Task } from '../../types';
import { generateId } from '../../utils/helpers';

export interface TaskSlice {
  tasks: Task[];
  addTask: (title: string, priority: Task['priority']) => void;
  toggleTask: (id: string) => void;
}

export const createTaskSlice: StateCreator<TaskSlice> = (set) => ({
  tasks: [],
  
  addTask: (title, priority) => {
    const task = {
      id: generateId(),
      title,
      completed: false,
      createdAt: new Date(),
      priority
    };
    
    set((state) => ({
      tasks: [...state.tasks, task]
    }));

    chrome.storage.local.get(['tasks'], (result) => {
      const tasks = result.tasks || [];
      chrome.storage.local.set({ tasks: [...tasks, task] });
    });
  },

  toggleTask: (id) => {
    set((state) => ({
      tasks: state.tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    }));

    chrome.storage.local.get(['tasks'], (result) => {
      const tasks = result.tasks.map((task: Task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      );
      chrome.storage.local.set({ tasks });
    });
  }
});