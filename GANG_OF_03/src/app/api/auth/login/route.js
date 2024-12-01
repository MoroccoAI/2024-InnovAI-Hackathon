/**
 * @swagger
 * /api/login:
 *   post:
 *     summary: Login a user
 *     description: Login a user in the system.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               email:
 *                 type: string
 *                 description: Email address of the user
 *               password:
 *                 type: string
 *                 description: User's password
 *             required:
 *               - email
 *               - password
 *     responses:
 *      200:
 *       description: User logged in successfully
 *     400:
 *      description: Invalid input
 *    500:
 *     description: An unexpected error occurred
 */

import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/prisma";

export async function POST(req) {
  try {
    const body = await req.json();

    // Validate input
    if (!body || !body.email || !body.password) {
      return NextResponse.json(
        {
          error: "Invalid input: email and password are required",
        },
        { status: 400 }
      );
    }

    const email = body.email.trim();
    const password = body.password.trim();

    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      return NextResponse.json(
        {
          error: "Invalid credentials",
        },
        { status: 400 }
      );
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      return NextResponse.json(
        {
          error: "Invalid credentials",
        },
        { status: 400 }
      );
    }

    return NextResponse.json(
      {
        id: user.id,
        email: user.email,
        // Include other safe user properties
      },
      { status: 200 }
    );
  } catch (error) {
    return NextResponse.json(
      {
        error: "An unexpected error occurred",
      },
      { status: 500 }
    );
  }
}
