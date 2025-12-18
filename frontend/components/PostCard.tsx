import Link from "next/link";
import type { FeedItem } from "../lib/api";

export default function PostCard({ item, locale }: { item: FeedItem; locale: string }) {
  return (
    <article className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">
          <Link href={`/${locale}/post/${item.slug_locale}`}>{item.title}</Link>
        </h2>
        <time className="text-xs text-zinc-500">{new Date(item.published_at).toLocaleDateString()}</time>
      </div>
      <p className="mt-2 text-zinc-700 dark:text-zinc-300">{item.summary}</p>
      <div className="mt-3 flex flex-wrap gap-2 text-xs">
        {item.categories.map((c) => (
          <span key={c.slug} className="rounded bg-zinc-200 px-2 py-1 dark:bg-zinc-800">
            {c.name}
          </span>
        ))}
        {item.tags.map((t) => (
          <span key={t.slug} className="rounded bg-zinc-200 px-2 py-1 dark:bg-zinc-800">
            #{t.name}
          </span>
        ))}
      </div>
    </article>
  );
}

