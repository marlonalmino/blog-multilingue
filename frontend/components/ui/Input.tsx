import React from "react";

type Props = React.InputHTMLAttributes<HTMLInputElement> & { label?: string };

export default function Input({ label, className, ...props }: Props) {
  return (
    <div className="flex w-full flex-col gap-2">
      {label && <label className="text-sm text-zinc-600 dark:text-zinc-300">{label}</label>}
      <input
        className={`w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-zinc-900 outline-none focus:ring-2 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 ${className || ""}`}
        {...props}
      />
    </div>
  );
}
