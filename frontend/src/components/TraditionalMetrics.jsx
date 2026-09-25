import { BarChart3, Info } from "lucide-react";

function TraditionalMetrics({
  metrics = {},
  referenceFreeMetrics = {},
}) {
  const metricList = [
    {
      name: "BLEU",
      value: Number(metrics?.BLEU ?? 0),
      description:
        "Measures n-gram overlap with the reference translation.",
    },
    {
      name: "chrF",
      value: Number(metrics?.chrF ?? 0),
      description:
        "Measures character n-gram similarity with the reference.",
    },
    {
      name: "chrF++",
      value: Number(metrics?.["chrF++"] ?? 0),
      description:
        "Character n-gram metric that also considers word-level information.",
    },
    {
      name: "METEOR",
      value: Number(metrics?.METEOR ?? 0),
      description:
        "Measures unigram matching with emphasis on precision and recall.",
    },
    {
      name: "BERTScore",
      value: Number(metrics?.BERTScore ?? 0),
      description:
        "Measures semantic similarity using contextual embeddings.",
    },
    {
      name: "COMET",
      value: Number(metrics?.COMET ?? 0),
      description:
        "Learned evaluation metric for machine translation quality.",
    },
    {
      name: "TER",
      value: Number(metrics?.TER ?? 0),
      inverse: true,
      description:
        "Measures the amount of editing required to transform the translation into the reference. Lower is better.",
    },
  ];

  const referenceFreeList = [
    {
      name: "Multilingual Similarity",
      value: Number(
        referenceFreeMetrics?.multilingual_similarity ?? 0
      ),
    },
    {
      name: "Word Alignment Coverage",
      value: Number(
        referenceFreeMetrics?.word_alignment_coverage ?? 0
      ),
    },
    {
      name: "Entity Preservation",
      value: Number(
        referenceFreeMetrics?.entity_preservation ?? 0
      ),
    },
    {
      name: "Terminology Accuracy",
      value: Number(
        referenceFreeMetrics?.terminology_accuracy ?? 0
      ),
    },
    {
      name: "Length Ratio",
      value: Number(
        referenceFreeMetrics?.length_ratio ?? 0
      ),
    },
    {
      name: "Untranslated Token Ratio",
      value: Number(
        referenceFreeMetrics?.untranslated_token_ratio ?? 0
      ),
      inverse: true,
    },
  ];

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold">
              Traditional Metrics
            </h2>

            <BarChart3
              size={15}
              className="text-slate-500"
            />
          </div>

          <p className="mt-1 text-[10px] text-slate-500">
            Reference-based translation quality metrics
          </p>
        </div>
      </div>

      {/* Reference-Based Metrics */}
      <div className="space-y-4">
        {metricList.map((metric) => {
          const percentage = Math.min(
            Math.max(metric.value * 100, 0),
            100
          );

          return (
            <div key={metric.name}>
              <div className="mb-1.5 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-300">
                  {metric.name}
                </span>

                <span
                  className={`text-xs font-semibold ${
                    metric.inverse
                      ? "text-rose-400"
                      : "text-slate-300"
                  }`}
                >
                  {metric.value.toFixed(3)}
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    metric.inverse
                      ? "bg-rose-500"
                      : "bg-gradient-to-r from-blue-500 to-violet-500"
                  }`}
                  style={{
                    width: `${percentage}%`,
                  }}
                />
              </div>

              <p className="mt-1 text-[9px] leading-4 text-slate-600">
                {metric.description}
              </p>
            </div>
          );
        })}
      </div>

      {/* Reference-Free Metrics */}
      <div className="mt-6 border-t border-white/5 pt-5">
        <div className="mb-4">
          <h3 className="text-sm font-semibold text-slate-200">
            Reference-Free Metrics
          </h3>

          <p className="mt-1 text-[10px] text-slate-500">
            Additional signals calculated without directly
            comparing against a reference.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {referenceFreeList.map((metric) => {
            const displayValue = metric.value;

            /*
             * Length ratio is not a bounded 0–1 quality score.
             * Keep its bar bounded for visual purposes while
             * displaying the actual value.
             */
            const barValue =
              metric.name === "Length Ratio"
                ? Math.min(displayValue * 50, 100)
                : Math.min(
                    Math.max(displayValue * 100, 0),
                    100
                  );

            return (
              <div
                key={metric.name}
                className="rounded-xl border border-white/5 bg-slate-900/50 p-3"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs text-slate-400">
                    {metric.name}
                  </span>

                  <span
                    className={`text-xs font-semibold ${
                      metric.inverse
                        ? "text-rose-400"
                        : "text-slate-200"
                    }`}
                  >
                    {displayValue.toFixed(3)}
                  </span>
                </div>

                <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className={`h-full rounded-full ${
                      metric.inverse
                        ? "bg-rose-500"
                        : "bg-blue-500"
                    }`}
                    style={{
                      width: `${barValue}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Info */}
      <div className="mt-5 flex gap-2 rounded-xl border border-white/5 bg-slate-900/50 p-3">
        <Info
          size={14}
          className="mt-0.5 shrink-0 text-slate-500"
        />

        <p className="text-[10px] leading-4 text-slate-500">
          Higher values generally indicate stronger quality
          signals. TER and untranslated-token ratio are
          error-oriented metrics, where lower values are
          preferable.
        </p>
      </div>
    </section>
  );
}

export default TraditionalMetrics;