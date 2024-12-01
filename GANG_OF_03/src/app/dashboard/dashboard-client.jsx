"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Brain, Footprints, Moon, TrendingUp } from "lucide-react";
import { signOut } from "next-auth/react";
import Link from "next/link";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function TimeframeSelector({ value, onChange }) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select timeframe" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="daily">Daily</SelectItem>
        <SelectItem value="weekly">Weekly</SelectItem>
        <SelectItem value="monthly">Monthly</SelectItem>
      </SelectContent>
    </Select>
  );
}

function SleepScoreCard({ score, insight, data }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">Sleep Score</CardTitle>
        <Moon className="w-4 h-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">
          {score !== null ? `${score.toFixed(1)}/10` : "N/A"}
        </div>
        <p className="text-xs text-muted-foreground">{insight}</p>
        <div className="h-[100px] mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <Area
                type="monotone"
                dataKey="hours"
                stroke="hsl(var(--primary))"
                fill="hsl(var(--primary))"
                fillOpacity={0.2}
              />
              <Tooltip />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

function StressScoreCard({ score, insight, data }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">Stress Score</CardTitle>
        <Brain className="w-4 h-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">
          {score !== null ? `${score.toFixed(1)}/10` : "N/A"}
        </div>
        <p className="text-xs text-muted-foreground">{insight}</p>
        <div className="h-[100px] mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <Bar dataKey="level" fill="hsl(var(--destructive))" />
              <Tooltip />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

function BurnoutRiskMeter({ risk }) {
  const riskPercentage = risk !== null ? Math.round(risk) : null;
  const riskLevel =
    risk === null
      ? "Unknown"
      : risk < 0.3
      ? "Low"
      : risk < 0.7
      ? "Moderate"
      : "High";
  const riskColor =
    risk === null
      ? "hsl(var(--muted-foreground))"
      : risk < 0.3
      ? "hsl(var(--success))"
      : risk < 0.7
      ? "hsl(var(--warning))"
      : "hsl(var(--destructive))";

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">Burnout Risk</CardTitle>
        <TrendingUp className="w-4 h-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold" style={{ color: riskColor }}>
          {riskLevel}
        </div>
        <p className="text-xs text-muted-foreground">
          {riskPercentage !== null
            ? `Current Risk: ${riskPercentage}%`
            : "No data available"}
        </p>
        <div className="h-[100px] mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={[
                { name: "Low", value: 30 },
                { name: "Moderate", value: 45 },
                { name: "High", value: 25 },
              ]}
            >
              <Area
                type="monotone"
                dataKey="value"
                stroke={riskColor}
                fill={riskColor}
                fillOpacity={0.2}
              />
              <Tooltip />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

function ActivityScoreCard({ score, insight, data }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">Activity Score</CardTitle>
        <Footprints className="w-4 h-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">
          {score !== null ? `${score.toFixed(1)}/10` : "N/A"}
        </div>
        <p className="text-xs text-muted-foreground">{insight}</p>
        <div className="h-[100px] mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <Bar dataKey="level" fill="hsl(var(--primary))" />
              <Tooltip />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

function TrendChart({ title, data, dataKey, timeframe, color }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey={dataKey} stroke={color} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex items-center justify-center h-[300px] text-muted-foreground">
            No data available
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function Dashboard({ userData }) {
  const [timeframe, setTimeframe] = useState("weekly");
  const userName = userData.name || "User";

  const calculateAverage = (data, key) => {
    if (data.length === 0) return null;
    const sum = data.reduce((acc, curr) => acc + (curr[key] || 0), 0);
    return sum / data.length;
  };

  const getActivityLevel = (level) => {
    switch (level) {
      case "sedentary":
        return 1;
      case "light":
        return 2;
      case "moderate":
        return 3;
      case "vigorous":
        return 4;
      default:
        return 0;
    }
  };

  const sleepData = userData.healthData
    .map((data) => ({
      day: new Date(data.date).toLocaleDateString("en-US", {
        weekday: "short",
      }),
      hours: data.sleepDuration || 0,
    }))
    .reverse();

  const stressData = userData.healthData
    .map((data) => ({
      day: new Date(data.date).toLocaleDateString("en-US", {
        weekday: "short",
      }),
      level: data.stressLevel || 0,
    }))
    .reverse();

  const activityData = userData.healthData
    .map((data) => ({
      day: new Date(data.date).toLocaleDateString("en-US", {
        weekday: "short",
      }),
      level: getActivityLevel(data.activityLevel),
    }))
    .reverse();

  const avgSleepDuration = calculateAverage(
    userData.healthData,
    "sleepDuration"
  );
  const avgStressLevel = calculateAverage(userData.healthData, "stressLevel");
  const avgActivityLevel = calculateAverage(
    userData.healthData.map((data) => ({
      level: getActivityLevel(data.activityLevel),
    })),
    "level"
  );

  const getSleepInsight = (avg) => {
    if (avg === null) return "No sleep data available";
    if (avg >= 7 && avg <= 9) return "Optimal Sleep Duration";
    if (avg < 7) return "Consider More Sleep";
    return "Excessive Sleep, Consider Adjusting";
  };

  const getStressInsight = (avg) => {
    if (avg === null) return "No stress data available";
    if (avg <= 3) return "Low Stress Levels";
    if (avg <= 6) return "Moderate Stress Levels";
    return "High Stress Levels, Consider Stress Management";
  };

  const getActivityInsight = (avg) => {
    if (avg === null) return "No activity data available";
    if (avg <= 1.5) return "Consider Increasing Activity";
    if (avg <= 2.5) return "Moderate Activity Level";
    return "Good Activity Level";
  };

  const latestBurnoutPrediction = userData.burnoutPredictions[0] || {
    burnoutRisk: null,
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container px-4 py-4 mx-auto">
          <nav className="flex items-center justify-between">
            <Link href="/dashboard" className="text-2xl font-bold">
              Burnout Predictor
            </Link>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" asChild>
                <Link href="/dashboard/health-data">Health Data</Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link href="/dashboard/profile">Profile</Link>
              </Button>
              <Button
                variant="destructive"
                onClick={() => signOut({ redirectTo: "/" })}
              >
                Sign Out
              </Button>
            </div>
          </nav>
        </div>
      </header>

      <main className="container p-4 mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">
              Welcome back, <span className="text-primary">{userName}!</span>
            </h1>
            <p className="text-muted-foreground">
              {userData.healthData.length === 0
                ? "Start tracking your well-being by submitting your first health data!"
                : "Here's an overview of your well-being metrics"}
            </p>
          </div>
          <TimeframeSelector value={timeframe} onChange={setTimeframe} />
        </div>

        {userData.healthData.length === 0 ? (
          <div className="p-8 text-center rounded-lg bg-muted">
            <h2 className="mb-4 text-2xl font-semibold">
              No Health Data Available
            </h2>
            <p className="mb-4">
              It looks like you haven't submitted any health data yet. Start
              tracking your well-being to see insights and trends!
            </p>
            <Button asChild>
              <Link href="/dashboard/health-data">Submit Health Data</Link>
            </Button>
          </div>
        ) : (
          <>
            <div className="grid gap-6 md:grid-cols-4">
              <SleepScoreCard
                score={avgSleepDuration}
                insight={getSleepInsight(avgSleepDuration)}
                data={sleepData}
              />
              <StressScoreCard
                score={avgStressLevel}
                insight={getStressInsight(avgStressLevel)}
                data={stressData}
              />
              <BurnoutRiskMeter risk={latestBurnoutPrediction.burnoutRisk} />
              <ActivityScoreCard
                score={avgActivityLevel}
                insight={getActivityInsight(avgActivityLevel)}
                data={activityData}
              />
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <TrendChart
                title="Sleep Trend"
                data={sleepData}
                dataKey="hours"
                timeframe={timeframe}
                color="hsl(var(--primary))"
              />
              <TrendChart
                title="Stress Trend"
                data={stressData}
                dataKey="level"
                timeframe={timeframe}
                color="hsl(var(--destructive))"
              />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
