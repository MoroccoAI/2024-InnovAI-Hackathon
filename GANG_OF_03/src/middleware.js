import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  // Allow access to "/" for non-logged in users
  if (!req.auth && req.nextUrl.pathname === "/") {
    return null;
  }

  // Redirect logged in users trying to access "/"
  if (req.auth && req.nextUrl.pathname === "/") {
    return NextResponse.redirect(new URL("/dashboard", req.nextUrl.origin));
  }

  // Prevent logged in users from accessing /login and /signup
  if (
    req.auth &&
    (req.nextUrl.pathname === "/login" || req.nextUrl.pathname === "/signup")
  ) {
    return NextResponse.redirect(new URL("/dashboard", req.nextUrl.origin));
  }

  // Handle other routes - redirect to login if not authenticated
  if (!req.auth && !["/login", "/signup"].includes(req.nextUrl.pathname)) {
    return NextResponse.redirect(new URL("/login", req.nextUrl.origin));
  }

  // Allow access for authenticated users or to /login and /signup for non-authenticated users
  return null;
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
