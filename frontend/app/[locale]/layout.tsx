import type { Metadata } from "next";
import "../globals.css";
import { getDictionary, Locale } from "../../lib/i18n";
import NavBar from "../../components/NavBar";
import { getServerUser } from "../../lib/auth.server";

export const metadata: Metadata = {
  title: "Blog Multilingue",
  description: "Conteúdo em múltiplos idiomas",
};

export default async function LocaleLayout({ children, params }: { children: React.ReactNode; params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const dict = getDictionary(locale as Locale);
  const user = await getServerUser();
  return (
    <div className="min-h-screen bg-background text-foreground">
      <NavBar locale={locale as Locale} dict={dict} initialUser={user || undefined} />
      <main className="mx-auto max-w-4xl px-6 py-8">{children}</main>
    </div>
  );
}
