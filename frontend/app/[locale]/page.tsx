import { getDictionary, Locale } from "../../lib/i18n";
import { getServerUser } from "../../lib/auth.server";
import { redirect } from "next/navigation";
import { fetchFeed, fetchNavigation } from "../../lib/api";
import FeedShell from "../../components/FeedShell";

export default async function LocaleHome({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
  const dict = getDictionary(locale as Locale);
  const initial = await fetchFeed({ locale });
  const navigation = await fetchNavigation({ locale });
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-4 text-2xl font-semibold">{dict.nav.home}</h1>
      <FeedShell initial={initial} locale={locale} navigation={navigation} />
    </div>
  );
}
