"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "@/hooks/use-toast";
import { CheckCircle } from "lucide-react";

export function BurnoutPredictionForm({ onSubmit }) {
  const [heartRate, setHeartRate] = useState("");
  const [sleepDuration, setSleepDuration] = useState("");
  const [sleepQuality, setSleepQuality] = useState("");
  const [activityLevel, setActivityLevel] = useState("");
  const [stressLevel, setStressLevel] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hasSubmittedToday, setHasSubmittedToday] = useState(false);

  useEffect(() => {
    checkTodaySubmission();
  }, []);

  const checkTodaySubmission = async () => {
    try {
      const response = await fetch("/api/health-data");
      if (response.ok) {
        const data = await response.json();
        const today = new Date().toDateString();
        const hasSubmitted = data.data.some(
          (entry) => new Date(entry.date).toDateString() === today
        );
        setHasSubmittedToday(hasSubmitted);
      }
    } catch (error) {
      console.error("Error checking today's submission:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/health-data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          heartRate: Number(heartRate),
          sleepDuration: Number(sleepDuration),
          sleepQuality,
          activityLevel,
          stressLevel: Number(stressLevel),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to submit health data");
      }

      const data = await response.json();
      onSubmit(data.data);
      toast({
        title: "Success",
        description: "Health data submitted successfully",
      });

      setHeartRate("");
      setSleepDuration("");
      setSleepQuality("");
      setActivityLevel("");
      setStressLevel("");
      setHasSubmittedToday(true);
    } catch (error) {
      console.error("Error submitting health data:", error);
      toast({
        title: "Error",
        description:
          error.message || "Failed to submit health data. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (hasSubmittedToday) {
    return (
      <div className="p-8 text-center border border-green-200 shadow-sm bg-gradient-to-br from-green-50 to-green-100 rounded-xl">
        <div className="mb-4">
          <CheckCircle className="w-16 h-16 mx-auto text-green-500" />
        </div>
        <h3 className="mb-2 text-xl font-semibold text-green-800">
          All Set for Today!
        </h3>
        <p className="text-green-700">
          You've already submitted your health data for today.
        </p>
        <p className="mt-2 text-sm text-green-600">
          Come back tomorrow to continue tracking your health journey.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div>
          <Label htmlFor="heartRate" className="text-sm font-medium">
            Heart Rate (bpm)
          </Label>
          <Input
            id="heartRate"
            type="number"
            value={heartRate}
            onChange={(e) => setHeartRate(e.target.value)}
            required
            min="30"
            max="220"
            className="mt-1"
            placeholder="Enter heart rate"
          />
        </div>
        <div>
          <Label htmlFor="sleepDuration" className="text-sm font-medium">
            Sleep Duration (hours)
          </Label>
          <Input
            id="sleepDuration"
            type="number"
            value={sleepDuration}
            onChange={(e) => setSleepDuration(e.target.value)}
            required
            min="0"
            max="24"
            step="0.1"
            className="mt-1"
            placeholder="Enter sleep duration"
          />
        </div>
        <div>
          <Label htmlFor="sleepQuality" className="text-sm font-medium">
            Sleep Quality
          </Label>
          <Select value={sleepQuality} onValueChange={setSleepQuality} required>
            <SelectTrigger className="mt-1">
              <SelectValue placeholder="Select sleep quality" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="poor">Poor</SelectItem>
              <SelectItem value="fair">Fair</SelectItem>
              <SelectItem value="good">Good</SelectItem>
              <SelectItem value="excellent">Excellent</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label htmlFor="activityLevel" className="text-sm font-medium">
            Activity Level
          </Label>
          <Select
            value={activityLevel}
            onValueChange={setActivityLevel}
            required
          >
            <SelectTrigger className="mt-1">
              <SelectValue placeholder="Select activity level" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="sedentary">Sedentary</SelectItem>
              <SelectItem value="light">Light</SelectItem>
              <SelectItem value="moderate">Moderate</SelectItem>
              <SelectItem value="vigorous">Vigorous</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label htmlFor="stressLevel" className="text-sm font-medium">
            Stress Level (1-10)
          </Label>
          <Input
            id="stressLevel"
            type="number"
            value={stressLevel}
            onChange={(e) => setStressLevel(e.target.value)}
            required
            min="1"
            max="10"
            className="mt-1"
            placeholder="Enter stress level"
          />
        </div>
      </div>
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? "Submitting..." : "Submit Data"}
      </Button>
    </form>
  );
}
