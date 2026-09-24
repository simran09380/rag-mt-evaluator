import { Copy } from "lucide-react";

function TranslationComparison({ evaluation }) {
  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      <div className="mb-5 flex items-center justify-between">

        <div className="flex items-center gap-3">
          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <h2 className="text-base font-semibold">
            Translation Comparison
          </h2>
        </div>

        <button className="rounded-lg border border-violet-500/30 px-3 py-1.5 text-xs text-violet-300 hover:bg-violet-500/10">
          View Differences
        </button>

      </div>


      <div className="space-y-3">

        <TranslationBlock
          badge="EN"
          title="Source (English)"
          text={evaluation.source_sentence}
          color="blue"
        />

        <TranslationBlock
          badge="HI"
          title="Machine Translation (Hindi)"
          text={evaluation.machine_translation}
          color="violet"
        />

        <TranslationBlock
          badge="HI"
          title="Reference (Hindi)"
          text={evaluation.reference}
          color="purple"
        />

      </div>

    </section>
  );
}


function TranslationBlock({
  badge,
  title,
  text,
  color,
}) {
  const badgeStyle =
    color === "blue"
      ? "bg-blue-500 text-white"
      : "bg-violet-500 text-white";

  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 p-3">

      <div className="flex items-start gap-3">

        <span
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-[11px] font-bold ${badgeStyle}`}
        >
          {badge}
        </span>

        <div className="min-w-0 flex-1">

          <p className="text-xs font-semibold text-slate-300">
            {title}
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            {text}
          </p>

        </div>

        <button className="text-slate-600 hover:text-slate-300">
          <Copy size={14} />
        </button>

      </div>

    </div>
  );
}

export default TranslationComparison;