import {
  FileText,
  CheckCircle2,
  BarChart3,
  AlertTriangle,
} from "lucide-react";

function DatasetSummary({ dataset }) {
  return (
    <section className="mt-6">

      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <div>
          <h2 className="text-lg font-semibold">
            Dataset Evaluation
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Summary of translation quality across the uploaded dataset.
          </p>
        </div>
      </div>


      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

        <SummaryCard
          icon={FileText}
          label="Total Sentences"
          value={dataset.total_sentences}
          iconStyle="bg-blue-500/10 text-blue-400"
        />

        <SummaryCard
          icon={CheckCircle2}
          label="Evaluated"
          value={dataset.evaluated_sentences}
          iconStyle="bg-emerald-500/10 text-emerald-400"
        />

        <SummaryCard
          icon={BarChart3}
          label="Average Score"
          value={dataset.average_score}
          suffix="/ 100"
          iconStyle="bg-violet-500/10 text-violet-400"
        />

        <SummaryCard
          icon={AlertTriangle}
          label="Needs Review"
          value={dataset.quality_distribution.needs_review}
          iconStyle="bg-orange-500/10 text-orange-400"
        />

      </div>


      {/* Quality distribution */}
      <div className="mt-4 rounded-2xl border border-white/10 bg-white/[0.03] p-5">

        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-semibold">
            Quality Distribution
          </h3>

          <span className="text-[10px] text-slate-600">
            {dataset.total_sentences} sentences
          </span>
        </div>


        <div className="flex h-3 overflow-hidden rounded-full bg-slate-800">

          <div
            className="bg-emerald-500"
            style={{
              width: `${
                (dataset.quality_distribution.excellent /
                  dataset.total_sentences) *
                100
              }%`,
            }}
          />

          <div
            className="bg-blue-500"
            style={{
              width: `${
                (dataset.quality_distribution.good /
                  dataset.total_sentences) *
                100
              }%`,
            }}
          />

          <div
            className="bg-orange-500"
            style={{
              width: `${
                (dataset.quality_distribution.needs_review /
                  dataset.total_sentences) *
                100
              }%`,
            }}
          />

        </div>


        <div className="mt-4 flex flex-wrap gap-5">

          <Legend
            label="Excellent"
            value={dataset.quality_distribution.excellent}
            color="bg-emerald-500"
          />

          <Legend
            label="Good"
            value={dataset.quality_distribution.good}
            color="bg-blue-500"
          />

          <Legend
            label="Needs Review"
            value={dataset.quality_distribution.needs_review}
            color="bg-orange-500"
          />

        </div>

      </div>

    </section>
  );
}


function SummaryCard({
  icon: Icon,
  label,
  value,
  suffix,
  iconStyle,
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      <div className="flex items-center gap-3">

        <div
          className={`flex h-10 w-10 items-center justify-center rounded-xl ${iconStyle}`}
        >
          <Icon size={19} />
        </div>

        <p className="text-xs text-slate-500">
          {label}
        </p>

      </div>

      <p className="mt-4 text-2xl font-bold">
        {value}

        {suffix && (
          <span className="ml-1 text-xs font-normal text-slate-500">
            {suffix}
          </span>
        )}
      </p>

    </div>
  );
}


function Legend({ label, value, color }) {
  return (
    <div className="flex items-center gap-2">

      <span className={`h-2.5 w-2.5 rounded-full ${color}`} />

      <span className="text-[10px] text-slate-500">
        {label}
      </span>

      <span className="text-[10px] font-semibold text-slate-300">
        {value}
      </span>

    </div>
  );
}

export default DatasetSummary;