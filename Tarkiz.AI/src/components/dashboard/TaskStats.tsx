import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

const productivityData = [
  { day: 'Mon', value: 65 },
  { day: 'Tue', value: 75 },
  { day: 'Wed', value: 85 },
  { day: 'Thu', value: 70 },
  { day: 'Fri', value: 90 },
];

const completionData = [
  { name: 'Completed', value: 75 },
  { name: 'Pending', value: 25 },
];

const COLORS = ['#00ff9d', '#16213e'];

export default function TaskStats() {
  return (
    <div className="dashboard-card p-6">
      <h2 className="text-xl font-semibold mb-6 neon-text">Task Statistics</h2>
      
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium mb-4 text-white">Task Completion Rate</h3>
          <div className="h-48 neon-chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={completionData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {completionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-medium mb-4 text-white">Productivity Trend</h3>
          <div className="h-48 neon-chart">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={productivityData}>
                <XAxis dataKey="day" stroke="#ffffff" />
                <YAxis stroke="#ffffff" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(22, 33, 62, 0.9)',
                    border: '1px solid #00ff9d',
                    borderRadius: '8px',
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#00ff9d" 
                  strokeWidth={2}
                  dot={{ fill: '#00ff9d' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}