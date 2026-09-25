import { useState } from "react";
import {
  Target,
  FileCheck,
  BookOpen,
  Tag,
  ShieldCheck,
  Palette,
  MinusCircle,
  PlusCircle,
  ChevronDown,
} from "lucide-react";

function DimensionScores({ scores = {}, llmEvaluation = {} }) {
  const [openDimension, setOpenDimension] = useState(null);

  const dimensions = [
    {
      key: "accuracy",
      name: "Accuracy",
      icon: Target,
      color: "blue",
      description: "How accurately the translation preserves the source meaning.",
    },
    {
      key: "fluency",
      name: "Fluency",
      icon: FileCheck,
      color: "emerald",
      description: "How natural, grammatical, and readable the translation is.",
    },
    {
      key: "terminology",
      name: "Terminology",
      icon: BookOpen,
      color: "violet",
      description: "Whether domain-specific terms are translated correctly.",
    },
    {
      key: "named_entities",
      name: "Named Entities",
      icon: Tag,
      color: "orange",
      description: "Whether names, places, organizations, and other entities are preserved correctly.",
    },
    {
      key: "factual_consistency",
      name: "Factual Consistency",
      icon: ShieldCheck,
      color: "cyan",
      description: "Whether the translation remains factually consistent with the source.",
    },
    {
      key: "style",
      name: "Style",
      icon: Palette,
      color: "pink",
      description: "Whether the translation follows an appropriate style and tone.",
    },
    {
      key: "omissions",
      name: "Omissions",
      icon: MinusCircle,
      color: "amber",
      description: "Whether important information from the source has been omitted.",
    },
    {
      key: "additions",
      name: "Additions",
      icon: PlusCircle,
      color: "rose",
      description: "Whether the translation introduces information that is not present in the source.",
    },
  ];

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <div>
          <h2 className="text-base font-semibold">
            Dimension Scores
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Detailed quality assessment across 8 evaluation dimensions
          </p>
        </div>
      </div>

      {/* Dimension Cards */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {dimensions.map((dimension) => {
          const Icon = dimension.icon;

          const value = Number(
            scores?.[dimension.key] ?? 0
          );

          const llmDimension =
            llmEvaluation?.[dimension.key] || {};

          const isOpen =
            openDimension === dimension.key;

          return (
            <ScoreCard
              key={dimension.key}
              dimension={dimension}
              value={value}
              llmDimension={llmDimension}
              Icon={Icon}
              isOpen={isOpen}
              onToggle={() =>
                setOpenDimension(
                  isOpen ? null : dimension.key
                )
              }
            />
          );
        })}
      </div>
    </section>
  );
}


function ScoreCard({
  dimension,
  value,
  llmDimension,
  Icon,
  isOpen,
  onToggle,
}) {
  const styles = {
    blue: {
      icon: "bg-blue-500/10 text-blue-400",
      bar: "bg-blue-500",
    },

    emerald: {
      icon: "bg-emerald-500/10 text-emerald-400",
      bar: "bg-emerald-500",
    },

    violet: {
      icon: "bg-violet-500/10 text-violet-400",
      bar: "bg-violet-500",
    },

    orange: {
      icon: "bg-orange-500/10 text-orange-400",
      bar: "bg-orange-500",
    },

    cyan: {
      icon: "bg-cyan-500/10 text-cyan-400",
      bar: "bg-cyan-500",
    },

    pink: {
      icon: "bg-pink-500/10 text-pink-400",
      bar: "bg-pink-500",
    },

    amber: {
      icon: "bg-amber-500/10 text-amber-400",
      bar: "bg-amber-500",
    },

    rose: {
      icon: "bg-rose-500/10 text-rose-400",
      bar: "bg-rose-500",
    },
  };

  const style = styles[dimension.color];

  const llmScore =
    typeof llmDimension?.score === "number"
      ? llmDimension.score
      : null;

  const judgment =
    llmDimension?.judgment ||
    "No detailed explanation was provided by the evaluation model.";

  const evidenceIds = Array.isArray(
    llmDimension?.evidence_ids
  )
    ? llmDimension.evidence_ids
    : [];

  const safeValue = Math.max(
    0,
    Math.min(100, value)
  );

  return (
    <div
      className={`rounded-xl border bg-slate-900/60 transition ${
        isOpen
          ? "border-violet-500/30"
          : "border-white/10"
      }`}
    >
      {/* Main Score */}
      <div className="p-4">
        <div className="flex items-center gap-3">
          <div
            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${style.icon}`}
          >
            <Icon size={18} />
          </div>

          <div className="min-w-0 flex-1">
            <p className="text-xs text-slate-500">
              {dimension.name}
            </p>

            <div className="flex items-baseline gap-1">
              <p className="text-lg font-bold">
                {safeValue}
              </p>

              <span className="text-xs font-normal text-slate-500">
                / 100
              </span>
            </div>
          </div>
        </div>

        {/* Score Bar */}
        <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-800">
          <div
            className={`h-full rounded-full transition-all duration-500 ${style.bar}`}
            style={{
              width: `${safeValue}%`,
            }}
          />
        </div>

        {/* View Reason */}
        <button
          type="button"
          onClick={onToggle}
          className="mt-4 flex w-full items-center justify-between border-t border-white/5 pt-3 text-left"
        >
          <span className="text-xs font-medium text-slate-400 transition hover:text-white">
            {isOpen ? "Hide reason" : "View reason"}
          </span>

          <ChevronDown
            size={15}
            className={`text-slate-500 transition-transform duration-200 ${
              isOpen ? "rotate-180" : ""
            }`}
          />
        </button>
      </div>

      {/* Reason Details */}
      {isOpen && (
        <div className="border-t border-white/5 px-4 pb-4 pt-3">
          <div className="rounded-lg bg-white/[0.02] p-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
              What this measures
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-400">
              {dimension.description}
            </p>
          </div>

          {/* LLM Score */}
          {llmScore !== null && (
            <div className="mt-3 flex items-center justify-between">
              <span className="text-xs text-slate-500">
                LLM Score
              </span>

              <span className="text-xs font-semibold text-slate-300">
                {llmScore} / 5
              </span>
            </div>
          )}

          {/* Judgment */}
          <div className="mt-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
              Evaluation Reason
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-300">
              {judgment}
            </p>
          </div>

          {/* Evidence */}
          <div className="mt-3">
            <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
              Supporting Evidence
            </p>

            {evidenceIds.length > 0 ? (
              <div className="mt-2 flex flex-wrap gap-2">
                {evidenceIds.map((id) => (
                  <span
                    key={id}
                    className="rounded-md border border-violet-500/20 bg-violet-500/10 px-2 py-1 text-[11px] font-medium text-violet-300"
                  >
                    {id}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-1 text-xs text-slate-500">
                No supporting evidence was attached to this dimension.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default DimensionScores;