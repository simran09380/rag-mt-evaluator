function OverallEvaluation({ evaluation }) {
  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <h2 className="text-base font-semibold">
          Overall Evaluation
        </h2>
      </div>

      <div className="flex flex-col items-center">

        {/* Score Ring */}
        <div className="relative flex h-36 w-36 items-center justify-center rounded-full border-[10px] border-emerald-500/20">

          <div className="absolute inset-0 rounded-full border-[10px] border-emerald-400 border-r-transparent border-b-transparent rotate-[-35deg]" />

          <div className="text-center">
            <p className="text-3xl font-bold">
              {evaluation.overall_score}
            </p>

            <p className="text-xs text-slate-500">
              / 100
            </p>
          </div>

        </div>

        {/* Quality */}
        <div className="mt-3 rounded-full bg-emerald-500/10 px-4 py-1.5">
          <span className="text-sm font-semibold text-emerald-400">
            ✓ {evaluation.quality_label}
          </span>
        </div>

      </div>


      {/* Bottom Information */}
      <div className="mt-6 grid grid-cols-2 gap-3">

        <div className="rounded-xl border border-white/10 bg-slate-900/60 p-3">
          <p className="text-xs text-slate-500">
            Confidence
          </p>

          <p className="mt-1 text-lg font-semibold">
            {evaluation.confidence}
          </p>

          <div className="mt-2 h-1.5 rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-violet-500"
              style={{
                width: `${evaluation.confidence * 100}%`,
              }}
            />
          </div>
        </div>


        <div className="rounded-xl border border-white/10 bg-slate-900/60 p-3">
          <p className="text-xs text-slate-500">
            Translation Quality
          </p>

          <p className="mt-1 text-sm font-semibold text-emerald-400">
            High Quality
          </p>
        </div>

      </div>

    </section>
  );
}

export default OverallEvaluation;