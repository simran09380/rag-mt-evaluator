import {
  Database,
  ExternalLink,
  ShieldCheck,
} from "lucide-react";

function RetrievedEvidence({ evidence }) {
  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      {/* Header */}
      <div className="mb-5 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div className="flex items-center gap-2">

            <h2 className="text-base font-semibold">
              Retrieved Evidence
            </h2>

            <span className="rounded-full bg-violet-500/10 px-2 py-0.5 text-[9px] font-medium text-violet-400">
              Top {evidence.length}
            </span>

          </div>

        </div>

        <button className="flex items-center gap-1 text-xs text-violet-400 hover:text-violet-300">
          View All
          <ExternalLink size={12} />
        </button>

      </div>


      {/* Evidence Cards */}
      <div className="space-y-3">

        {evidence.map((item) => (

          <div
            key={item.id}
            className="rounded-xl border border-white/10 bg-slate-900/60 p-3.5 transition hover:border-violet-500/20"
          >

            <div className="flex gap-3">

              {/* Evidence ID */}
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-violet-500/10 text-xs font-bold text-violet-400">
                {item.id}
              </div>


              {/* Content */}
              <div className="min-w-0 flex-1">

                <div className="flex items-start justify-between gap-2">

                  <div>
                    <p className="text-xs font-semibold text-slate-200">
                      {item.title}
                    </p>

                    <p className="mt-1 text-[10px] leading-4 text-slate-500">
                      "{item.content}"
                    </p>
                  </div>

                </div>


                {/* Scores */}
                <div className="mt-3 flex flex-wrap items-center gap-3">

                  <span className="text-[10px] text-slate-500">
                    Relevance:
                    <strong className="ml-1 text-slate-300">
                      {item.relevance.toFixed(2)}
                    </strong>
                  </span>

                  <span className="text-[10px] text-slate-500">
                    Authority:
                    <strong className="ml-1 text-slate-300">
                      {item.authority.toFixed(2)}
                    </strong>
                  </span>

                </div>

              </div>

            </div>


            {/* Used For */}
            <div className="mt-3 flex items-center justify-between border-t border-white/5 pt-3">

              <span className="flex items-center gap-1.5 text-[10px] text-emerald-400">

                <ShieldCheck size={12} />

                Evidence used for

              </span>

              <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-[9px] font-medium text-emerald-400">
                {item.used_for}
              </span>

            </div>

          </div>

        ))}

      </div>


      {/* RAG indicator */}
      <div className="mt-4 flex items-center gap-2 rounded-xl border border-blue-500/10 bg-blue-500/5 p-3">

        <Database
          size={15}
          className="text-blue-400"
        />

        <p className="text-[10px] leading-4 text-slate-400">
          Retrieved evidence is used to ground the evaluation
          and provide traceable support for the final assessment.
        </p>

      </div>

    </section>
  );
}

export default RetrievedEvidence;