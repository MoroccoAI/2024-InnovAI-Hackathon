/**
 * @swagger
 * /api/signup:
 *   post:
 *     summary: Register a new user
 *     description: Register a new user in the system.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *                 description: Full name of the user
 *               email:
 *                 type: string
 *                 description: Email address of the user
 *               password:
 *                 type: string
 *                 description: User's password
 *               age:
 *                 type: number
 *                 description: Age of the user
 *               gender:
 *                 type: string
 *                 description: Gender of the user
 *             required:
 *               - name
 *               - email
 *               - password
 *               - age
 *               - gender
 *     responses:
 *       200:
 *         description: User registered successfully
 *       400:
 *         description: Invalid input
 *       500:
 *         description: An unexpected error occurred
 */

import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/prisma";

export async function POST(req) {
  try {
    const body = await req.json();

    // Validate input
    if (
      !body ||
      !body.name ||
      !body.email ||
      !body.password ||
      !body.age ||
      !body.gender
    ) {
      return NextResponse.json(
        {
          error:
            "Invalid input: name, email, password, age, and gender are required",
        },
        { status: 400 }
      );
    }

    const name = body.name.trim();
    const email = body.email.trim();
    const password = body.password.trim();
    const age = parseInt(body.age, 10);
    const gender = body.gender.toLowerCase();

    if (isNaN(age) || age <= 0) {
      return NextResponse.json(
        { error: "Invalid age. Age must be a positive number" },
        { status: 400 }
      );
    }

    const allowedGenders = ["male", "female"];
    if (!allowedGenders.includes(gender)) {
      return NextResponse.json(
        { error: "Invalid gender value. Allowed values: male, female" },
        { status: 400 }
      );
    }

    // Check for existing user
    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
      return NextResponse.json(
        { error: "User with this email already exists" },
        { status: 400 }
      );
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new user
    const newUser = await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
        age,
        gender,
      },
      select: { id: true, name: true, email: true, age: true, gender: true },
    });

    return NextResponse.json(
      { message: "User registered successfully", user: newUser },
      { status: 201 }
    );
  } catch (error) {
    console.error("Error during registration:", error.message || error);
    return NextResponse.json(
      { error: "An unexpected error occurred" },
      { status: 500 }
    );
  }
}
