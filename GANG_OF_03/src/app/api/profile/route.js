import { auth } from "@/auth";
import { prisma } from "@/prisma";
import { NextResponse } from "next/server";

export const GET = auth(async function GET(req) {
  if (!req.auth) {
    return NextResponse.json({ message: "Not authenticated" }, { status: 401 });
  }

  try {
    const user = await prisma.user.findUnique({
      where: { id: req.auth.user.id },
      select: {
        id: true,
        name: true,
        email: true,
        age: true,
        gender: true,
        image: true,
      },
    });

    return NextResponse.json({ user }, { status: 200 });
  } catch (error) {
    console.error("Error retrieving profile:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
});

export const PUT = auth(async function PUT(req) {
  if (!req.auth) {
    return NextResponse.json({ message: "Not authenticated" }, { status: 401 });
  }

  try {
    const body = await req.json();

    // Validate input
    const updateData = {};
    if (body.name) updateData.name = body.name;
    if (body.email) updateData.email = body.email;
    if (body.age) updateData.age = parseInt(body.age);
    if (body.gender) updateData.gender = body.gender;
    if (body.image) updateData.image = body.image;

    const user = await prisma.user.update({
      where: { id: req.auth.user.id },
      data: updateData,
      select: {
        id: true,
        name: true,
        email: true,
        age: true,
        gender: true,
        image: true,
      },
    });

    return NextResponse.json({ user }, { status: 200 });
  } catch (error) {
    console.error("Error updating profile:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
});
