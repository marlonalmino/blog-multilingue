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
  user_username?: string | null;
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

// Posts CRUD (ownership)
export type Post = {
  id: number;
  slug_base: string;
  status: string;
  published_at: string | null;
  canonical_url: string;
  is_featured: boolean;
  author: number | null;
  cover_media: number | null;
};

export async function fetchMyPosts(cookieHeader?: string): Promise<Post[]> {
  const res = await fetch(`${API_BASE}/my-posts/`, {
    credentials: "include",
    headers: cookieHeader ? { cookie: cookieHeader } : undefined,
  });
  if (!res.ok) throw new Error("my_posts_failed");
  const json = await res.json();
  if (Array.isArray(json)) return json as Post[];
  if (json && Array.isArray(json.results)) return json.results as Post[];
  return [];
}

export async function createPost(payload: { slug_base: string; status?: string; canonical_url?: string; is_featured?: boolean }) {
  const res = await fetch(`${API_BASE}/my-posts/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("post_create_failed");
  return res.json();
}

export async function fetchMyPost(id: number, cookieHeader?: string): Promise<Post> {
  const res = await fetch(`${API_BASE}/my-posts/${id}/`, {
    credentials: "include",
    headers: cookieHeader ? { cookie: cookieHeader } : undefined,
  });
  if (!res.ok) throw new Error("my_post_failed");
  return res.json();
}

export async function updatePost(
  id: number,
  payload: Partial<{ slug_base: string; status: string; canonical_url: string; is_featured: boolean; published_at: string | null; cover_media: number | null }>
) {
  const res = await fetch(`${API_BASE}/my-posts/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("post_update_failed");
  return res.json();
}

export async function deletePost(id: number) {
  const res = await fetch(`${API_BASE}/my-posts/${id}/`, { method: "DELETE", credentials: "include" });
  if (!res.ok) throw new Error("post_delete_failed");
  return true;
}

// PostLocale CRUD (ownership)
export type PostLocaleItem = {
  id: number;
  post: number;
  locale: string;
  title: string;
  summary: string;
  body_md: string;
  body_html: string;
  slug_locale: string;
};

export async function fetchMyPostLocales(cookieHeader?: string): Promise<PostLocaleItem[]> {
  const res = await fetch(`${API_BASE}/my-post-locales/`, {
    credentials: "include",
    headers: cookieHeader ? { cookie: cookieHeader } : undefined,
  });
  if (!res.ok) throw new Error("my_post_locales_failed");
  const json = await res.json();
  if (Array.isArray(json)) return json as PostLocaleItem[];
  if (json && Array.isArray(json.results)) return json.results as PostLocaleItem[];
  return [];
}

export async function createPostLocale(payload: Omit<PostLocaleItem, "id">) {
  const res = await fetch(`${API_BASE}/my-post-locales/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("postlocale_create_failed");
  return res.json();
}

export async function updatePostLocale(id: number, payload: Partial<PostLocaleItem>) {
  const res = await fetch(`${API_BASE}/my-post-locales/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("postlocale_update_failed");
  return res.json();
}

export async function deletePostLocale(id: number) {
  const res = await fetch(`${API_BASE}/my-post-locales/${id}/`, { method: "DELETE", credentials: "include" });
  if (!res.ok) throw new Error("postlocale_delete_failed");
  return true;
}

