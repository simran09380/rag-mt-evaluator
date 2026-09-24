import {
  Target,
  FileCheck,
  BookOpen,
  Tag,
  ShieldCheck,
} from "lucide-react";

const dimensionConfig = {
  accuracy: {
    label: "Accuracy",
    icon: Target,
    iconStyle: "bg-blue-500/10 text-blue-400",
  },

  fluency: {
    label: "Fluency",
    icon: FileCheck,
    iconStyle: "bg-emerald-500/10 text-emerald-400",
  },

  terminology: {
    label: "Terminology",
    icon: BookOpen,
    iconStyle: "bg-violet-500/10 text-violet-400",
  },

  named_entities: {
    label: "Named Entities",
    icon: Tag,
    iconStyle: "bg-orange-500/10 text-orange-400",
  },
};

function LLMEvaluation({ evaluation }) {
  const dimensions = Object.entries(evaluation);

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      {/* Header */}
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

        <div className="flex items-center gap-3">

          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div>
            <div className="flex items-center gap-2">

              <h2 className="text-base font-semibold">
                LLM Evaluation
              </h2>

              <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2 py-0.5 text-[9px] font-medium text-emerald-400">
                Evidence-Grounded
              </span>

            </div>

            <p className="mt-1 text-[10px] text-slate-500">
              Qualitative assessment generated using retrieved evidence
            </p>
          </div>

        </div>


        {/* Grounding indicator */}
        <div className="flex items-center gap-2 rounded-lg border border-emerald-500/10 bg-emerald-500/5 px-3 py-2">

          <ShieldCheck
            size={14}
            className="text-emerald-400"
          />

          <span className="text-[10px] text-emerald-400">
            Evidence Grounded
          </span>

        </div>

      </div>


      {/* Evaluation Cards */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

        {dimensions.map(([key, item]) => {

          const config = dimensionConfig[key];

          if (!config) return null;

          const Icon = config.icon;

          return (
            <div
              key={key}
              className="group rounded-xl border border-white/10 bg-slate-900/60 p-4 transition hover:border-violet-500/20"
            >

              {/* Card Header */}
              <div className="flex items-start justify-between">

                <div className="flex items-center gap-3">

                  <div
                    className={`flex h-9 w-9 items-center justify-center rounded-lg ${config.iconStyle}`}
                  >
                    <Icon size={18} />
                  </div>

                  <div>

                    <p className="text-xs font-semibold text-slate-200">
                      {config.label}
                    </p>

                    <p className="mt-0.5 text-[9px] text-slate-600">
                      LLM Assessment
                    </p>

                  </div>

                </div>


                {/* Score */}
                <div className="text-right">

                  <p className="text-lg font-bold text-slate-100">
                    {item.score}
                    <span className="ml-0.5 text-xs font-normal text-slate-500">
                      / 5
                    </span>
                  </p>

                </div>

              </div>


              {/* Score bar */}
              <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">

                <div
                  className="h-full rounded-full bg-gradient-to-r from-violet-500 to-blue-500"
                  style={{
                    width: `${(item.score / 5) * 100}%`,
                  }}
                />

              </div>


              {/* Judgment */}
              <div className="mt-4">

                <p className="text-[10px] font-medium uppercase tracking-wide text-slate-600">
                  Judgment
                </p>

                <p className="mt-1.5 text-[11px] leading-5 text-slate-400">
                  {item.judgment}
                </p>

              </div>


              {/* Evidence */}
              <div className="mt-4 flex items-center gap-2 border-t border-white/5 pt-3">

                <span className="text-[9px] text-slate-600">
                  Evidence:
                </span>

                {item.evidence_ids.length > 0 ? (
                  <div className="flex gap-1">

                    {item.evidence_ids.map((evidenceId) => (
                      <span
                        key={evidenceId}
                        className="rounded-md bg-violet-500/10 px-2 py-1 text-[9px] font-semibold text-violet-400"
                      >
                        {evidenceId}
                      </span>
                    ))}

                  </div>
                ) : (
                  <span className="text-[9px] text-slate-500">
                    No direct evidence
                  </span>
                )}

              </div>

            </div>
          );
        })}

      </div>


      {/* Explanation */}
      <div className="mt-5 rounded-xl border border-blue-500/10 bg-blue-500/5 p-4">

        <div className="flex gap-3">

          <ShieldCheck
            size={17}
            className="mt-0.5 shrink-0 text-blue-400"
          />

          <div>

            <p className="text-xs font-semibold text-blue-300">
              How the LLM evaluation works
            </p>

            <p className="mt-1 text-[10px] leading-5 text-slate-500">
              The evaluator considers the source sentence, machine
              translation, retrieved evidence, traditional metric
              signals, and evaluation instructions to produce
              dimension-level judgments.
            </p>

          </div>

        </div>

      </div>

    </section>
  );
}

export default LLMEvaluation;