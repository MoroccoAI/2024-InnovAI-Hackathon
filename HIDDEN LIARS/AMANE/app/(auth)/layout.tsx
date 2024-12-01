import { ReactNode } from "react";
import { NavBar } from "../../components/navbar";  // Adjust the import path as needed

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="relative min-h-screen w-full">
      {/* Background image can be added here if needed */}
      {/* <Image
        src="/path-to-your-background-image.jpg"
        alt="Background"
        layout="fill"
        objectFit="cover"
        className="opacity-60"
      /> */}

      <NavBar />

      <main className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4 pt-24 md:pt-32">
        <div className="w-full max-w-md space-y-8 bg-white dark:bg-zinc-900 p-8 rounded-xl shadow-lg">
          {children}
        </div>
      </main>
    </div>
  );
}