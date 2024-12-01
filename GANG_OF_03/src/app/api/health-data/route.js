import { auth } from "@/auth";
import { prisma } from "@/prisma";
import { NextResponse } from "next/server";

// Helper function to calculate averages from health data
async function calculateAverages(userId) {
  const last7Days = new Date();
  last7Days.setDate(last7Days.getDate() - 7);

  const healthData = await prisma.healthData.findMany({
    where: {
      userId: userId,
      date: {
        gte: last7Days,
      },
    },
    orderBy: {
      date: "desc",
    },
  });

  // Default values if not enough data
  if (healthData.length === 0) {
    return {
      avg_sleep: 7,
      avg_stress: 5,
      avg_steps: 8000,
      avg_work_hours: 8,
      avg_hrv: 60,
      avg_rhr: 70,
      avg_sleep_quality: 70,
    };
  }

  // Calculate averages
  const avgSleep =
    healthData.reduce((acc, data) => acc + (data.sleepDuration || 0), 0) /
    healthData.length;
  const avgStress =
    healthData.reduce((acc, data) => acc + (data.stressLevel || 0), 0) /
    healthData.length;
  const avgHR =
    healthData.reduce((acc, data) => acc + (data.heartRate || 0), 0) /
    healthData.length;

  // Convert sleep quality string to number (assuming sleep quality is stored as "Poor", "Fair", "Good", "Excellent")
  const sleepQualityMap = { Poor: 25, Fair: 50, Good: 75, Excellent: 100 };
  const avgSleepQuality =
    healthData.reduce(
      (acc, data) => acc + (sleepQualityMap[data.sleepQuality] || 70),
      0
    ) / healthData.length;

  return {
    avg_sleep: avgSleep,
    avg_stress: avgStress,
    avg_steps: 8000, // Default value as it's not in your schema
    avg_work_hours: 8, // Default value as it's not in your schema
    avg_hrv: 60, // Default or calculated from heart rate
    avg_rhr: avgHR,
    avg_sleep_quality: avgSleepQuality,
  };
}

// Helper function to predict burnout
async function predictBurnout(averages) {
  try {
    const response = await fetch(
      "https://yusef-faik-burnout-prediction.hf.space/predict",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.HUGGINGFACE_TOKEN}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(averages),
      }
    );

    if (!response.ok) {
      throw new Error(`Prediction API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Burnout prediction error:", error);
    throw error;
  }
}

export const GET = auth(async function GET(req) {
  if (!req.auth) {
    return NextResponse.json({ message: "Not authenticated" }, { status: 401 });
  }

  try {
    const healthData = await prisma.healthData.findMany({
      where: {
        userId: req.auth.user.id,
      },
      orderBy: {
        date: "desc",
      },
      take: 7,
    });

    return NextResponse.json(
      { message: "Health data retrieved successfully", data: healthData },
      { status: 200 }
    );
  } catch (error) {
    console.error("Error retrieving health data:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
});

export const POST = auth(async function POST(req) {
  if (!req.auth) {
    return NextResponse.json({ message: "Not authenticated" }, { status: 401 });
  }

  try {
    const body = await req.json();

    // Validate input
    if (
      !body.heartRate ||
      !body.sleepDuration ||
      !body.sleepQuality ||
      !body.activityLevel ||
      !body.stressLevel
    ) {
      return NextResponse.json(
        { error: "Invalid input: all fields are required" },
        { status: 400 }
      );
    }

    // Check if an entry already exists for today
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const existingEntry = await prisma.healthData.findFirst({
      where: {
        userId: req.auth.user.id,
        date: {
          gte: today,
          lt: new Date(today.getTime() + 24 * 60 * 60 * 1000),
        },
      },
    });

    if (existingEntry) {
      return NextResponse.json(
        { error: "Health data has already been submitted for today" },
        { status: 400 }
      );
    }

    // Create health data entry
    const healthData = await prisma.healthData.create({
      data: {
        userId: req.auth.user.id,
        date: new Date(),
        heartRate: parseInt(body.heartRate),
        sleepDuration: parseFloat(body.sleepDuration),
        sleepQuality: body.sleepQuality,
        activityLevel: body.activityLevel,
        stressLevel: parseInt(body.stressLevel),
      },
    });

    // Calculate averages and predict burnout
    const averages = await calculateAverages(req.auth.user.id);
    const burnoutPrediction = await predictBurnout(averages);

    // Store burnout prediction
    await prisma.burnoutPrediction.create({
      data: {
        userId: req.auth.user.id,
        date: new Date(),
        burnoutRisk: burnoutPrediction.burnout_percentage || 0,
        recommendations: burnoutPrediction.recommendations || [],
      },
    });

    return NextResponse.json(
      {
        message: "Health data submitted successfully",
        data: healthData,
        burnoutPrediction: burnoutPrediction,
      },
      { status: 201 }
    );
  } catch (error) {
    console.error("Error submitting health data:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
});
