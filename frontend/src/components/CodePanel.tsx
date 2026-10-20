import { CheckCircle2, Code2, XCircle } from "lucide-react";

type Props = {
  title: string;
  subtitle: string;
  code: string;
  variant: "buggy" | "fixed";
};

export function CodePanel({ title, subtitle, code, variant }: Props) {
  const buggy = variant === "buggy";
  return (
    <article className={`overflow-hidden rounded-3xl border bg-white shadow-soft ${buggy ? "border-rose-200" : "border-emerald-200"}`}>
      <div className={`flex items-center justify-between border-b px-5 py-4 ${buggy ? "border-rose-100 bg-rose-50/70" : "border-emerald-100 bg-emerald-50/70"}`}>
        <div className="flex items-center gap-3">
          <span className={`grid h-9 w-9 place-items-center rounded-xl ${buggy ? "bg-rose-100 text-rose-600" : "bg-emerald-100 text-emerald-600"}`}>
            {buggy ? <XCircle size={18} /> : <CheckCircle2 size={18} />}
          </span>
          <div>
            <h3 className="text-sm font-extrabold text-slate-900">{title}</h3>
            <p className="text-xs text-slate-500">{subtitle}</p>
          </div>
        </div>
        <Code2 size={18} className="text-slate-400" />
      </div>
      <pre className="code-font min-h-64 overflow-x-auto p-5 text-sm leading-7 text-slate-700"><code>{code}</code></pre>
    </article>
  );
}
