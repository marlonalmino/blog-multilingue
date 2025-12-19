/** @jsxImportSource react */
"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { locales, Locale, Dictionary } from "../lib/i18n";
import Button from "./ui/Button";
import { logout, me } from "../lib/auth";

type User = { id: number; username: string; email: string; roles: string[] };

export default function NavBar({ locale, dict, initialUser }: { locale: Locale; dict: Dictionary; initialUser?: User }) {
  const [user, setUser] = useState<User | null>(initialUser ?? null);
  useEffect(() => {
    me()
      .then((u) => setUser(u))
      .catch(() => setUser(null));
    const handler = () => {
      me()
        .then((u) => setUser(u))
        .catch(() => setUser(null));
    };
    window.addEventListener("auth-changed", handler);
    return () => window.removeEventListener("auth-changed", handler);
  }, []);
  async function onLogout() {
    try {
      await logout();
      setUser(null);
      window.location.assign(`/${locale}/login`);
      window.dispatchEvent(new Event("auth-changed"));
    } catch {}
  }
  return (
    <nav className="flex w-full items-center justify-between border-b border-zinc-200 bg-white px-6 py-4 dark:border-zinc-800 dark:bg-black">
      <div className="flex items-center gap-4">
        <Link href={`/${locale}`} className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          Multilang Blog
        </Link>
        <div className="hidden sm:flex">
          <div className="flex items-center gap-1 rounded-full border border-zinc-300 p-1 dark:border-zinc-700">
            {locales.map((l) => (
              <Link
                key={l}
                href={`/${l}`}
                className={`rounded-full px-2 py-1 text-xs transition ${
                  l === locale ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900" : "text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
                }`}
              >
                {l.toUpperCase()}
              </Link>
            ))}
          </div>
        </div>
        <Link
          href={`/${locale}/explore`}
          className="hidden rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800 sm:inline-block"
        >
          {dict.nav.explore}
        </Link>
      </div>
      {user ? (
        <div className="flex items-center gap-3">
          <span className="text-sm text-zinc-700 dark:text-zinc-200">{user.username}</span>
          <Link
            href={`/${locale}/posts`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.myPosts}
          </Link>
          <Link
            href={`/${locale}/posts/new`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.newPost}
          </Link>
          <Button onClick={onLogout} className="px-3 py-1 text-xs">
            {dict.nav.logout}
          </Button>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Link href={`/${locale}/login`} className="text-xs text-zinc-700 dark:text-zinc-200">
            {dict.nav.login}
          </Link>
          <Link
            href={`/${locale}/signup`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.signup}
          </Link>
        </div>
      )}
    </nav>
  );
}
