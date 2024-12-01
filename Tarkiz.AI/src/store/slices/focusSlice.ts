import { StateCreator } from 'zustand';
import { FocusSession } from '../../types';
import { generateId } from '../../utils/helpers';

export interface FocusSlice {
  focusSessions: FocusSession[];
  currentSession: FocusSession | null;
  startFocusSession: (duration: number, taskId?: string) => void;
  endFocusSession: () => void;
}

export const createFocusSlice: StateCreator<FocusSlice> = (set) => ({
  focusSessions: [],
  currentSession: null,

  startFocusSession: (duration, taskId) => {
    const session = {
      id: generateId(),
      startTime: new Date(),
      duration,
      taskId,
      completed: false
    };

    set(() => ({ currentSession: session }));

    chrome.alarms.create(`focus_timer_${session.id}`, {
      delayInMinutes: duration
    });

    chrome.storage.local.set({ currentSession: session });
  },

  endFocusSession: () => {
    set((state) => {
      if (!state.currentSession) return state;
      const completedSession = { ...state.currentSession, completed: true };
      
      chrome.storage.local.get(['focusSessions'], (result) => {
        const focusSessions = result.focusSessions || [];
        chrome.storage.local.set({
          focusSessions: [...focusSessions, completedSession],
          currentSession: null
        });
      });

      return {
        focusSessions: [...state.focusSessions, completedSession],
        currentSession: null
      };
    });
  }
});