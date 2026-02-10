import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const sessionCookie = request.cookies.get("better-auth.session_token");
  const { pathname } = request.nextUrl;

  const isProtected = pathname.startsWith("/dashboard") || pathname.startsWith("/chat");

  // Only redirect unauthenticated users away from protected pages
  // Let auth pages handle their own redirects to avoid loops
  if (isProtected && !sessionCookie) {
    return NextResponse.redirect(new URL("/sign-in", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/chat/:path*", "/sign-in", "/sign-up"],
};
