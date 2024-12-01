import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/utils/auth";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await getServerSession(authOptions);
  return NextResponse.json({
    user: session?.user ?? null,
  });
}