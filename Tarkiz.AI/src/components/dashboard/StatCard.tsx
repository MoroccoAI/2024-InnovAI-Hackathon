import React from 'react';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';

interface StatCardProps {
  title: string;
  value: string;
  change: number;
  comparison: string;
}

export default function StatCard({ title, value, change, comparison }: StatCardProps) {
  const isPositive = change >= 0;

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm">
      <h3 className="text-gray-500 text-sm mb-2">{title}</h3>
      <div className="flex items-baseline space-x-2">
        <span className="text-2xl font-bold">{value}</span>
        <span className={clsx(
          'flex items-center text-sm',
          isPositive ? 'text-green-500' : 'text-red-500'
        )}>
          {isPositive ? <ArrowUpIcon className="h-4 w-4" /> : <ArrowDownIcon className="h-4 w-4" />}
          {Math.abs(change)}%
        </span>
      </div>
      <p className="text-gray-400 text-sm mt-1">Compared to {comparison}</p>
    </div>
  );
}