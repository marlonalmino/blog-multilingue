import React from "react";

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { full?: boolean };

export default function Button({ className, full, ...props }: Props) {
  return (
    <button
      className={`${full ? "w-full" : ""} rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300 ${className || ""}`}
      {...props}
    />
  );
}
