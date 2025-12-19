/** @jsxImportSource react */
"use client";
import { useEffect, useState } from "react";
import type { Dictionary } from "../lib/i18n";
import { createComment, fetchComments, type CommentItem } from "../lib/api";
import { getCsrf, me } from "../lib/auth";
import Button from "./ui/Button";
import Input from "./ui/Input";

export default function Comments({ postId, dict }: { postId: number; dict: Dictionary }) {
  const [items, setItems] = useState<CommentItem[]>([]);
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    fetchComments({ postId, status: "approved" })
      .then(setItems)
      .catch(() => setItems([]));
  }, [postId]);
  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const user = await me().catch(() => null);
      await getCsrf();
      const created = await createComment({ postId, body, userId: user?.id });
      setItems((prev) => [...prev, created]);
      setBody("");
    } catch {
      setError(dict.comments.submitError);
    } finally {
      setLoading(false);
    }
  }
  return (
    <section>
      <h2 className="mb-4 text-xl font-semibold">{dict.comments.title}</h2>
      <div className="mb-6 space-y-3">
        {items.map((c) => (
          <div key={c.id} className="rounded border border-zinc-200 p-3 text-sm dark:border-zinc-800">
            <div className="mb-1 text-xs text-zinc-500">{new Date(c.created_at).toLocaleString()}</div>
            <div className="mb-1">
              <span className="mr-2 font-medium">{c.user_username ? c.user_username : "Anônimo"}</span>
            </div>
            <div>{c.body}</div>
          </div>
        ))}
        {!items.length && <div className="text-sm text-zinc-500">{dict.comments.noComments}</div>}
      </div>
      <form className="flex flex-col gap-3" onSubmit={onSubmit}>
        <Input label={dict.comments.title} value={body} onChange={(e) => setBody(e.target.value)} required />
        {error && <div className="text-sm text-red-600">{error}</div>}
        <Button type="submit" disabled={loading}>
          {dict.auth.submit}
        </Button>
      </form>
    </section>
  );
}

