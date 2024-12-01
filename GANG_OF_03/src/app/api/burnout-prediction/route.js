import { NextResponse } from "next/server";
import { prisma } from "@/prisma";

export async function POST(req) {
  try {
    const body = await req.json();

    if (!body.userId) {
      return NextResponse.json(
        { error: "userId is required" },
        { status: 400 }
      );
    }

    /* const burnoutPrediction = await prisma.burnoutPrediction.create({
      data: {
        userId: body.userId,
        date: new Date(),
        burnoutRisk: 11,
        recommendations: [
          "Take a break",
          "Go for a walk",
          "Talk to a friend",
          "Sleep well",
        ],
      },
    }); */

    const burnoutPrediction = {
      userId: body.userId,
      date: new Date(),
      burnoutRisk: 11,
      recommendations: [
        "Take a break",
        "Go for a walk",
        "Talk to a friend",
        "Sleep well",
      ],
    };

    return NextResponse.json(
      { message: "Burnout prediction generated", data: burnoutPrediction },
      { status: 201 }
    );
  } catch (error) {
    console.error("Error generating burnout prediction:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
}
