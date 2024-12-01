import { useState, useEffect } from 'react';
import { useStorage } from './useStorage';

interface Profile {
  name: string;
  focusDuration: number;
  breakDuration: number;
  theme: string;
}

export function useProfile() {
  const { profile: storedProfile, saveProfile } = useStorage();
  const [profile, setProfile] = useState<Profile>(storedProfile);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setProfile(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    saveProfile(profile);
  };

  return { profile, handleChange, handleSubmit };
}