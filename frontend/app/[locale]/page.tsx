import { getDictionary, Locale } from "../../lib/i18n";
import { getServerUser } from "../../lib/auth.server";
import { redirect } from "next/navigation";

export default async function LocaleHome({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
  const dict = getDictionary(locale as Locale);
  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-4 text-2xl font-semibold">{dict.nav.home}</h1>
      <p className="text-zinc-700 dark:text-zinc-300">Bem-vindo! Em breve: feed inicial e posts.</p>
    </div>
  );
}
