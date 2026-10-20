import { Check, Lightbulb, ListChecks } from "lucide-react";
import type { DebugExample } from "../types";

export function ReportSection({ example }: { example: DebugExample }) {
  return (
    <section id="report" className="scroll-mt-24 py-24">
      <div className="mb-8"><div className="mb-2 text-xs font-extrabold uppercase tracking-[.2em] text-violet">03 / Нәтиже</div><h2 className="text-3xl font-extrabold tracking-tight md:text-4xl">Debugging есебі</h2></div>
      <div className="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
        <div className="rounded-3xl bg-[#15162b] p-6 text-white">
          <div className="mb-5 flex items-center gap-2 text-sm font-bold"><ListChecks size={18} className="text-violet-300" />Автоматтандырылған тесттер</div>
          {example.tests.map((test) => <div key={test.name} className="mb-3 rounded-xl bg-white/10 p-3"><div className="flex items-center justify-between text-sm font-bold">{test.name}<Check size={16} className="text-emerald-400" /></div><div className="code-font mt-1 text-xs text-slate-400">{test.result}</div></div>)}
          <div className="mt-5 border-t border-white/10 pt-4 text-sm font-bold text-emerald-300">Барлығы өтті: {example.tests.length}/{example.tests.length}</div>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          {Object.entries(example.report).map(([key, value]) => <article key={key} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft"><div className="mb-2 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-violet"><Lightbulb size={14} />{key}</div><p className="text-sm leading-6 text-slate-600">{value}</p></article>)}
        </div>
      </div>
    </section>
  );
}
