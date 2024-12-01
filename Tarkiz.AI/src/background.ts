// Handle notifications when focus timer ends
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name.startsWith('focus_timer_')) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Focus Session Complete',
      message: 'Great job! Take a short break before starting your next task.',
      priority: 2
    });
  }
});

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  // Set up initial storage state
  chrome.storage.local.set({
    tasks: [],
    focusSessions: [],
    currentSession: null
  });
});