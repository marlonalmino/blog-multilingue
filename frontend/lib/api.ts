import { API_BASE } from "./config";

export type FeedItem = {
  id: number;
  post: number;
  locale: string;
  title: string;
  summary: string;
  slug_locale: string;
  cover: string | null;
  published_at: string;
  categories: { name: string; slug: string }[];
  tags: { name: string; slug: string }[];
};

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export async function fetchFeed(params: {
  locale: string;
  page?: number;
  q?: string;
  category?: string;
  tag?: string;
  featured?: boolean;
}): Promise<Paginated<FeedItem>> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  if (params.page) query.set("page", String(params.page));
  if (params.q) query.set("q", params.q);
  if (params.category) query.set("category", params.category);
  if (params.tag) query.set("tag", params.tag);
  if (params.featured) query.set("featured", "true");
  const res = await fetch(`${API_BASE}/feed?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("feed_failed");
  return res.json();
}

export type PostDetail = {
  id: number;
  post: number;
  locale: string;
  title: string;
  summary: string;
  body_md: string;
  body_html: string;
  slug_locale: string;
  categories: { name: string; slug: string }[];
  tags: { name: string; slug: string }[];
  embeds: { url: string; provider: string; position: number; metadata: Record<string, unknown> }[];
};

export async function fetchPostDetail(params: { locale: string; slug: string }): Promise<PostDetail> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  query.set("slug", params.slug);
  const res = await fetch(`${API_BASE}/post?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("post_failed");
  return res.json();
}

export async function fetchFeatured(params: { locale: string; limit?: number }): Promise<FeedItem[]> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  if (params.limit) query.set("limit", String(params.limit));
  const res = await fetch(`${API_BASE}/featured?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("featured_failed");
  return res.json();
}

export async function fetchRelated(params: { locale: string; slug: string; limit?: number }): Promise<FeedItem[]> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  query.set("slug", params.slug);
  if (params.limit) query.set("limit", String(params.limit));
  const res = await fetch(`${API_BASE}/related?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("related_failed");
  return res.json();
}

export async function fetchNavigation(params: { locale: string }): Promise<{
  categories: { name: string; slug: string; count: number }[];
  tags: { name: string; slug: string; count: number }[];
}> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  const res = await fetch(`${API_BASE}/navigation?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("navigation_failed");
  return res.json();
}

export async function fetchSuggest(params: { locale: string; q: string; limit?: number }): Promise<{ title: string; slug: string }[]> {
  const query = new URLSearchParams();
  query.set("locale", params.locale);
  query.set("q", params.q);
  if (params.limit) query.set("limit", String(params.limit));
  const res = await fetch(`${API_BASE}/suggest?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("suggest_failed");
  return res.json();
}

export type CommentItem = {
  id: number;
  post: number;
  user: number | null;
  parent: number | null;
  body: string;
  status: string;
  created_at: string;
};

export async function fetchComments(params: { postId: number; status?: string }): Promise<CommentItem[]> {
  const query = new URLSearchParams();
  query.set("post", String(params.postId));
  if (params.status) query.set("status", params.status);
  const res = await fetch(`${API_BASE}/comments?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("comments_failed");
  const json = await res.json();
  if (Array.isArray(json)) return json as CommentItem[];
  if (json && Array.isArray(json.results)) return json.results as CommentItem[];
  return [];
}

export async function createComment(payload: { postId: number; body: string; userId?: number }) {
  const res = await fetch(`${API_BASE}/comments/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ post: payload.postId, body: payload.body, user: payload.userId }),
  });
  if (!res.ok) throw new Error("comment_create_failed");
  return res.json();
}

