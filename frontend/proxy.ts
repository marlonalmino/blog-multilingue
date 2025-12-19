import { NextRequest, NextResponse } from "next/server";

const locales = ["pt", "en", "es"];
const defaultLocale = "pt";

export default function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const hasToken = !!req.cookies.get("access_token")?.value;
  console.log("[proxy] path", pathname, "token", hasToken ? "yes" : "no");
  if (pathname.startsWith("/_next") || pathname.startsWith("/api") || pathname.startsWith("/assets") || pathname.startsWith("/favicon.ico")) {
    return NextResponse.next();
  }
  if (pathname === "/") {
    const url = req.nextUrl.clone();
    url.pathname = `/${defaultLocale}/explore`;
    console.log("[proxy] redirect root to explore", url.pathname);
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
      console.log("[proxy] redirect auth pages to home", url.pathname);
      return NextResponse.redirect(url);
    }
  }
  if (!locale || !locales.includes(locale)) {
    const url = req.nextUrl.clone();
    url.pathname = `/${defaultLocale}${pathname.startsWith("/") ? pathname : `/${pathname}`}`;
    console.log("[proxy] normalize locale", url.pathname);
    return NextResponse.redirect(url);
  }
  console.log("[proxy] pass-through", pathname);
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next|static|.*\\..*).*)"],
};
