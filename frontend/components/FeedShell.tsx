"use client";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { FeedItem, Paginated } from "../lib/api";
import { fetchFeed } from "../lib/api";
import SearchBar from "./SearchBar";
import Feed from "./Feed";
import { getDictionary, Locale } from "../lib/i18n";

export default function FeedShell({
  locale,
  initial,
  navigation,
  initialQ,
  initialCategory,
  initialTag,
}: {
  locale: string;
  initial: Paginated<FeedItem>;
  navigation: { categories: { name: string; slug: string; count: number }[]; tags: { name: string; slug: string; count: number }[] };
  initialQ?: string;
  initialCategory?: string | null;
  initialTag?: string | null;
}) {
  const router = useRouter();
  const dict = getDictionary(locale as Locale);
  const [q, setQ] = useState(initialQ || "");
  const [category, setCategory] = useState<string | null>(initialCategory || null);
  const [tag, setTag] = useState<string | null>(initialTag || null);
  const [current, setCurrent] = useState<Paginated<FeedItem>>(initial);
  const [loading, setLoading] = useState(false);
  const params = useMemo(
    () => ({ locale, q: q || undefined, category: category || undefined, tag: tag || undefined }),
    [locale, q, category, tag]
  );
  const queryKey = useMemo(() => `${locale}|${q}|${category || ""}|${tag || ""}`, [locale, q, category, tag]);
  useEffect(() => {
    const qs = new URLSearchParams();
    if (q) qs.set("q", q);
    if (category) qs.set("category", category);
    if (tag) qs.set("tag", tag);
    const search = qs.toString();
    router.replace(`/${locale}${search ? `?${search}` : ""}`);
  }, [locale, q, category, tag, router]);
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
        {loading && <div className="text-sm text-zinc-500">{dict.common.loading}</div>}
      </div>
      <aside className="space-y-6">
        <div>
          <h3 className="mb-2 text-sm font-semibold">{dict.feed.categories}</h3>
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
          <h3 className="mb-2 text-sm font-semibold">{dict.feed.tags}</h3>
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
