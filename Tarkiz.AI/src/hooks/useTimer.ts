import { useState, useEffect } from 'react';
import { useStorage } from './useStorage';

export function useTimer(initialMinutes: number) {
  const [minutes, setMinutes] = useState(initialMinutes);
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const { incrementFocusSessions } = useStorage();

  useEffect(() => {
    let interval: number;

    if (isRunning) {
      interval = setInterval(() => {
        if (seconds === 0) {
          if (minutes === 0) {
            setIsRunning(false);
            incrementFocusSessions();
            return;
          }
          setMinutes(minutes - 1);
          setSeconds(59);
        } else {
          setSeconds(seconds - 1);
        }
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isRunning, minutes, seconds]);

  const toggleTimer = () => setIsRunning(!isRunning);
  
  const resetTimer = () => {
    setMinutes(initialMinutes);
    setSeconds(0);
    setIsRunning(false);
  };

  return { minutes, seconds, isRunning, toggleTimer, resetTimer };
}