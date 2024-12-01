import { getServerSession } from "next-auth";
import { authOptions } from "@/app/utils/auth";

export async function SessionProvider() {
  const session = await getServerSession(authOptions);
  return { session };
}