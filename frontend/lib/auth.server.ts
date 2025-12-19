import { headers } from "next/headers";
import { API_BASE } from "./config";

export async function getServerUser() {
  const hdrs = await headers();
  const cookieHeader = hdrs.get("cookie") || "";
  console.log("[auth.server] cookieHeader", cookieHeader ? "present" : "missing");
  if (!/access_token=/.test(cookieHeader)) {
    console.log("[auth.server] no access_token cookie, returning null");
    return null;
  }
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { cookie: cookieHeader },
    cache: "no-store",
  });
  console.log("[auth.server] /auth/me res.ok", res.ok);
  if (!res.ok) return null;
  return res.json();
}
