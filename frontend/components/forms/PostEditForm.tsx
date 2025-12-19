"use client";
import Input from "../ui/Input";
import Button from "../ui/Button";
import { updatePost, deletePost, fetchMyPost, fetchMyPostLocales, updatePostLocale, createPostLocale } from "../../lib/api";
import type { Post, PostLocaleItem } from "../../lib/api";
import { getCsrf } from "../../lib/auth";
import { useEffect, useMemo, useState } from "react";
import type { Locale } from "../../lib/i18n";

export default function PostEditForm({ id, locale, dictSubmit }: { id: number; locale: Locale; dictSubmit: string }) {
  const [slugBase, setSlugBase] = useState("");
  const [status, setStatus] = useState("published");
  const [canonicalUrl, setCanonicalUrl] = useState("");
  const [isFeatured, setIsFeatured] = useState(false);
  const [coverMediaId, setCoverMediaId] = useState<number | null>(null);
  const [publishedAt, setPublishedAt] = useState<string>("");
  const [locId, setLocId] = useState<number | null>(null);
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [bodyMd, setBodyMd] = useState("");
  const [bodyHtml, setBodyHtml] = useState("");
  const [slugLocale, setSlugLocale] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const formattedPublishedAt = useMemo(() => {
    if (!publishedAt) return "";
    try {
      const d = new Date(publishedAt);
      const pad = (n: number) => String(n).padStart(2, "0");
      const yyyy = d.getFullYear();
      const mm = pad(d.getMonth() + 1);
      const dd = pad(d.getDate());
      const hh = pad(d.getHours());
      const min = pad(d.getMinutes());
      return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    } catch {
      return "";
    }
  }, [publishedAt]);
  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const post = await fetchMyPost(id);
        setSlugBase(post.slug_base || "");
        setStatus(post.status || "draft");
        setCanonicalUrl(post.canonical_url || "");
        setIsFeatured(!!post.is_featured);
        setCoverMediaId(post.cover_media ?? null);
        setPublishedAt(post.published_at || "");
        const locs = await fetchMyPostLocales();
        const current = locs.find((l) => l.post === id && l.locale === locale);
        if (current) {
          setLocId(current.id);
          setTitle(current.title || "");
          setSummary(current.summary || "");
          setBodyMd(current.body_md || "");
          setBodyHtml(current.body_html || "");
          setSlugLocale(current.slug_locale || "");
        } else {
          setLocId(null);
          setTitle("");
          setSummary("");
          setBodyMd("");
          setBodyHtml("");
          setSlugLocale(`${post.slug_base || ""}-${locale}`);
        }
      } catch {
        setError("Falha ao carregar dados do post");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id, locale]);
  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await getCsrf();
      const payloadPost: Partial<Post> & { published_at?: string | null } = {
        slug_base: slugBase || undefined,
        status,
        canonical_url: canonicalUrl || undefined,
        is_featured: isFeatured,
        cover_media: coverMediaId || undefined,
      };
      if (formattedPublishedAt) {
        const iso = new Date(formattedPublishedAt).toISOString();
        payloadPost.published_at = iso;
      }
      await updatePost(id, payloadPost);
      if (locId) {
        const payloadLocaleUpdate: Partial<PostLocaleItem> = {
          post: id,
          locale,
          title,
          summary,
          body_md: bodyMd,
          body_html: bodyHtml,
          slug_locale: slugLocale || `${slugBase}-${locale}`,
        };
        await updatePostLocale(locId, payloadLocaleUpdate);
      } else {
        const payloadLocaleCreate: Omit<PostLocaleItem, "id"> = {
          post: id,
          locale,
          title,
          summary,
          body_md: bodyMd,
          body_html: bodyHtml,
          slug_locale: slugLocale || `${slugBase}-${locale}`,
        };
        await createPostLocale(payloadLocaleCreate);
      }
      window.location.assign(`/${locale}/posts`);
    } catch {
      setError("Falha ao editar post");
    } finally {
      setLoading(false);
    }
  }
  async function onDelete() {
    setLoading(true);
    setError(null);
    try {
      await getCsrf();
      await deletePost(id);
      window.location.assign(`/${locale}/posts`);
    } catch {
      setError("Falha ao deletar post");
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-semibold">Editar Post #{id}</h1>
      <form className="flex flex-col gap-4" onSubmit={onSubmit}>
        <Input label="Slug base" value={slugBase} onChange={(e) => setSlugBase(e.target.value)} />
        <Input label="Status" value={status} onChange={(e) => setStatus(e.target.value)} />
        <Input label="Canonical URL" value={canonicalUrl} onChange={(e) => setCanonicalUrl(e.target.value)} />
        <div className="flex items-center gap-2">
          <input type="checkbox" checked={isFeatured} onChange={(e) => setIsFeatured(e.target.checked)} />
          <span className="text-sm">Destacar</span>
        </div>
        <Input label="Cover media ID" type="number" value={coverMediaId ?? ""} onChange={(e) => setCoverMediaId(e.target.value ? Number(e.target.value) : null)} />
        <input
          type="datetime-local"
          value={formattedPublishedAt}
          onChange={(e) => setPublishedAt(e.target.value)}
          className="w-full rounded-md border border-zinc-300 bg-white px-3 h-9 text-sm text-zinc-900 outline-none focus:ring-2 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
        />
        <h2 className="mt-4 text-lg font-semibold">Conteúdo ({locale})</h2>
        <Input label="Título" value={title} onChange={(e) => setTitle(e.target.value)} />
        <Input label="Resumo" value={summary} onChange={(e) => setSummary(e.target.value)} />
        <Input label="Body MD" value={bodyMd} onChange={(e) => setBodyMd(e.target.value)} />
        <Input label="Body HTML" value={bodyHtml} onChange={(e) => setBodyHtml(e.target.value)} />
        <Input label="Slug locale" value={slugLocale} onChange={(e) => setSlugLocale(e.target.value)} />
        {error && <div className="text-sm text-red-600">{error}</div>}
        <div className="flex gap-2">
          <Button type="submit" disabled={loading}>
            {dictSubmit}
          </Button>
          <Button type="button" disabled={loading} onClick={onDelete} className="bg-red-600 hover:bg-red-500 dark:bg-red-500 dark:hover:bg-red-400">
            Deletar
          </Button>
        </div>
      </form>
    </div>
  );
}
