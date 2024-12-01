import React from 'react';
import { useProfile } from '../../hooks/useProfile';

export function Profile() {
  const { profile, handleSubmit, handleChange } = useProfile();

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Name
        </label>
        <input
          type="text"
          name="name"
          value={profile.name}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Enter your name"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Focus Duration (minutes)
        </label>
        <input
          type="number"
          name="focusDuration"
          value={profile.focusDuration}
          onChange={handleChange}
          min="1"
          max="60"
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Break Duration (minutes)
        </label>
        <input
          type="number"
          name="breakDuration"
          value={profile.breakDuration}
          onChange={handleChange}
          min="1"
          max="30"
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Theme
        </label>
        <select
          name="theme"
          value={profile.theme}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="nature">Nature</option>
        </select>
      </div>
      <button
        type="submit"
        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
      >
        Save Settings
      </button>
    </form>
  );
}