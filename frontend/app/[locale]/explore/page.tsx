import { getDictionary, Locale } from "../../../lib/i18n";
import { fetchFeed, fetchNavigation } from "../../../lib/api";
import FeedShell from "../../../components/FeedShell";

export default async function ExplorePage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ q?: string; category?: string; tag?: string }>;
}) {
  const { locale } = await params;
  const sp = await searchParams;
  const dict = getDictionary(locale as Locale);
  const initial = await fetchFeed({
    locale,
    q: sp?.q || undefined,
    category: sp?.category || undefined,
    tag: sp?.tag || undefined,
  });
  const navigation = await fetchNavigation({ locale });
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-4 text-2xl font-semibold">{dict.nav.explore}</h1>
      <FeedShell
        initial={initial}
        locale={locale}
        navigation={navigation}
        initialQ={sp?.q || ""}
        initialCategory={sp?.category || null}
        initialTag={sp?.tag || null}
      />
    </div>
  );
}
