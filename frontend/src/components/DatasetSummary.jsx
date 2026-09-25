import {
  FileText,
  CheckCircle2,
  BarChart3,
  AlertTriangle,
} from "lucide-react";

function getQualityLabel(score) {
  if (typeof score !== "number") return "Not Available";

  if (score >= 90) return "Excellent";
  if (score >= 75) return "Good";
  if (score >= 60) return "Needs Review";
  return "Poor";
}

function DatasetSummary({ dataset }) {
  const records = Array.isArray(dataset?.data)
    ? dataset.data
    : [];

  const totalSentences =
    dataset?.metadata?.num_records ??
    records.length;

  const evaluatedSentences = records.filter(
    (record) =>
      typeof record?.final_evaluation?.final_score ===
      "number"
  ).length;

  const scores = records
    .map(
      (record) =>
        record?.final_evaluation?.final_score
    )
    .filter((score) => typeof score === "number");

  const averageScore =
    scores.length > 0
      ? scores.reduce((sum, score) => sum + score, 0) /
        scores.length
      : 0;

  const qualityDistribution = {
    excellent: 0,
    good: 0,
    needs_review: 0,
    poor: 0,
  };

  scores.forEach((score) => {
    const quality = getQualityLabel(score);

    if (quality === "Excellent") {
      qualityDistribution.excellent++;
    } else if (quality === "Good") {
      qualityDistribution.good++;
    } else if (quality === "Needs Review") {
      qualityDistribution.needs_review++;
    } else if (quality === "Poor") {
      qualityDistribution.poor++;
    }
  });

  const needsReview =
    qualityDistribution.needs_review +
    qualityDistribution.poor;

  const distributionTotal =
    scores.length || 1;

  const cards = [
    {
      title: "Total Sentences",
      value: totalSentences,
      icon: FileText,
      description: "Sentences in uploaded dataset",
    },
    {
      title: "Evaluated Sentences",
      value: evaluatedSentences,
      icon: CheckCircle2,
      description: "Successfully evaluated",
    },
    {
      title: "Average Score",
      value:
        scores.length > 0
          ? averageScore.toFixed(1)
          : "—",
      icon: BarChart3,
      description: "Across evaluated sentences",
    },
    {
      title: "Needs Review",
      value: needsReview,
      icon: AlertTriangle,
      description: "Sentences requiring attention",
    },
  ];

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/[0.02] p-6">

      {/* Header */}
      <div className="mb-6">
        <p className="text-xs font-medium uppercase tracking-wider text-violet-400">
          Dataset Summary
        </p>

        <h2 className="mt-1 text-xl font-bold text-white">
          Dataset evaluation overview
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Summary calculated from the evaluated dataset returned by the backend.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div
              key={card.title}
              className="
                rounded-xl
                border border-white/10
                bg-black/20
                p-5
              "
            >
              <div className="flex items-start justify-between">

                <div>
                  <p className="text-xs text-slate-500">
                    {card.title}
                  </p>

                  <p className="mt-2 text-2xl font-bold text-white">
                    {card.value}
                  </p>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
                  <Icon size={19} />
                </div>

              </div>

              <p className="mt-3 text-[11px] text-slate-600">
                {card.description}
              </p>
            </div>
          );
        })}

      </div>

      {/* Quality Distribution */}
      <div className="mt-6 rounded-xl border border-white/10 bg-black/20 p-5">

        <div className="flex items-center justify-between">

          <div>
            <p className="text-sm font-semibold text-white">
              Quality Distribution
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Distribution of evaluated sentences by final score
            </p>
          </div>

          <span className="text-xs text-slate-500">
            {scores.length} evaluated
          </span>

        </div>

        {/* Distribution Bar */}
        {scores.length > 0 ? (
          <div className="mt-5 flex h-3 overflow-hidden rounded-full bg-white/5">

            {qualityDistribution.excellent > 0 && (
              <div
                className="bg-emerald-500"
                style={{
                  width: `${
                    (qualityDistribution.excellent /
                      distributionTotal) *
                    100
                  }%`,
                }}
              />
            )}

            {qualityDistribution.good > 0 && (
              <div
                className="bg-blue-500"
                style={{
                  width: `${
                    (qualityDistribution.good /
                      distributionTotal) *
                    100
                  }%`,
                }}
              />
            )}

            {qualityDistribution.needs_review > 0 && (
              <div
                className="bg-orange-500"
                style={{
                  width: `${
                    (qualityDistribution.needs_review /
                      distributionTotal) *
                    100
                  }%`,
                }}
              />
            )}

            {qualityDistribution.poor > 0 && (
              <div
                className="bg-rose-500"
                style={{
                  width: `${
                    (qualityDistribution.poor /
                      distributionTotal) *
                    100
                  }%`,
                }}
              />
            )}

          </div>
        ) : (
          <div className="mt-5 h-3 rounded-full bg-white/5" />
        )}

        {/* Legend */}
        <div className="mt-5 flex flex-wrap gap-x-6 gap-y-3">

          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
            <span className="text-xs text-slate-400">
              Excellent
            </span>
            <span className="text-xs font-semibold text-white">
              {qualityDistribution.excellent}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-blue-500" />
            <span className="text-xs text-slate-400">
              Good
            </span>
            <span className="text-xs font-semibold text-white">
              {qualityDistribution.good}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-orange-500" />
            <span className="text-xs text-slate-400">
              Needs Review
            </span>
            <span className="text-xs font-semibold text-white">
              {qualityDistribution.needs_review}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-rose-500" />
            <span className="text-xs text-slate-400">
              Poor
            </span>
            <span className="text-xs font-semibold text-white">
              {qualityDistribution.poor}
            </span>
          </div>

        </div>

      </div>

    </section>
  );
}

export default DatasetSummary;