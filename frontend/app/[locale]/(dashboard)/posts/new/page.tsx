import { getDictionary, Locale } from "../../../../../lib/i18n";
import { getServerUser } from "../../../../../lib/auth.server";
import { redirect } from "next/navigation";
import PostNewForm from "../../../../../components/forms/PostNewForm";

export default async function NewPostPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
  const dict = getDictionary(locale as Locale);
  return (
    <PostNewForm locale={locale as Locale} dictSubmit={dict.auth.submit} />
  );
}
