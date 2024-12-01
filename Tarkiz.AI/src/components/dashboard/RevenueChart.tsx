import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Sep', arrival: 450, spending: 200 },
  { month: 'Oct', arrival: 400, spending: 100 },
  { month: 'Nov', arrival: 300, spending: 500 },
  { month: 'Dec', arrival: 150, spending: 250 },
  { month: 'Jan', arrival: 100, spending: 200 },
  { month: 'Feb', arrival: 400, spending: 250 },
];

export default function RevenueChart() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold">Revenue</h3>
        <select className="border rounded-md px-3 py-1 text-sm">
          <option>Monthly</option>
          <option>Weekly</option>
          <option>Daily</option>
        </select>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="arrival" fill="#1e40af" />
            <Bar dataKey="spending" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}