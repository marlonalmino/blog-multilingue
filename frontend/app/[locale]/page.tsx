import { getDictionary, Locale } from "../../lib/i18n";
import { getServerUser } from "../../lib/auth.server";
import { redirect } from "next/navigation";
import { fetchFeed, fetchNavigation } from "../../lib/api";
import FeedShell from "../../components/FeedShell";

export default async function LocaleHome({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ q?: string; category?: string; tag?: string }>;
}) {
  const { locale } = await params;
  const sp = await searchParams;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
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
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{dict.nav.home}</h1>
        <div className="flex items-center gap-2">
          <a
            href={`/${locale}/explore`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.explore}
          </a>
          <a
            href={`/${locale}/posts`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.myPosts}
          </a>
          <a
            href={`/${locale}/posts/new`}
            className="rounded-full border border-zinc-300 px-3 py-1 text-xs text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {dict.nav.newPost}
          </a>
        </div>
      </div>
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
