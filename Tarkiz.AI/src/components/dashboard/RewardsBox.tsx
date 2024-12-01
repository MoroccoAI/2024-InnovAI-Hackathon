import React from 'react';
import { TrophyIcon, FireIcon, SparklesIcon } from '@heroicons/react/24/solid';

const rewards = [
  {
    title: "Focus Champion",
    description: "Completed 5 focus sessions today",
    icon: TrophyIcon,
    progress: 80,
  },
  {
    title: "Productivity Streak",
    description: "5 days streak of completing all tasks",
    icon: FireIcon,
    progress: 60,
  },
  {
    title: "Task Master",
    description: "Completed 20 tasks this week",
    icon: SparklesIcon,
    progress: 45,
  },
];

export default function RewardsBox() {
  return (
    <div className="dashboard-card p-6 h-[350px]">
      <h2 className="text-xl font-semibold mb-6 neon-text">Rewards & Achievements</h2>
      <div className="space-y-4 h-[calc(100%-4rem)] overflow-y-auto">
        {rewards.map((reward) => (
          <div key={reward.title} className="bg-opacity-10 bg-white backdrop-blur-md rounded-lg p-4 border border-gray-700">
            <div className="flex items-start space-x-4">
              <div className="bg-neon-green bg-opacity-10 p-2 rounded-lg">
                <reward.icon className="h-6 w-6 text-neon-green" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-white">{reward.title}</h3>
                <p className="text-sm text-gray-300">{reward.description}</p>
                <div className="mt-2 w-full bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-neon-green h-2 rounded-full transition-all duration-500"
                    style={{ width: `${reward.progress}%` }}
                  />
                </div>
                <p className="text-xs text-gray-300 mt-1">{reward.progress}% Complete</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}