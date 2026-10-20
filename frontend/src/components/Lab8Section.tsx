import {
  AlertTriangle,
  Braces,
  Check,
  CheckCircle2,
  CirclePlay,
  ClipboardCheck,
  Copy,
  FileCode2,
  Gauge,
  GitCompareArrows,
  ListChecks,
  ScanSearch,
  ShieldAlert,
  TerminalSquare,
  Wrench,
} from "lucide-react";
import type { Lab8Case, Lab8RunResult } from "../types";
import { CodePanel } from "./CodePanel";

type Props = {
  labCase: Lab8Case;
  runResult: Lab8RunResult | null;
  running: boolean;
  onRun: () => void;
};

function severityClass(severity: string) {
  if (severity === "Critical") return "bg-rose-100 text-rose-700";
  if (severity === "High") return "bg-orange-100 text-orange-700";
  if (severity === "Medium") return "bg-amber-100 text-amber-700";
  return "bg-slate-100 text-slate-600";
}

export function Lab8Section({ labCase, runResult, running, onRun }: Props) {
  return (
    <section id="lab8" className="scroll-mt-24 border-t border-slate-200 py-24">
      <div className="mb-9 flex flex-wrap items-end justify-between gap-5">
        <div>
          <div className="mb-2 text-xs font-extrabold uppercase tracking-[.2em] text-violet">04 / 8-зертханалық жұмыс</div>
          <h2 className="max-w-4xl text-3xl font-extrabold tracking-tight md:text-4xl">Static Analysis және Code Review</h2>
          <p className="mt-3 max-w-3xl text-slate-500">{labCase.summary}</p>
        </div>
        <div className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-extrabold text-emerald-700"><CheckCircle2 className="mr-2 inline" size={17} />20/20 орындалды</div>
      </div>

      <div className="mb-8 grid gap-4 md:grid-cols-2">
        <article className="rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <div className="mb-3 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-rose-700"><FileCode2 size={16} />Бастапқы scope</div>
          {labCase.source_files.map((file) => <div key={file} className="code-font break-all text-sm leading-7 text-rose-950">{file}</div>)}
        </article>
        <article className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
          <div className="mb-3 flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-emerald-700"><FileCode2 size={16} />Түзетілген scope</div>
          {labCase.fixed_files.map((file) => <div key={file} className="code-font break-all text-sm leading-7 text-emerald-950">{file}</div>)}
        </article>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        <CodePanel title="Before — сапасыз код" subtitle="eval, shell=True, mutable default және undefined name" code={labCase.buggy_code} variant="buggy" />
        <CodePanel title="After — түзетілген код" subtitle="typing, Decimal, validation және шағын функциялар" code={labCase.fixed_code} variant="fixed" />
      </div>

      <div className="mt-8 grid gap-5 lg:grid-cols-[1.15fr_.85fr]">
        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
          <div className="mb-5 flex items-center gap-2 font-extrabold"><ListChecks size={19} className="text-violet" />Coding Standards</div>
          <div className="grid gap-3 sm:grid-cols-2">
            {labCase.standards.map((standard) => <div key={standard} className="flex gap-3 rounded-xl bg-slate-50 p-3 text-sm"><Check size={17} className="mt-0.5 shrink-0 text-emerald-600" /><span>{standard}</span></div>)}
          </div>
        </article>
        <article className="rounded-3xl bg-[#15162b] p-6 text-white shadow-soft">
          <div className="mb-5 flex items-center gap-2 font-extrabold"><TerminalSquare size={19} className="text-violet-300" />Analysis құралдары</div>
          <div className="space-y-3">
            {labCase.tools.map((tool) => <div key={tool.name} className="rounded-xl border border-white/10 p-4"><div className="flex justify-between gap-3 font-bold"><span>{tool.name}</span><code className="text-violet-300">{tool.version}</code></div><p className="mt-1 text-xs text-slate-400">{tool.purpose}</p></div>)}
          </div>
          <code className="mt-5 block rounded-xl bg-black/20 p-4 text-xs leading-6 text-slate-300">npm run lab8</code>
        </article>
      </div>

      <div className="mt-8 grid gap-5 lg:grid-cols-[1.25fr_.75fr]">
        <article className="overflow-hidden rounded-3xl border border-amber-200 bg-white shadow-soft">
          <div className="flex items-center gap-2 border-b border-amber-100 bg-amber-50 p-6 font-extrabold text-amber-800"><AlertTriangle size={19} />Warning / Issue тізімі</div>
          <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-400"><tr><th className="px-5 py-3">Код</th><th className="px-5 py-3">Саны</th><th className="px-5 py-3">Мәселе</th><th className="px-5 py-3">Severity</th></tr></thead><tbody>{labCase.warnings.map((item) => <tr key={item.code} className="border-t border-slate-100"><td className="code-font px-5 py-3 font-bold">{item.code}</td><td className="px-5 py-3">{item.count}</td><td className="px-5 py-3 text-slate-600">{item.description}</td><td className="px-5 py-3"><span className={`rounded-full px-2 py-1 text-xs font-bold ${severityClass(item.severity)}`}>{item.severity}</span></td></tr>)}</tbody></table></div>
        </article>
        <article className="rounded-3xl border border-rose-200 bg-rose-50 p-6">
          <div className="mb-5 flex items-center gap-2 font-extrabold text-rose-700"><AlertTriangle size={19} />Error тізімі</div>
          {labCase.errors.map((item) => <div key={item.code} className="rounded-2xl bg-white p-5"><code className="font-extrabold text-rose-700">{item.code}</code><p className="mt-3 text-sm leading-6 text-rose-950">{item.description}</p><span className={`mt-4 inline-block rounded-full px-2 py-1 text-xs font-bold ${severityClass(item.severity)}`}>{item.severity}</span></div>)}
          <div className="mt-5 rounded-xl border border-rose-200 p-4 text-sm font-bold text-rose-800">Before: Ruff 11 issue · Pylint 10 message · 7.41/10</div>
        </article>
      </div>

      <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft"><div className="mb-4 flex items-center gap-2 font-extrabold"><Braces size={18} className="text-violet" />Code Smell</div><div className="space-y-2">{labCase.code_smells.map((smell) => <div key={smell} className="rounded-lg bg-slate-50 px-3 py-2 text-xs font-bold">{smell}</div>)}</div></article>
        <article className="rounded-3xl border border-sky-200 bg-sky-50 p-6"><div className="mb-4 flex items-center gap-2 font-extrabold text-sky-800"><Copy size={18} />Duplicate Code</div><p className="text-sm leading-7 text-sky-950">{labCase.duplicate_evidence}</p></article>
        <article className="rounded-3xl border border-violet/20 bg-violet/5 p-6"><div className="mb-4 flex items-center gap-2 font-extrabold"><Gauge size={18} className="text-violet" />Complexity</div>{labCase.complexity.map((row) => <div key={row.stage} className="mb-3 rounded-xl bg-white p-3 text-xs"><b>{row.stage}</b><div className="mt-2 text-slate-500">Max CC: <strong className="text-slate-800">{row.max_cc}</strong></div><div className="mt-1 text-slate-500">Average: <strong className="text-slate-800">{row.average}</strong></div></div>)}</article>
        <article className="rounded-3xl border border-rose-200 bg-rose-50 p-6"><div className="mb-4 flex items-center gap-2 font-extrabold text-rose-700"><ShieldAlert size={18} />Security</div>{labCase.security_issues.map((issue) => <div key={issue.code} className="mb-3 rounded-xl bg-white p-3"><div className="flex items-center justify-between gap-2"><code className="text-xs font-extrabold">{issue.code}</code><span className={`rounded-full px-2 py-1 text-[10px] font-bold ${severityClass(issue.severity)}`}>{issue.severity}</span></div><p className="mt-2 text-xs text-slate-600">{issue.description}</p></div>)}</article>
      </div>

      <article className="mt-8 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
        <div className="flex items-center gap-2 border-b border-slate-100 p-6 font-extrabold"><ScanSearch size={19} className="text-violet" />Қолмен тексеру: 10 кемшілік және Severity</div>
        <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-400"><tr><th className="px-4 py-3">№</th><th className="px-4 py-3">Кемшілік</th><th className="px-4 py-3">Severity</th><th className="px-4 py-3">Табу тәсілі</th><th className="px-4 py-3">Түзету</th></tr></thead><tbody>{labCase.deficiencies.map((item) => <tr key={item.id} className="border-t border-slate-100"><td className="px-4 py-3 font-bold">{item.id}</td><td className="px-4 py-3 font-semibold">{item.problem}</td><td className="px-4 py-3"><span className={`rounded-full px-2 py-1 text-xs font-bold ${severityClass(item.severity)}`}>{item.severity}</span></td><td className="px-4 py-3 text-slate-500">{item.detection}</td><td className="px-4 py-3 text-emerald-700">{item.fix}</td></tr>)}</tbody></table></div>
        <div className="border-t border-slate-100 bg-slate-50 px-6 py-4 text-sm font-bold">Critical — 2 · High — 4 · Medium — 3 · Low — 1</div>
      </article>

      <div className="mt-8 grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft"><div className="mb-5 flex items-center gap-2 font-extrabold"><ClipboardCheck size={19} className="text-violet" />Code Review Checklist</div><div className="space-y-3">{labCase.checklist.map((item) => <div key={item} className="flex gap-3 text-sm"><CheckCircle2 size={18} className="shrink-0 text-emerald-600" /><span>{item}</span></div>)}</div></article>
        <article className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft"><div className="flex items-center gap-2 border-b border-slate-100 p-6 font-extrabold"><GitCompareArrows size={19} className="text-violet" />Before / After метрикалары</div><div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-400"><tr><th className="px-5 py-3">Көрсеткіш</th><th className="px-5 py-3 text-rose-600">Before</th><th className="px-5 py-3 text-emerald-600">After</th><th className="px-5 py-3">Өзгеріс</th></tr></thead><tbody>{labCase.metrics.map((row) => <tr key={row.metric} className="border-t border-slate-100"><td className="px-5 py-3 font-bold">{row.metric}</td><td className="px-5 py-3 text-rose-700">{row.before}</td><td className="px-5 py-3 text-emerald-700">{row.after}</td><td className="px-5 py-3 font-bold text-violet">{row.change}</td></tr>)}</tbody></table></div></article>
      </div>

      <article className="mt-8 overflow-hidden rounded-3xl border border-emerald-200 bg-white shadow-soft">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-emerald-100 bg-emerald-50 p-6"><div><div className="flex items-center gap-2 font-extrabold text-emerald-800"><Wrench size={19} />Quality Gate</div><p className="mt-1 text-sm text-emerald-700">Түзетілген кодтың қабылдау шарттары.</p></div><button type="button" onClick={onRun} disabled={running} className="flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-bold text-white hover:bg-emerald-700 disabled:opacity-60"><CirclePlay size={18} />{running ? "Тексерілуде..." : "Нәтижені тексеру"}</button></div>
        <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-400"><tr><th className="px-5 py-3">Шарт</th><th className="px-5 py-3">Threshold</th><th className="px-5 py-3">Нәтиже</th><th className="px-5 py-3">Status</th></tr></thead><tbody>{labCase.quality_gate.map((row) => <tr key={row.condition} className="border-t border-slate-100"><td className="px-5 py-3 font-bold">{row.condition}</td><td className="px-5 py-3 text-slate-500">{row.threshold}</td><td className="px-5 py-3">{row.result}</td><td className="px-5 py-3"><span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-extrabold text-emerald-700">{row.status}</span></td></tr>)}</tbody></table></div>
        {runResult && <div className="flex items-start gap-3 border-t border-emerald-100 bg-emerald-50 p-5 text-emerald-800"><CheckCircle2 className="mt-0.5 shrink-0" size={20} /><div><div className="font-extrabold">Quality Gate: {runResult.quality_gate}</div><p className="mt-1 text-sm">{runResult.message}</p></div></div>}
      </article>

      <div className="mt-12">
        <div className="mb-6"><div className="mb-2 text-xs font-extrabold uppercase tracking-[.2em] text-violet">Қорытынды есеп</div><h3 className="text-2xl font-extrabold tracking-tight md:text-3xl">20 тапсырманың орындалу журналы</h3></div>
        <div className="grid gap-3 md:grid-cols-2">{labCase.tasks.map((task) => <article key={task.id} className="flex gap-4 rounded-2xl border border-slate-200 bg-white p-4"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-emerald-100 text-xs font-extrabold text-emerald-700">{task.id}</span><div><div className="flex items-center gap-2 text-sm font-extrabold">{task.title}<Check size={15} className="text-emerald-600" /></div><p className="mt-1 text-xs leading-5 text-slate-500">{task.evidence}</p></div></article>)}</div>
        <div className="mt-6 flex items-start gap-3 rounded-2xl bg-emerald-600 p-5 text-white"><CheckCircle2 className="mt-0.5 shrink-0" size={20} /><div><div className="font-extrabold">Қорытынды: PASS</div><p className="mt-1 text-sm leading-6 text-emerald-50">{labCase.conclusion}</p></div></div>
      </div>
    </section>
  );
}
