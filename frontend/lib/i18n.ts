export type Locale = "pt" | "en" | "es";
export const locales: Locale[] = ["pt", "en", "es"];
export const defaultLocale: Locale = "pt";
import { dictionary as pt } from "../dictionaries/pt";
import { dictionary as en } from "../dictionaries/en";
import { dictionary as es } from "../dictionaries/es";
export type Dictionary = {
  nav: { home: string; login: string; signup: string; logout: string; explore: string; myPosts: string; newPost: string };
  auth: {
    loginTitle: string;
    signupTitle: string;
    username: string;
    email: string;
    password: string;
    submit: string;
    or: string;
    goSignup: string;
    goLogin: string;
  };
  search: { label: string; button: string; noSuggestions: string };
  feed: { categories: string; tags: string; loadMoreError: string; end: string };
  comments: { title: string; noComments: string; submitError: string };
  related: { title: string };
  common: { loading: string };
};
const DICTIONARIES: Record<Locale, Dictionary> = { pt, en, es };
export function getDictionary(locale: Locale): Dictionary {
  return DICTIONARIES[locale] || DICTIONARIES[defaultLocale];
}
