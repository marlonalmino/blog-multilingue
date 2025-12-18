import { API_BASE } from "./config";

export async function getCsrf() {
  const res = await fetch(`${API_BASE}/auth/csrf-token`, { credentials: "include" });
  if (!res.ok) throw new Error("csrf_failed");
  return res.json();
}

export async function login(payload: { username: string; password: string }) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("login_failed");
  return res.json();
}

export async function register(payload: { username: string; email?: string; password: string }) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("register_failed");
  return res.json();
}

export async function me() {
  const res = await fetch(`${API_BASE}/auth/me`, { credentials: "include" });
  if (!res.ok) throw new Error("me_failed");
  return res.json();
}

export async function logout() {
  const res = await fetch(`${API_BASE}/auth/logout`, { method: "POST", credentials: "include" });
  if (!res.ok) throw new Error("logout_failed");
  return res.json();
}

export function notifyAuthChanged() {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new Event("auth-changed"));
  }
}
