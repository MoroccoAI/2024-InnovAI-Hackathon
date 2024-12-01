"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BurnoutPredictionForm } from "@/components/BurnoutPredictionForm";
import Link from "next/link";
import { signOut } from "next-auth/react";
import {
  Loader2,
  Activity,
  Heart,
  Moon,
  Zap,
  BarChart,
  ChevronRight,
} from "lucide-react";

export default function SubmitData() {
  const [healthData, setHealthData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchHealthData = async () => {
    try {
      const response = await fetch("/api/health-data");
      if (!response.ok) {
        throw new Error("Failed to fetch health data");
      }
      const data = await response.json();
      setHealthData(data.data);
    } catch (error) {
      console.error("Error fetching health data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHealthData();
  }, []);

  const handleDataSubmit = (newData) => {
    setHealthData([newData, ...healthData.slice(0, 6)]); // Keep only the last 7 days of data
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
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
        <div className="grid gap-8 lg:grid-cols-3">
          <Card className="overflow-hidden transition-shadow duration-300 shadow-lg lg:col-span-2 hover:shadow-xl">
            <CardHeader className="bg-primary/5">
              <CardTitle className="flex items-center space-x-2 text-2xl font-bold">
                <BarChart className="w-6 h-6 text-primary" />
                <span>Your Health Dashboard</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              {isLoading ? (
                <div className="flex items-center justify-center h-64">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
              ) : healthData.length > 0 ? (
                <div className="space-y-6">
                  {healthData.map((data, index) => (
                    <div
                      key={index}
                      className="p-4 transition-all duration-200 rounded-lg bg-card hover:bg-accent hover:shadow-md"
                    >
                      <h3 className="flex items-center justify-between mb-3 text-lg font-semibold text-primary">
                        <span>
                          {new Date(data.date).toLocaleDateString(undefined, {
                            weekday: "long",
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          })}
                        </span>
                        <ChevronRight className="w-5 h-5 text-muted-foreground" />
                      </h3>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="flex items-center p-2 space-x-2 rounded-md bg-background/50">
                          <Heart className="w-4 h-4 text-red-500" />
                          <p>
                            Heart Rate:{" "}
                            <span className="font-semibold">
                              {data.heartRate} bpm
                            </span>
                          </p>
                        </div>
                        <div className="flex items-center p-2 space-x-2 rounded-md bg-background/50">
                          <Moon className="w-4 h-4 text-blue-500" />
                          <p>
                            Sleep:{" "}
                            <span className="font-semibold">
                              {data.sleepDuration} hours
                            </span>
                          </p>
                        </div>
                        <div className="flex items-center p-2 space-x-2 rounded-md bg-background/50">
                          <Activity className="w-4 h-4 text-green-500" />
                          <p>
                            Sleep Quality:{" "}
                            <span className="font-semibold">
                              {data.sleepQuality}
                            </span>
                          </p>
                        </div>
                        <div className="flex items-center p-2 space-x-2 rounded-md bg-background/50">
                          <Zap className="w-4 h-4 text-yellow-500" />
                          <p>
                            Activity:{" "}
                            <span className="font-semibold">
                              {data.activityLevel}
                            </span>
                          </p>
                        </div>
                        <div className="flex items-center col-span-2 p-2 space-x-2 rounded-md bg-background/50">
                          <BarChart className="w-4 h-4 text-purple-500" />
                          <p>
                            Stress Level:{" "}
                            <span className="font-semibold">
                              {data.stressLevel}/10
                            </span>
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-12 text-center rounded-lg text-muted-foreground bg-accent/50">
                  <BarChart className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-lg font-semibold">No data submitted yet</p>
                  <p className="mt-2">
                    Use the form on the right to submit your health data and
                    start tracking your well-being.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="overflow-hidden transition-shadow duration-300 shadow-lg lg:col-span-1 hover:shadow-xl">
            <CardHeader className="bg-primary/5">
              <CardTitle className="flex items-center space-x-2 text-2xl font-bold">
                <Activity className="w-6 h-6 text-primary" />
                <span>Daily Health Check-In</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <BurnoutPredictionForm onSubmit={handleDataSubmit} />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
