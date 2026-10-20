import { useEffect, useMemo, useState } from "react";
import { ArrowRight, Check, Terminal, Zap } from "lucide-react";
import { checkLab8QualityGate, getLab8Case, getLabExamples, startDebug } from "./api";
import { Lab8Section } from "./components/Lab8Section";
import { LabSection } from "./components/LabSection";
import { ReportSection } from "./components/ReportSection";
import type { DebugExample, DebugResult, Lab8Case, Lab8RunResult } from "./types";

export default function App() {
  const [examples, setExamples] = useState<DebugExample[]>([]);
  const [selectedId, setSelectedId] = useState("division");
  const [debug, setDebug] = useState<DebugResult | null>(null);
  const [running, setRunning] = useState(false);
  const [lab8Case, setLab8Case] = useState<Lab8Case | null>(null);
  const [lab8Result, setLab8Result] = useState<Lab8RunResult | null>(null);
  const [lab8Running, setLab8Running] = useState(false);
  const [error, setError] = useState("");

  const selected = useMemo(
    () => examples.find((example) => example.id === selectedId),
    [examples, selectedId],
  );

  useEffect(() => {
    getLabExamples()
      .then(setExamples)
      .catch((reason: unknown) => {
        console.error(reason);
        setError("Оқу материалдарын жүктеу мүмкін болмады. Backend серверінің іске қосылғанын тексеріңіз.");
      });
    getLab8Case()
      .then(setLab8Case)
      .catch((reason: unknown) => {
        console.error(reason);
        setError("8-зертхана есебін жүктеу мүмкін болмады. Backend серверін тексеріңіз.");
      });
  }, []);

  const runDebug = async () => {
    if (!selected) return;
    setRunning(true);
    setError("");
    try {
      setDebug(await startDebug(selected));
    } catch (reason) {
      console.error(reason);
      setError("Debug режимін іске қосу мүмкін болмады. API байланысын тексеріңіз.");
    } finally {
      setRunning(false);
    }
  };

  const selectExample = (id: string) => {
    setSelectedId(id);
    setDebug(null);
  };

  const checkLab8 = async () => {
    setLab8Running(true);
    setError("");
    try {
      setLab8Result(await checkLab8QualityGate());
    } catch (reason) {
      console.error(reason);
      setError("8-зертхананың Quality Gate нәтижесін алу мүмкін болмады.");
    } finally {
      setLab8Running(false);
    }
  };

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <a href="#top" className="flex items-center gap-3">
            <span className="rounded-xl bg-violet p-2 text-white"><Zap size={20} fill="currentColor" /></span>
            <span><span className="block text-lg font-extrabold tracking-tight">DebugLab <b className="text-violet">KZ</b></span><span className="block text-[10px] font-bold uppercase tracking-[.22em] text-slate-400">Python зертханасы</span></span>
          </a>
          <nav className="hidden items-center gap-7 text-sm font-semibold text-slate-500 md:flex"><a href="#lab" className="hover:text-violet">7-зертхана</a><a href="#lab8" className="hover:text-violet">8-зертхана</a><a href="#report" className="hover:text-violet">Есеп</a></nav>
          <div className="rounded-full bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-700">20/20 тапсырма</div>
        </div>
      </header>

      <main id="top" className="mx-auto max-w-7xl px-6 pb-12">
        <section className="grid items-center gap-12 py-16 lg:grid-cols-[1.05fr_.95fr] lg:py-24">
          <div>
            <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-violet/10 px-3 py-2 text-xs font-bold text-violet"><Terminal size={14} />7–8 зертханалық жұмыс</div>
            <h1 className="max-w-3xl text-4xl font-extrabold leading-tight tracking-tight md:text-6xl">Кодты талда. <span className="text-violet">Мәселені тап.</span> Сапаны көтер.</h1>
            <p className="mt-6 max-w-xl text-lg leading-8 text-slate-500">Python кодын debugging, static analysis, code review және regression test арқылы зерттеңіз.</p>
            <div className="mt-8 flex flex-wrap gap-3"><a href="#lab8" className="flex items-center gap-2 rounded-xl bg-violet px-5 py-3 text-sm font-bold text-white shadow-lg shadow-violet/20 hover:bg-indigo-600">8-зертхананы ашу <ArrowRight size={17} /></a><a href="#lab" className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-600 hover:text-violet">7-зертхана</a></div>
          </div>
          <div className="relative rounded-3xl bg-[#15162b] p-6 shadow-2xl shadow-indigo-200">
            <div className="mb-5 flex gap-2"><span className="h-3 w-3 rounded-full bg-rose-400" /><span className="h-3 w-3 rounded-full bg-amber-300" /><span className="h-3 w-3 rounded-full bg-emerald-400" /><span className="ml-auto code-font text-xs text-slate-500">lab7/debug_session.py</span></div>
            <pre className="code-font overflow-x-auto text-sm leading-8 text-slate-300"><span className="text-slate-500">01 </span><span className="text-violet-300">def</span> <span className="text-sky-300">final_price</span>(price, percent):{"\n"}<span className="text-slate-500">02 </span>    discount = price * percent<span className="text-rose-300">  ← қате</span>{"\n"}<span className="text-slate-500">03 </span>    <span className="text-violet-300">return</span> price - discount{"\n\n"}<span className="text-rose-300">Нақты нәтиже: -19000</span>{"\n"}<span className="text-emerald-300">Күтілетін нәтиже: 800</span></pre>
            <div className="absolute -bottom-5 -left-3 flex items-center gap-3 rounded-2xl bg-white p-4 shadow-soft sm:-left-5"><span className="rounded-xl bg-emerald-100 p-2 text-emerald-600"><Check size={18} /></span><span><span className="block text-xs font-bold text-slate-800">Regression тест</span><span className="block text-xs text-slate-400">Түзетуді қорғайды</span></span></div>
          </div>
        </section>

        {error && <div role="alert" className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm font-semibold text-rose-700">{error}</div>}

        <LabSection examples={examples} selected={selected} debug={debug} running={running} onSelect={selectExample} onRun={runDebug} />
        {selected && <ReportSection example={selected} />}
        {lab8Case && <Lab8Section labCase={lab8Case} runResult={lab8Result} running={lab8Running} onRun={checkLab8} />}
      </main>

      <footer className="border-t border-slate-200 bg-white py-8 text-center text-sm text-slate-400">© 2026 DebugLab KZ · Сенімді код қадамдық талдаудан басталады.</footer>
    </div>
  );
}
