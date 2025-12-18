import { NextRequest, NextResponse } from "next/server";

const locales = ["pt", "en", "es"];
const defaultLocale = "pt";

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  if (pathname.startsWith("/_next") || pathname.startsWith("/api") || pathname.startsWith("/assets") || pathname.startsWith("/favicon.ico")) {
    return NextResponse.next();
  }
  if (pathname === "/") {
    const url = req.nextUrl.clone();
    url.pathname = `/${defaultLocale}/login`;
    return NextResponse.redirect(url);
  }
  const parts = pathname.split("/").filter(Boolean);
  const locale = parts[0];
  if ((locale && locales.includes(locale) && pathname === `/${locale}/login`) 
    || (locale && locales.includes(locale) && pathname === `/${locale}/signup`)) {
    const token = req.cookies.get("access_token")?.value;
    if (token) {
      const url = req.nextUrl.clone();
      url.pathname = `/${locale}`;
      return NextResponse.redirect(url);
    }
  }
  if (!locale || !locales.includes(locale)) {
    const url = req.nextUrl.clone();
    url.pathname = `/${defaultLocale}${pathname.startsWith("/") ? pathname : `/${pathname}`}`;
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next|static|.*\\..*).*)"],
};
