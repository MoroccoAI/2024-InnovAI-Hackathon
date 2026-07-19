// Local storage keys
export const STORAGE_KEYS = {
  RECENT_STORIES: 'learnershood_recent_stories',
  QUIZ_HISTORY: 'learnershood_quiz_history'
};

export interface Story {
  _id: string;
  title: string;
  audioUrl: string;
  transcript: string;
  visualScenes: string[];
  createdAt: number;
}

export const saveStory = (story: Story) => {
  try {
    const stories = getRecentStories();
    // Check if story already exists
    const existingIndex = stories.findIndex(s => s._id === story._id);
    
    if (existingIndex !== -1) {
      // Update existing story
      stories[existingIndex] = story;
    } else {
      // Add new story
      stories.unshift(story);
    }
    
    // Keep only the last 10 stories
    const updatedStories = stories.slice(0, 10);
    localStorage.setItem(STORAGE_KEYS.RECENT_STORIES, JSON.stringify(updatedStories));
  } catch (error) {
    console.error('Error saving story:', error);
  }
};

export const getRecentStories = (): Story[] => {
  try {
    const stories = localStorage.getItem(STORAGE_KEYS.RECENT_STORIES);
    return stories ? JSON.parse(stories) : [];
  } catch (error) {
    console.error('Error getting recent stories:', error);
    return [];
  }
};

export const clearStories = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.RECENT_STORIES);
  } catch (error) {
    console.error('Error clearing stories:', error);
  }
};