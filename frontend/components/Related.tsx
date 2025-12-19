import { fetchRelated, type FeedItem } from "../lib/api";
import PostCard from "./PostCard";
import { getDictionary, Locale } from "../lib/i18n";

export default async function Related({ locale, slug }: { locale: string; slug: string }) {
  const items: FeedItem[] = await fetchRelated({ locale, slug, limit: 6 }).catch(() => []);
  if (!items.length) return null;
  const dict = getDictionary(locale as Locale);
  return (
    <section>
      <h2 className="mb-4 text-xl font-semibold">{dict.related.title}</h2>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {items.map((i) => (
          <PostCard key={`${i.post}-${i.slug_locale}`} item={i} locale={locale} />
        ))}
      </div>
    </section>
  );
}
