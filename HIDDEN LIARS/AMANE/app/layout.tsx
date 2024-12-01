import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { NextAuthProvider } from "./components/NextAuthProvider";
import { NavBar } from "@/components/navbar";
import Footer from "@/components/footer";
import { getServerSession } from "next-auth"; // Import the session checker
import { authOptions } from "@/app/utils/auth"; // Adjust the import according to your project structure

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Amane",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getServerSession(authOptions); // Get the current session

  const isAuthenticated = !!session; // Check if there is an active session

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Render NavBar and Footer conditionally based on authentication status */}
        {!isAuthenticated && <NavBar/>}
        {/* <NavBar/> */}
        <NextAuthProvider>{children}</NextAuthProvider>
        {/* <Footer/> */}
        {!isAuthenticated && <Footer/>}
        
      </body>
    </html>
  );
}
