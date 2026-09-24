import {
  FileInput,
  Languages,
  Search,
  Layers3,
  Database,
  ScanSearch,
  SlidersHorizontal,
  BarChart3,
  Sparkles,
  TriangleAlert,
  Check,
  LoaderCircle,
} from "lucide-react";

const pipelineSteps = [
  {
    id: 1,
    name: "Data Ingestion",
    icon: FileInput,
  },
  {
    id: 2,
    name: "Linguistic Preprocessing",
    icon: Languages,
  },
  {
    id: 3,
    name: "Query Generation",
    icon: Search,
  },
  {
    id: 4,
    name: "Chunking",
    icon: Layers3,
  },
  {
    id: 5,
    name: "Embeddings & Indexing",
    icon: Database,
  },
  {
    id: 6,
    name: "Hybrid Retrieval",
    icon: ScanSearch,
  },
  {
    id: 7,
    name: "Reranking",
    icon: SlidersHorizontal,
  },
  {
    id: 8,
    name: "Traditional Metrics",
    icon: BarChart3,
  },
  {
    id: 9,
    name: "LLM Evaluation",
    icon: Sparkles,
  },
  {
    id: 10,
    name: "Error Classification",
    icon: TriangleAlert,
  },
];

function EvaluationPipeline({
  currentStep = 0,
  isEvaluating = false,
}) {
  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/[0.03] p-6">

      {/* Header */}
      <div className="mb-7 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">

        <div className="flex items-center gap-3">

          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div>
            <h2 className="text-lg font-semibold">
              Evaluation Pipeline
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              {isEvaluating
                ? "Processing your translation through the evaluation pipeline..."
                : currentStep === 10
                  ? "Evaluation completed successfully."
                  : "10-stage translation evaluation"}
            </p>
          </div>

        </div>

        {isEvaluating && (
          <div className="flex items-center gap-2 text-xs text-violet-400">

            <LoaderCircle
              size={14}
              className="animate-spin"
            />

            Processing

          </div>
        )}

      </div>


      {/* Pipeline */}
      <div className="relative">

        {/* Connecting Line */}
        <div
          className="
            pointer-events-none
            absolute
            left-[5%]
            right-[5%]
            top-7
            hidden
            h-px
            bg-slate-800
            xl:block
          "
        />

        {/* Progress Line */}
        <div
          className="
            pointer-events-none
            absolute
            left-[5%]
            top-7
            hidden
            h-px
            bg-gradient-to-r from-blue-500 to-violet-500
            transition-all duration-700
            xl:block
          "
          style={{
            width:
              currentStep > 1
                ? `${((currentStep - 1) / 9) * 90}%`
                : "0%",
          }}
        />


        {/* Steps */}
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-5 xl:grid-cols-10">

          {pipelineSteps.map((step) => {

            const Icon = step.icon;

            const completed =
              step.id < currentStep ||
              (step.id === currentStep && !isEvaluating);

            const active =
              step.id === currentStep && isEvaluating;

            return (
              <PipelineStep
                key={step.id}
                step={step}
                Icon={Icon}
                completed={completed}
                active={active}
              />
            );
          })}

        </div>

      </div>

    </section>
  );
}


/* =========================================================
   Pipeline Step
========================================================= */

function PipelineStep({
  step,
  Icon,
  completed,
  active,
}) {
  let status = "Waiting";

  if (completed) {
    status = "Completed";
  } else if (active) {
    status = "Processing";
  }

  return (
    <div className="group relative">

      {/* Circle */}
      <div
        className={`
          relative z-10 mx-auto
          flex h-14 w-14
          items-center justify-center
          rounded-full
          border
          transition-all duration-500

          ${
            completed
              ? "border-emerald-400/50 bg-emerald-500/10"
              : active
                ? "border-violet-400 bg-violet-500/10 shadow-lg shadow-violet-900/30"
                : "border-violet-400/20 bg-[#0a1025]"
          }
        `}
      >

        {completed ? (
          <Check
            size={21}
            className="text-emerald-400"
          />
        ) : active ? (
          <LoaderCircle
            size={21}
            className="animate-spin text-violet-400"
          />
        ) : (
          <Icon
            size={21}
            className="text-violet-400"
          />
        )}

      </div>


      {/* Number */}
      <div
        className={`
          absolute left-1/2 top-[43px]
          z-20 flex h-5 w-5
          -translate-x-1/2
          items-center justify-center
          rounded-full
          border border-[#0a1025]
          text-[9px] font-bold

          ${
            completed
              ? "bg-emerald-500 text-white"
              : active
                ? "bg-violet-600 text-white"
                : "bg-slate-700 text-slate-300"
          }
        `}
      >
        {step.id}
      </div>


      {/* Name */}
      <div className="mt-5 px-1 text-center">

        <p
          className={`
            text-[11px] font-medium leading-4
            ${
              completed
                ? "text-emerald-300"
                : active
                  ? "text-violet-300"
                  : "text-slate-400"
            }
          `}
        >
          {step.name}
        </p>

        <p
          className={`
            mt-2 text-[9px]
            ${
              completed
                ? "text-emerald-500"
                : active
                  ? "text-violet-400"
                  : "text-slate-600"
            }
          `}
        >
          {status}
        </p>

      </div>

    </div>
  );
}

export default EvaluationPipeline;