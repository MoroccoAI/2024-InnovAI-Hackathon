import React from 'react';
import { MagnifyingGlassIcon, BellIcon } from '@heroicons/react/24/outline';

interface HeaderProps {
  userName: string;
}

export default function Header({ userName }: HeaderProps) {
  return (
    <div className="flex justify-between items-center mb-8">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Good Morning, {userName}</h1>
        <p className="text-gray-500">Welcome back, nice to see you again!</p>
      </div>
      <div className="flex items-center space-x-4">
        <button className="p-2 hover:bg-gray-100 rounded-full">
          <MagnifyingGlassIcon className="h-6 w-6 text-gray-500" />
        </button>
        <button className="p-2 hover:bg-gray-100 rounded-full">
          <BellIcon className="h-6 w-6 text-gray-500" />
        </button>
        <img
          src="https://ui-avatars.com/api/?name=John+Doe"
          alt="Profile"
          className="h-10 w-10 rounded-full"
        />
      </div>
    </div>
  );
}