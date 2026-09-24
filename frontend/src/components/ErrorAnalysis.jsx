import {
  AlertTriangle,
  CircleAlert,
  Minus,
} from "lucide-react";

function ErrorAnalysis({ errorAnalysis }) {
  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      {/* Header */}
      <div className="mb-5 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div className="flex items-center gap-2">

            <h2 className="text-base font-semibold">
              Error Analysis
            </h2>

            <span className="rounded-md bg-orange-500/10 px-2 py-1 text-[9px] font-medium text-orange-400">
              MQM
            </span>

          </div>

        </div>

        <button className="rounded-lg border border-white/10 px-3 py-1.5 text-[10px] text-slate-400 hover:text-white">
          View Details
        </button>

      </div>


      {/* Summary */}
      <div className="grid grid-cols-3 gap-2">

        <SummaryCard
          label="Total Errors"
          value={errorAnalysis.total_errors}
          type="total"
        />

        <SummaryCard
          label="Major Errors"
          value={errorAnalysis.major_errors}
          type="major"
        />

        <SummaryCard
          label="Minor Errors"
          value={errorAnalysis.minor_errors}
          type="minor"
        />

      </div>


      {/* Tabs */}
      <div className="mt-5 flex gap-2">

        <button className="rounded-md bg-violet-600 px-3 py-1.5 text-[10px] font-medium text-white">
          By Category
        </button>

        <button className="rounded-md border border-white/10 px-3 py-1.5 text-[10px] text-slate-500 hover:text-slate-300">
          Highlighted Translation
        </button>

      </div>


      {/* Categories */}
      <div className="mt-5 space-y-3">

        {errorAnalysis.categories.map((category) => {

          const maxCount = Math.max(
            ...errorAnalysis.categories.map(
              (item) => item.count
            ),
            1
          );

          const width =
            (category.count / maxCount) * 100;

          return (
            <div key={category.name}>

              <div className="mb-1 flex items-center justify-between">

                <span className="text-[10px] text-slate-400">
                  {category.name}
                </span>

                <span className="text-[10px] font-medium text-slate-500">
                  {category.count}
                </span>

              </div>

              <div className="h-1.5 overflow-hidden rounded-full bg-slate-800">

                <div
                  className={`h-full rounded-full ${
                    category.name === "Mistranslation" ||
                    category.name === "Omission"
                      ? "bg-rose-400"
                      : category.name === "Wrong Terminology"
                        ? "bg-emerald-400"
                        : "bg-blue-500"
                  }`}
                  style={{
                    width: `${width}%`,
                  }}
                />

              </div>

            </div>
          );
        })}

      </div>


      {/* Error explanation */}
      <div className="mt-5 rounded-xl border border-orange-500/10 bg-orange-500/5 p-3">

        <div className="flex gap-2">

          <AlertTriangle
            size={14}
            className="mt-0.5 shrink-0 text-orange-400"
          />

          <div>

            <p className="text-[10px] font-semibold text-orange-300">
              MQM Error Classification
            </p>

            <p className="mt-1 text-[10px] leading-4 text-slate-500">
              Detected translation issues are grouped by
              standardized error categories and severity.
            </p>

          </div>

        </div>

      </div>

    </section>
  );
}


/* ---------------------------------------------
   Summary Card
--------------------------------------------- */

function SummaryCard({
  label,
  value,
  type,
}) {
  const styles = {
    total: {
      icon: CircleAlert,
      container: "border-blue-500/10 bg-blue-500/5",
      text: "text-blue-400",
    },

    major: {
      icon: AlertTriangle,
      container: "border-rose-500/10 bg-rose-500/5",
      text: "text-rose-400",
    },

    minor: {
      icon: Minus,
      container: "border-orange-500/10 bg-orange-500/5",
      text: "text-orange-400",
    },
  };

  const style = styles[type];
  const Icon = style.icon;

  return (
    <div
      className={`rounded-xl border p-3 ${style.container}`}
    >

      <div className="flex items-center gap-2">

        <Icon
          size={13}
          className={style.text}
        />

        <p className="text-[9px] text-slate-500">
          {label}
        </p>

      </div>

      <p
        className={`mt-2 text-xl font-bold ${style.text}`}
      >
        {value}
      </p>

    </div>
  );
}

export default ErrorAnalysis;