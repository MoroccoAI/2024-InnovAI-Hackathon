import { getServerSession } from "next-auth";
import { ReactNode } from "react";
import { authOptions } from "../utils/auth";
import { redirect } from "next/navigation";
import Sidebar, { SidebarItem } from "../components/SideBar";
import { Home, Settings, User, FileText, HelpCircle } from "lucide-react"; 
import Navbar from "../components/NavBar";

export default async function HomeLayout({
  children,
}: {
  children: ReactNode;
}) {
  const session = await getServerSession(authOptions);

  if (!session) {
    return redirect("/login");
  }

  const userName = session.user?.name || "Guest";
  const userEmail = session.user?.email || "example@example.com";

  return (
    <div className="flex h-screen">
      <Sidebar name={userName} email={userEmail}>
        <SidebarItem icon={<Home />} text={"Home"} href="/home" />
        <SidebarItem icon={<FileText />} text={"Sensor State"} href="/sensor" />
        <SidebarItem icon={<User />} text={"Profile"} href="/profile" />
        <SidebarItem icon={<Settings />} text={"Settings"} href="/settings" />
        <SidebarItem icon={<HelpCircle />} text={"Help"} href="/help" />
      </Sidebar>
      <main className="flex-1 p-4 overflow-y-auto">
        <Navbar />
        {children}
      </main>
    </div>
  );
}