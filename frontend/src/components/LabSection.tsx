import { Check, CirclePlay, GitBranch } from "lucide-react";
import type { DebugExample, DebugResult } from "../types";
import { CodePanel } from "./CodePanel";

type Props = {
  examples: DebugExample[];
  selected: DebugExample | undefined;
  debug: DebugResult | null;
  running: boolean;
  onSelect: (id: string) => void;
  onRun: () => void;
};

export function LabSection({ examples, selected, debug, running, onSelect, onRun }: Props) {
  return (
    <section id="lab" className="scroll-mt-24 py-24">
      <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="mb-2 text-xs font-extrabold uppercase tracking-[.2em] text-violet">02 / 7-зертханалық жұмыс</div>
          <h2 className="text-3xl font-extrabold tracking-tight md:text-4xl">Қатеден дұрыс шешімге дейін</h2>
          <p className="mt-3 text-slate-500">Алдымен қатені бақылаңыз, debugger арқылы себебін табыңыз, кейін түзетуді тексеріңіз.</p>
        </div>
        <div className="flex items-center gap-2 text-sm font-bold text-slate-400"><GitBranch size={17} /> 3 нақты Python мысалы</div>
      </div>

      <div className="mb-7 grid gap-3 sm:grid-cols-3">
        {["Қатені бақылау", "Себебін табу", "Түзетуді тексеру"].map((label, index) => (
          <div key={label} className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4">
            <span className={`grid h-8 w-8 place-items-center rounded-full text-xs font-extrabold ${index === 0 ? "bg-rose-100 text-rose-600" : index === 1 ? "bg-violet/10 text-violet" : "bg-emerald-100 text-emerald-600"}`}>{index + 1}</span>
            <span className="text-sm font-bold">{label}</span>
          </div>
        ))}
      </div>

      <div className="mb-6 flex gap-2 overflow-x-auto pb-1">
        {examples.map((example) => (
          <button key={example.id} type="button" onClick={() => onSelect(example.id)} className={`whitespace-nowrap rounded-xl px-4 py-3 text-sm font-bold ${selected?.id === example.id ? "bg-violet text-white" : "bg-white text-slate-500 shadow-soft hover:text-violet"}`}>{example.title}</button>
        ))}
      </div>

      {selected && (
        <>
          <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-violet/10 bg-violet/5 p-5">
            <div>
              <div className="mb-2 flex items-center gap-2 text-xs font-bold text-violet"><span className="rounded-md bg-violet px-2 py-1 text-white">{selected.error_type}</span><span>{selected.difficulty}</span></div>
              <p className="font-extrabold leading-6">{selected.summary}</p>
            </div>
            <button type="button" onClick={onRun} disabled={running} className="flex items-center gap-2 rounded-xl bg-ink px-4 py-3 text-sm font-bold text-white hover:bg-slate-700 disabled:cursor-wait disabled:opacity-60"><CirclePlay size={18} />{running ? "Іске қосылуда..." : "Breakpoint іске қосу"}</button>
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            <CodePanel title="Бастапқы қате код" subtitle="Алдымен осы нәтижені зерттеңіз" code={selected.buggy_code} variant="buggy" />
            <CodePanel title="Түзетілген дұрыс код" subtitle="Түпкі себеп жойылған нұсқа" code={selected.fixed_code} variant="fixed" />
          </div>
        </>
      )}

      {debug && (
        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
          <div className="flex items-center gap-2 font-bold text-emerald-800"><Check size={18} />{debug.message}</div>
          <p className="mt-2 text-sm text-emerald-700">{debug.next_action}</p>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl border border-rose-200 bg-rose-50 p-4"><div className="text-xs font-extrabold uppercase tracking-wider text-rose-700">Қате нәтиже</div><div className="code-font mt-2 text-lg font-bold text-rose-900">{debug.buggy_result}</div></div>
            <div className="rounded-xl border border-emerald-200 bg-white p-4"><div className="text-xs font-extrabold uppercase tracking-wider text-emerald-700">Дұрыс нәтиже</div><div className="code-font mt-2 text-lg font-bold text-emerald-900">{debug.fixed_result}</div></div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">{Object.entries(debug.variables).map(([key, value]) => <span key={key} className="code-font rounded-lg bg-white px-3 py-2 text-xs text-slate-600 shadow-sm"><b>{key}</b> = {value}</span>)}</div>
        </div>
      )}
    </section>
  );
}
