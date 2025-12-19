"use client";
import { useEffect, useMemo, useState } from "react";
import type { FeedItem, Paginated } from "../lib/api";
import { fetchFeed } from "../lib/api";
import SearchBar from "./SearchBar";
import Feed from "./Feed";

export default function FeedShell({
  locale,
  initial,
  navigation,
}: {
  locale: string;
  initial: Paginated<FeedItem>;
  navigation: { categories: { name: string; slug: string; count: number }[]; tags: { name: string; slug: string; count: number }[] };
}) {
  const [q, setQ] = useState("");
  const [category, setCategory] = useState<string | null>(null);
  const [tag, setTag] = useState<string | null>(null);
  const [current, setCurrent] = useState<Paginated<FeedItem>>(initial);
  const [loading, setLoading] = useState(false);
  const params = useMemo(
    () => ({ locale, q: q || undefined, category: category || undefined, tag: tag || undefined }),
    [locale, q, category, tag]
  );
  const queryKey = useMemo(() => `${locale}|${q}|${category || ""}|${tag || ""}`, [locale, q, category, tag]);
  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const data = await fetchFeed(params);
        setCurrent(data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [queryKey, params]);
  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-[1fr_280px]">
      <div className="space-y-4">
        <SearchBar locale={locale} onSearch={(v) => setQ(v)} />
        <Feed initial={current} locale={locale} />
        {loading && <div className="text-sm text-zinc-500">Carregando...</div>}
      </div>
      <aside className="space-y-6">
        <div>
          <h3 className="mb-2 text-sm font-semibold">Categorias</h3>
          <div className="flex flex-wrap gap-2">
            {navigation.categories.map((c) => (
              <button
                key={c.slug}
                className={`rounded px-2 py-1 text-sm ${category === c.slug ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900" : "bg-zinc-200 dark:bg-zinc-800"}`}
                onClick={() => setCategory(category === c.slug ? null : c.slug)}
              >
                {c.name} ({c.count})
              </button>
            ))}
          </div>
        </div>
        <div>
          <h3 className="mb-2 text-sm font-semibold">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {navigation.tags.map((t) => (
              <button
                key={t.slug}
                className={`rounded px-2 py-1 text-sm ${tag === t.slug ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900" : "bg-zinc-200 dark:bg-zinc-800"}`}
                onClick={() => setTag(tag === t.slug ? null : t.slug)}
              >
                #{t.name} ({t.count})
              </button>
            ))}
          </div>
        </div>
      </aside>
    </div>
  );
}

