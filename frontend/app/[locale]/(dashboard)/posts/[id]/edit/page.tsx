import { getDictionary, Locale } from "../../../../../../lib/i18n";
import { getServerUser } from "../../../../../../lib/auth.server";
import { redirect } from "next/navigation";
import PostEditForm from "../../../../../../components/forms/PostEditForm";

export default async function EditPostPage({ params }: { params: Promise<{ locale: string; id: string }> }) {
  const { locale, id } = await params;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
  const dict = getDictionary(locale as Locale);
  return <PostEditForm id={Number(id)} locale={locale as Locale} dictSubmit={dict.auth.submit} />;
}
