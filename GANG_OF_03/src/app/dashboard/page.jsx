import { PrismaClient } from "@prisma/client";
import Dashboard from "./dashboard-client";
import { auth } from "@/auth";

const prisma = new PrismaClient();

async function getData(userId) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: {
      healthData: {
        orderBy: { date: "desc" },
        take: 7,
      },
      burnoutPredictions: {
        orderBy: { date: "desc" },
        take: 1,
      },
    },
  });

  return user;
}

export default async function DashboardPage() {
  const session = await auth();
  if (!session?.user) {
    return <div>Please sign in to view your dashboard</div>;
  }

  const userData = await getData(session.user.id);

  if (!userData) {
    return <div>User not found</div>;
  }

  return <Dashboard userData={userData} />;
}
