import { fetchPostDetail } from "../../../../lib/api";
import { getDictionary, Locale } from "../../../../lib/i18n";
import Comments from "../../../../components/Comments";
import Related from "../../../../components/Related";

export default async function PostDetailPage({ params }: { params: Promise<{ locale: string; slug: string }> }) {
  const { locale, slug } = await params;
  const dict = getDictionary(locale as Locale);
  const post = await fetchPostDetail({ locale, slug });
  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-2 text-3xl font-bold">{post.title}</h1>
      <p className="mb-6 text-zinc-700 dark:text-zinc-300">{post.summary}</p>
      <article
        className="prose prose-zinc dark:prose-invert"
        dangerouslySetInnerHTML={{ __html: post.body_html || `<pre>${post.body_md}</pre>` }}
      />
      <hr className="my-8 border-zinc-200 dark:border-zinc-800" />
      <Comments postId={post.post} dict={dict} />
      <hr className="my-8 border-zinc-200 dark:border-zinc-800" />
      <Related locale={locale} slug={post.slug_locale} />
    </div>
  );
}

