import { headers } from "next/headers";
import { API_BASE } from "./config";

export async function getServerUser() {
  const hdrs = await headers();
  const cookieHeader = hdrs.get("cookie") || "";
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { cookie: cookieHeader },
    cache: "no-store",
  });
  if (!res.ok) return null;
  return res.json();
}
