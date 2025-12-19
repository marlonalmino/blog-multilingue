/** @jsxImportSource react */
"use client";
import { useEffect, useRef, useState } from "react";
import { fetchFeed, type FeedItem, type Paginated } from "../lib/api";
import PostCard from "./PostCard";
import { getDictionary, Locale } from "../lib/i18n";

export default function Feed({ initial, locale }: { initial: Paginated<FeedItem>; locale: string }) {
  const [data, setData] = useState<Paginated<FeedItem>>(initial);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sentinel = useRef<HTMLDivElement | null>(null);
  const dict = getDictionary(locale as Locale);
  useEffect(() => {
    setData(initial);
  }, [initial]);
  useEffect(() => {
    if (!sentinel.current) return;
    const observer = new IntersectionObserver(async (entries) => {
      const entry = entries[0];
      if (entry.isIntersecting && !loading && data.next) {
        setLoading(true);
        setError(null);
        try {
          const url = new URL(data.next);
          const page = Number(url.searchParams.get("page") || "2");
          const more = await fetchFeed({ locale, page });
          setData((prev) => ({
            ...more,
            results: [...(prev?.results || []), ...(more?.results || [])],
          }));
        } catch {
          setError("load_failed");
        } finally {
          setLoading(false);
        }
      }
    });
    observer.observe(sentinel.current);
    return () => observer.disconnect();
  }, [data.next, loading, locale]);
  return (
    <div className="flex flex-col gap-4">
      {data.results.map((item) => (
        <PostCard key={`${item.post}-${item.slug_locale}`} item={item} locale={locale} />
      ))}
      {error && <div className="text-sm text-red-600">{dict.feed.loadMoreError}</div>}
      <div ref={sentinel} />
      {loading && <div className="text-sm text-zinc-500">{dict.common.loading}</div>}
      {!data.next && <div className="py-4 text-center text-sm text-zinc-500">{dict.feed.end}</div>}
    </div>
  );
}
