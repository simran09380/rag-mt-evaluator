import {
  ChevronDown,
  Info,
  ShieldCheck,
} from "lucide-react";
import { useState } from "react";

function formatPercent(value) {
  if (typeof value !== "number") {
    return "0.00";
  }

  return (value * 100).toFixed(2);
}

function formatContribution(value, weight) {
  if (
    typeof value !== "number" ||
    typeof weight !== "number"
  ) {
    return "0.00";
  }

  return (value * weight * 100).toFixed(2);
}

function getQualityLabel(score) {
  if (typeof score !== "number") {
    return "Not Available";
  }

  if (score >= 90) {
    return "Excellent";
  }

  if (score >= 75) {
    return "Good";
  }

  if (score >= 60) {
    return "Needs Review";
  }

  return "Poor";
}

function getQualityStyle(label) {
  const styles = {
    Excellent:
      "border-emerald-500/20 bg-emerald-500/10 text-emerald-400",

    Good:
      "border-blue-500/20 bg-blue-500/10 text-blue-400",

    "Needs Review":
      "border-orange-500/20 bg-orange-500/10 text-orange-400",

    Poor:
      "border-rose-500/20 bg-rose-500/10 text-rose-400",

    "Not Available":
      "border-slate-500/20 bg-slate-500/10 text-slate-500",
  };

  return styles[label] || styles["Not Available"];
}

function getQualityDescription(score) {
  if (typeof score !== "number") {
    return "The evaluation score is not available.";
  }

  if (score >= 90) {
    return "The translation achieved a very high overall evaluation score.";
  }

  if (score >= 75) {
    return "The translation achieved a good overall evaluation score.";
  }

  if (score >= 60) {
    return "The translation may need review in one or more evaluation dimensions.";
  }

  return "The translation has significant quality issues that should be reviewed.";
}

function getComponentLabel(key) {
  const labels = {
    reference_metrics: "Reference Metrics",
    llm_evaluation: "LLM Evaluation",
    evidence_agreement: "Evidence Agreement",
    semantic_adequacy: "Semantic Adequacy",
    terminology: "Terminology",
    fluency: "Fluency",
    mqm_penalty: "MQM Penalty",
  };

  return labels[key] || key;
}

function getComponentDescription(key) {
  const descriptions = {
    reference_metrics:
      "Contribution from reference-based translation metrics such as BLEU, METEOR, chrF, BERTScore and COMET.",

    llm_evaluation:
      "Contribution from the evidence-grounded LLM evaluation.",

    evidence_agreement:
      "Measures agreement between the retrieved evidence and the evaluation.",

    semantic_adequacy:
      "Measures how well the translation preserves the source meaning.",

    terminology:
      "Measures terminology correctness and consistency.",

    fluency:
      "Measures the fluency and naturalness of the target translation.",

    mqm_penalty:
      "Penalty associated with MQM-classified translation errors.",
  };

  return (
    descriptions[key] ||
    "Component used by the final evaluation."
  );
}

