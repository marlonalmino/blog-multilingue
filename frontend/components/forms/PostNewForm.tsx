"use client";
import Input from "../ui/Input";
import Button from "../ui/Button";
import { createPost, createPostLocale } from "../../lib/api";
import { getCsrf } from "../../lib/auth";
import { useState } from "react";
import type { Locale } from "../../lib/i18n";

export default function PostNewForm({ locale, dictSubmit }: { locale: Locale; dictSubmit: string }) {
  const [slugBase, setSlugBase] = useState("");
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await getCsrf();
      const post = await createPost({ slug_base: slugBase, status: "published" });
      await createPostLocale({
        post: post.id,
        locale,
        title,
        summary,
        body_md: body,
        body_html: `<p>${body}</p>`,
        slug_locale: `${slugBase}-${locale}`,
      });
      window.location.assign(`/${locale}/posts`);
    } catch {
      setError("Falha ao criar post");
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-semibold">Novo Post</h1>
      <form className="flex flex-col gap-4" onSubmit={onSubmit}>
        <Input label="Slug base" value={slugBase} onChange={(e) => setSlugBase(e.target.value)} required />
        <Input label="Título" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <Input label="Resumo" value={summary} onChange={(e) => setSummary(e.target.value)} />
        <Input label="Conteúdo" value={body} onChange={(e) => setBody(e.target.value)} required />
        {error && <div className="text-sm text-red-600">{error}</div>}
        <Button type="submit" disabled={loading}>
          {dictSubmit}
        </Button>
      </form>
    </div>
  );
}
