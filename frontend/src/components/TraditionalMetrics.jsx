import { BarChart3 } from "lucide-react";

function TraditionalMetrics({ metrics }) {
  const metricList = [
    {
      name: "BLEU",
      value: metrics.BLEU,
    },
    {
      name: "METEOR",
      value: metrics.METEOR,
    },
    {
      name: "chrF",
      value: metrics.chrF,
    },
    {
      name: "TER",
      value: metrics.TER,
      inverse: true,
    },
    {
      name: "BERTScore",
      value: metrics.BERTScore,
    },
    {
      name: "COMET",
      value: metrics.COMET,
    },
  ];

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      {/* Header */}
      <div className="mb-5 flex items-center justify-between">

        <div className="flex items-center gap-3">
          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold">
              Traditional Metrics
            </h2>

            <BarChart3
              size={15}
              className="text-slate-500"
            />
          </div>
        </div>

        <div className="flex rounded-lg border border-white/10 bg-slate-900 p-1">

          <button className="rounded-md bg-violet-600 px-3 py-1.5 text-[10px] font-medium text-white">
            Scores
          </button>

          <button className="rounded-md px-3 py-1.5 text-[10px] text-slate-500 hover:text-slate-300">
            Chart
          </button>

        </div>

      </div>


      {/* Metrics */}
      <div className="space-y-4">

        {metricList.map((metric) => {

          const percentage = metric.value * 100;

          return (
            <div key={metric.name}>

              <div className="mb-1.5 flex items-center justify-between">

                <span className="text-xs font-medium text-slate-300">
                  {metric.name}
                </span>

                <span className="text-xs font-semibold text-slate-300">
                  {metric.value.toFixed(2)}
                </span>

              </div>

              <div className="h-2 overflow-hidden rounded-full bg-slate-800">

                <div
                  className={`h-full rounded-full ${
                    metric.inverse
                      ? "bg-rose-500"
                      : "bg-gradient-to-r from-blue-500 to-violet-500"
                  }`}
                  style={{
                    width: `${Math.min(percentage, 100)}%`,
                  }}
                />

              </div>

            </div>
          );
        })}

      </div>

      {/* Info */}
      <div className="mt-5 rounded-xl border border-white/5 bg-slate-900/50 p-3">

        <p className="text-[10px] leading-4 text-slate-500">
          Traditional metrics provide quantitative signals for
          translation quality and complement the evidence-grounded
          evaluation.
        </p>

      </div>

    </section>
  );
}

export default TraditionalMetrics;