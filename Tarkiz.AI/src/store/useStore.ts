import { create } from 'zustand';
import { TaskSlice, createTaskSlice } from './slices/taskSlice';
import { FocusSlice, createFocusSlice } from './slices/focusSlice';

type Store = TaskSlice & FocusSlice;

export const useStore = create<Store>((...args) => ({
  ...createTaskSlice(...args),
  ...createFocusSlice(...args)
}));