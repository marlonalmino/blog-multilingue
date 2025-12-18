"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { fetchSuggest } from "../lib/api";
import Input from "./ui/Input";
import Link from "next/link";

export default function SearchBar({ locale, onSearch }: { locale: string; onSearch: (q: string) => void }) {
  const [q, setQ] = useState("");
  const [items, setItems] = useState<{ title: string; slug: string }[]>([]);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);
  useEffect(() => {
    const t = setTimeout(async () => {
      if (!q.trim()) {
        setItems([]);
        return;
      }
      try {
        const data = await fetchSuggest({ locale, q, limit: 8 });
        setItems(data);
        setOpen(true);
      } catch {
        setItems([]);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, locale]);
  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(q.trim());
    setOpen(false);
  };
  const dropdown = useMemo(
    () => (
      <div className="absolute z-10 mt-1 w-full rounded-md border border-zinc-200 bg-white p-2 shadow-sm dark:border-zinc-800 dark:bg-black">
        {items.length ? (
          items.map((s) => (
            <Link
              key={s.slug}
              href={`/${locale}/post/${s.slug}`}
              className="block rounded px-2 py-1 text-sm hover:bg-zinc-100 dark:hover:bg-zinc-900"
              onClick={() => setOpen(false)}
            >
              {s.title}
            </Link>
          ))
        ) : (
          <div className="px-2 py-1 text-sm text-zinc-500">Sem sugestões</div>
        )}
      </div>
    ),
    [items, locale]
  );
  return (
    <div ref={ref} className="relative">
      <form onSubmit={onSubmit} className="flex gap-2">
        <Input label="Buscar" value={q} onChange={(e) => setQ(e.target.value)} />
        <button className="rounded bg-zinc-900 px-3 py-2 text-white dark:bg-zinc-100 dark:text-zinc-900" type="submit">
          Buscar
        </button>
      </form>
      {open && dropdown}
    </div>
  );
}