function OverallEvaluation({ evaluation }) {
  const [showBreakdown, setShowBreakdown] = useState(false);

  const finalEvaluation =
    evaluation?.final_evaluation || {};

  const components =
    finalEvaluation?.components || {};

  const weights =
    finalEvaluation?.weights || {};

  const finalScore =
    typeof finalEvaluation?.final_score === "number"
      ? finalEvaluation.final_score
      : evaluation?.overall_score ?? 0;

  const qualityLabel =
    evaluation?.quality_label ||
    getQualityLabel(finalScore);

  const evaluationType =
    finalEvaluation?.evaluation_type ||
    "reference_based";

  const weightedScore =
    typeof finalEvaluation?.weighted_score === "number"
      ? finalEvaluation.weighted_score
      : finalScore;

  const componentEntries = Object.entries(weights);

  return (
    <div className="rounded-2xl border border-white/10 bg-[#0b1020] p-5 shadow-xl shadow-black/10">

      {/* Header */}
      <div className="mb-5 flex items-start justify-between">

        <div>
          <div className="flex items-center gap-2">
            <div className="h-5 w-1 rounded-full bg-violet-500" />

            <h2 className="text-sm font-semibold text-white">
              Overall Evaluation
            </h2>
          </div>

          <p className="mt-2 text-[11px] text-slate-500">
            Final score based on multiple evaluation signals
          </p>
        </div>

        <div className="flex items-center gap-1 rounded-lg border border-white/10 bg-white/[0.03] px-2 py-1 text-[10px] text-slate-400">
          <Info size={11} />
          {evaluationType.replace("_", " ")}
        </div>

      </div>


      {/* Score */}
      <div className="flex flex-col items-center">

        <div className="relative flex h-36 w-36 items-center justify-center">

          <div className="absolute inset-0 rounded-full border-[7px] border-slate-800" />

          <div
            className="absolute inset-0 rounded-full border-[7px] border-emerald-400"
            style={{
              clipPath: `inset(${100 - Math.min(finalScore, 100)}% 0 0 0)`,
            }}
          />

          <div className="text-center">

            <div className="text-3xl font-bold tracking-tight">
              {finalScore.toFixed(2)}
            </div>

            <div className="text-[10px] text-slate-500">
              / 100
            </div>

          </div>

        </div>


        {/* Quality */}
        <div
            className={`mt-3 rounded-full border px-3 py-1 text-[11px] font-medium ${getQualityStyle(
              qualityLabel
            )}`}
          >
            {qualityLabel}
          </div>

        <p className="mt-3 max-w-[270px] text-center text-[11px] leading-5 text-slate-500">
          {getQualityDescription(finalScore)}
        </p>

      </div>


      {/* Why this score */}
      <div className="mt-5 border-t border-white/10 pt-4">

        <button
          type="button"
          onClick={() =>
            setShowBreakdown((previous) => !previous)
          }
          className="flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/[0.02] px-3 py-2.5 text-left transition hover:bg-white/[0.04]"
        >

          <div className="flex items-center gap-2">

            <ShieldCheck
              size={15}
              className="text-violet-400"
            />

            <div>
              <p className="text-xs font-semibold text-slate-200">
                Why this score?
              </p>

              <p className="mt-0.5 text-[10px] text-slate-500">
                View the final score composition
              </p>
            </div>

          </div>

          <ChevronDown
            size={15}
            className={`text-slate-500 transition ${
              showBreakdown ? "rotate-180" : ""
            }`}
          />

        </button>


        {showBreakdown && (
          <div className="mt-3 space-y-3">

            {componentEntries.map(
              ([key, weight]) => {
                const value =
                  typeof components[key] === "number"
                    ? components[key]
                    : 0;

                const contribution =
                  formatContribution(
                    value,
                    weight
                  );

                return (
                  <div
                    key={key}
                    className="rounded-xl border border-white/10 bg-[#080d1b] p-3"
                  >

                    <div className="flex items-start justify-between gap-3">

                      <div>
                        <p className="text-[11px] font-medium text-slate-200">
                          {getComponentLabel(key)}
                        </p>

                        <p className="mt-1 text-[9px] leading-4 text-slate-500">
                          {getComponentDescription(key)}
                        </p>
                      </div>

                      <div className="shrink-0 text-right">

                        <p className="text-[11px] font-semibold text-white">
                          {formatPercent(value)}
                        </p>

                        <p className="text-[9px] text-slate-500">
                          Weight {(weight * 100).toFixed(0)}%
                        </p>

                      </div>

                    </div>


                    {/* Component bar */}
                    <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-800">

                      <div
                        className="h-full rounded-full bg-violet-500 transition-all"
                        style={{
                          width: `${Math.min(
                            Math.max(value * 100, 0),
                            100
                          )}%`,
                        }}
                      />

                    </div>


                    <div className="mt-2 flex items-center justify-between">

                      <span className="text-[9px] text-slate-500">
                        Weighted contribution
                      </span>

                      <span className="text-[10px] font-semibold text-violet-300">
                        +{contribution}
                      </span>

                    </div>

                  </div>
                );
              }
            )}


            {/* Final calculation */}
            <div className="rounded-xl border border-violet-500/20 bg-violet-500/[0.05] p-3">

              <div className="flex items-center justify-between">

                <span className="text-[10px] text-slate-400">
                  Weighted Score
                </span>

                <span className="text-sm font-bold text-white">
                  {Number(weightedScore).toFixed(2)}
                </span>

              </div>

              <div className="mt-2 flex items-center justify-between border-t border-white/10 pt-2">

                <span className="text-[10px] font-semibold text-slate-300">
                  Final Score
                </span>

                <span className="text-base font-bold text-violet-300">
                  {finalScore.toFixed(2)} / 100
                </span>

              </div>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default OverallEvaluation;