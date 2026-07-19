import { NextResponse } from "next/server";

export function middleware(req) {
    // Retrieve the current response
    const res = NextResponse.next();

    // Add CORS headers for all API routes
    res.headers.append('Access-Control-Allow-Credentials', "false");
    res.headers.append('Access-Control-Allow-Origin', '*'); 
    res.headers.append('Access-Control-Allow-Methods', 'GET,DELETE,PATCH,POST,PUT');
    res.headers.append('Access-Control-Allow-Headers', 'Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date');

    return res;
}

// Apply middleware to all API routes
export const config = {
    matcher: '/api/:path*',
};
