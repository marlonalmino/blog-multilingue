import React from "react";

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { full?: boolean };

export default function Button({ className, full, ...props }: Props) {
  return (
    <button
      className={`${full ? "w-full" : ""} inline-flex items-center justify-center rounded-full px-3 py-1 text-sm bg-zinc-900 text-white hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 ${className || ""}`}
      {...props}
    />
  );
}
