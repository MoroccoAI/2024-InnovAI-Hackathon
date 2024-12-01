import { useState, useEffect } from 'react';

interface Storage {
  tasks: Task[];
  profile: Profile;
  focusSessions: number;
}

const defaultStorage: Storage = {
  tasks: [],
  profile: {
    name: '',
    focusDuration: 25,
    breakDuration: 5,
    theme: 'light'
  },
  focusSessions: 0
};

export function useStorage() {
  const [storage, setStorage] = useState<Storage>(defaultStorage);

  useEffect(() => {
    const loadStorage = async () => {
      const data = await chrome.storage.sync.get(null);
      setStorage({ ...defaultStorage, ...data });
    };
    loadStorage();
  }, []);

  const saveTasks = async (tasks: Task[]) => {
    await chrome.storage.sync.set({ tasks });
    setStorage(prev => ({ ...prev, tasks }));
  };

  const saveProfile = async (profile: Profile) => {
    await chrome.storage.sync.set({ profile });
    setStorage(prev => ({ ...prev, profile }));
  };

  const incrementFocusSessions = async () => {
    const newCount = storage.focusSessions + 1;
    await chrome.storage.sync.set({ focusSessions: newCount });
    setStorage(prev => ({ ...prev, focusSessions: newCount }));
  };

  return {
    ...storage,
    saveTasks,
    saveProfile,
    incrementFocusSessions
  };
}