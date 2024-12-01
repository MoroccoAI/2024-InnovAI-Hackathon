"use client";
import { MoreVertical, ChevronLast, ChevronFirst } from "lucide-react";
import { useContext, createContext, useState, ReactNode } from "react";
import { useRouter } from "next/navigation"; 
import Logo from "@/public/amane.svg";
import Image from "next/image";

const SidebarContext = createContext<{ expanded: boolean }>({ expanded: true });

interface SidebarProps {
  children: ReactNode;
  name: string;
  email: string;
}

export default function Sidebar({ children, name, email }: SidebarProps) {
  const [expanded, setExpanded] = useState(true);

  return (
    <aside className={`h-screen ${expanded ? 'w-64' : 'w-16'} transition-all bg-white border-r shadow-sm`}>
      <nav className="h-full flex flex-col">
        <div className="p-4 pb-2 flex flex-col items-center">
          <div className={`flex items-center ${expanded ? 'ml-3' : ''}`}>
            <Image
              src={Logo}
              width={142}
              height={72}
              alt="Amane Logo"
              className={`transition-all dark:invert ${expanded ? 'block' : 'hidden'}`} // Show logo only when expanded
            />
            <div className={`w-10 h-10 rounded-full flex justify-center items-center ${expanded ? 'hidden' : 'block'}`}>
              <Image
                src={Logo}
                width={32}
                height={32}
                alt="Company Logo"
                className="dark:invert"
              />
            </div>
          </div>
          
          {/* Move the button below the logo when minimized */}
          <button
            onClick={() => setExpanded((curr) => !curr)}
            className="p-1.5 rounded-lg bg-gray-50 hover:bg-gray-100 mt-4"
          >
            {expanded ? <ChevronFirst /> : <ChevronLast />}
          </button>
        </div>

        <SidebarContext.Provider value={{ expanded }}>
          <ul className="flex-1 px-3 overflow-y-auto">
            {children}
          </ul>
        </SidebarContext.Provider>

        <div className="border-t flex p-3 items-center space-x-3">
          <img
            src={`https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=c7d2fe&color=3730a3&bold=true`}
            alt="User Avatar"
            className="w-10 h-10 rounded-md"
          />

          <div
            className={`flex justify-between items-center overflow-hidden transition-all ${expanded ? "ml-3" : "w-0"}`}
          >
            <div className="leading-4">
              <h4 className="font-semibold">{name}</h4>
              <span className="text-xs text-gray-600">{email}</span>
            </div>
            <MoreVertical size={20} />
          </div>
        </div>
      </nav>
    </aside>
  );
}

interface SidebarItemProps {
  icon: ReactNode;
  text: string;
  href?: string; // Add optional href for navigation
  active?: boolean;
  alert?: boolean;
}

export function SidebarItem({ icon, text, href = "/", active, alert }: SidebarItemProps) {
  const { expanded } = useContext(SidebarContext);
  const router = useRouter();

  const handleClick = () => {
    router.push(href);
  };

  return (
    <li
      onClick={handleClick}
      className={`relative flex items-center py-2 px-3 my-1 font-medium rounded-md cursor-pointer transition-colors group ${
        active
          ? "bg-gradient-to-tr from-indigo-200 to-indigo-100 text-indigo-800"
          : "hover:bg-indigo-50 text-gray-600"
      }`}
    >
      <div className={`${expanded ? 'text-xl' : 'text-2xl'} transition-all`}>
        {icon}
      </div>

      <span
        className={`overflow-hidden transition-all ${expanded ? "ml-3" : "w-0"}`}
      >
        {text}
      </span>

      {alert && (
        <div
          className={`absolute right-2 w-2 h-2 rounded bg-indigo-400 ${expanded ? "" : "top-2"}`}
        />
      )}

      {!expanded && (
        <div
          className={`absolute left-full rounded-md px-2 py-1 ml-6 bg-indigo-100 text-indigo-800 text-sm invisible opacity-20 -translate-x-3 transition-all group-hover:visible group-hover:opacity-100 group-hover:translate-x-0`}
        >
          {text}
        </div>
      )}
    </li>
  );
}
