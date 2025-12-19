import { getDictionary, Locale } from "../../../../lib/i18n";
import { getServerUser } from "../../../../lib/auth.server";
import { redirect } from "next/navigation";
import Link from "next/link";
import { fetchMyPosts, type Post } from "../../../../lib/api";
import { headers } from "next/headers";

export default async function MyPostsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const user = await getServerUser();
  if (!user) redirect(`/${locale}/login`);
  const dict = getDictionary(locale as Locale);
  const hdrs = await headers();
  const cookieHeader = hdrs.get("cookie") || "";
  const posts: Post[] = await fetchMyPosts(cookieHeader).catch(() => []);
  return (
    <div className="mx-auto max-w-4xl">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{dict.nav.home}</h1>
        <Link
          href={`/${locale}/posts/new`}
          className="rounded-md bg-zinc-900 px-3 py-2 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900"
        >
          Novo Post
        </Link>
      </div>
      <div className="space-y-3">
        {posts.map((p) => (
          <div key={p.id} className="flex items-center justify-between rounded border border-zinc-200 p-3 dark:border-zinc-800">
            <div>
              <div className="text-sm text-zinc-500">#{p.id}</div>
              <div className="font-medium">{p.slug_base}</div>
              <div className="text-xs text-zinc-500">{p.status}</div>
            </div>
            <div className="flex items-center gap-2">
              <Link href={`/${locale}/posts/${p.id}/edit`} className="text-sm text-blue-600 hover:underline dark:text-blue-400">
                Editar
              </Link>
            </div>
          </div>
        ))}
        {!posts.length && <div className="text-sm text-zinc-500">Você não tem posts</div>}
      </div>
    </div>
  );
}
