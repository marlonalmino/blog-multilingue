"use client";
import { useState } from "react";
import Input from "../../../../components/ui/Input";
import Button from "../../../../components/ui/Button";
import { getDictionary, Locale } from "../../../../lib/i18n";
import { getCsrf, login, notifyAuthChanged, me } from "../../../../lib/auth";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

export default function LoginPage() {
  const pathname = usePathname();
  const locale = (pathname.split("/")[1] ?? "pt") as Locale;
  const dict = getDictionary(locale);
  useEffect(() => {
    me()
      .then(() => {
        window.location.assign(`/${locale}`);
      })
      .catch(() => {});
  }, [locale]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await getCsrf();
      await login({ username, password });
      notifyAuthChanged();
      window.location.assign(`/${locale}`);
    } catch {
      setError("Login falhou");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md">
      <h1 className="mb-6 text-2xl font-semibold">{dict.auth.loginTitle}</h1>
      <form className="flex flex-col gap-4" onSubmit={onSubmit}>
        <Input label={dict.auth.username} value={username} onChange={(e) => setUsername(e.target.value)} required />
        <Input label={dict.auth.password} type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error && <div className="text-sm text-red-600">{error}</div>}
        <Button type="submit" full disabled={loading}>
          {dict.auth.submit}
        </Button>
      </form>
    </div>
  );
}
