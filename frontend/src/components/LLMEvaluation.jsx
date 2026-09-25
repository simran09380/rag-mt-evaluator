import { useState } from "react";
import {
  Brain,
  ChevronDown,
  ShieldCheck,
  ExternalLink,
  FileText,
} from "lucide-react";

function LLMEvaluation({
  evaluation = {},
  evidence = [],
}) {
  const [openDimension, setOpenDimension] = useState(null);
  const [selectedEvidence, setSelectedEvidence] = useState(null);

  const dimensions = [
    {
      key: "accuracy",
      label: "Accuracy",
      description:
        "Whether the translation preserves the meaning of the source.",
    },
    {
      key: "fluency",
      label: "Fluency",
      description:
        "Whether the translation is natural, grammatical, and readable.",
    },
    {
      key: "terminology",
      label: "Terminology",
      description:
        "Whether domain-specific terminology is translated correctly.",
    },
    {
      key: "named_entities",
      label: "Named Entities",
      description:
        "Whether names, places, organizations, and other entities are handled correctly.",
    },
    {
      key: "factual_consistency",
      label: "Factual Consistency",
      description:
        "Whether the translation preserves the facts expressed in the source.",
    },
    {
      key: "style",
      label: "Style",
      description:
        "Whether the translation follows an appropriate style and tone.",
    },
    {
      key: "omissions",
      label: "Omissions",
      description:
        "Whether important information from the source has been omitted.",
    },
    {
      key: "additions",
      label: "Additions",
      description:
        "Whether unsupported information has been added to the translation.",
    },
  ];

  const model = evaluation?.model || "Not available";

  const supportedByEvidence =
    evaluation?.supported_by_evidence === true;

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-semibold">
                LLM Evaluation
              </h2>

              <Brain
                size={15}
                className="text-violet-400"
              />
            </div>

            <p className="mt-1 text-[10px] text-slate-500">
              Evidence-grounded evaluation across 8 quality dimensions
            </p>
          </div>
        </div>

        {/* Model */}
        <div className="text-right">
          <p className="text-[9px] uppercase tracking-wider text-slate-600">
            Model
          </p>

          <p className="mt-1 text-[10px] font-medium text-slate-400">
            {model}
          </p>
        </div>
      </div>

      {/* Evidence Status */}
      <div className="mb-5 flex items-center justify-between rounded-xl border border-white/5 bg-slate-900/50 px-4 py-3">
        <div className="flex items-center gap-2">
          <ShieldCheck
            size={15}
            className={
              supportedByEvidence
                ? "text-emerald-400"
                : "text-slate-600"
            }
          />

          <div>
            <p className="text-xs font-medium text-slate-300">
              Evidence Grounding
            </p>

            <p className="mt-0.5 text-[9px] text-slate-600">
              Whether the LLM evaluation was supported by retrieved evidence
            </p>
          </div>
        </div>

        <span
          className={`rounded-full border px-2.5 py-1 text-[9px] font-semibold ${
            supportedByEvidence
              ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
              : "border-slate-500/10 bg-slate-500/10 text-slate-500"
          }`}
        >
          {supportedByEvidence
            ? "Supported"
            : "Not Supported"}
        </span>
      </div>

      {/* 8 Dimensions */}
      <div className="grid gap-3 md:grid-cols-2">
        {dimensions.map((dimension) => {
          const data =
            evaluation?.[dimension.key] || {};

          const isOpen =
            openDimension === dimension.key;

          return (
            <LLMDimensionCard
              key={dimension.key}
              dimension={dimension}
              data={data}
              isOpen={isOpen}
              onToggle={() =>
                setOpenDimension(
                  isOpen
                    ? null
                    : dimension.key
                )
              }
              onEvidenceClick={(id) => {
                const foundEvidence =
                  evidence.find(
                    (item) => item.id === id
                  );

                setSelectedEvidence(
                  foundEvidence
                    ? {
                        id,
                        evidence: foundEvidence,
                      }
                    : {
                        id,
                        evidence: null,
                      }
                );
              }}
            />
          );
        })}
      </div>

      {/* Selected Evidence */}
      {selectedEvidence && (
        <LinkedEvidence
          evidence={selectedEvidence.evidence}
          evidenceId={selectedEvidence.id}
          onClose={() =>
            setSelectedEvidence(null)
          }
        />
      )}
    </section>
  );
}


/* =========================================================
   LLM DIMENSION CARD
========================================================= */

function LLMDimensionCard({
  dimension,
  data,
  isOpen,
  onToggle,
  onEvidenceClick,
}) {
  const score =
    typeof data?.score === "number"
      ? data.score
      : null;

  const percentage =
    score !== null
      ? Math.min(Math.max(score * 20, 0), 100)
      : 0;

  const judgment =
    data?.judgment ||
    "No evaluation judgment was returned.";

  const evidenceIds = Array.isArray(
    data?.evidence_ids
  )
    ? data.evidence_ids
    : [];

  return (
    <div
      className={`rounded-xl border bg-slate-900/50 transition ${
        isOpen
          ? "border-violet-500/30"
          : "border-white/5"
      }`}
    >
      {/* Main */}
      <button
        type="button"
        onClick={onToggle}
        className="w-full p-4 text-left"
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold text-slate-200">
              {dimension.label}
            </p>

            <p className="mt-1 text-[9px] leading-4 text-slate-600">
              {dimension.description}
            </p>
          </div>

          <div className="text-right">
            <p className="text-lg font-bold text-slate-200">
              {score !== null ? score : "—"}
              <span className="ml-1 text-[9px] font-normal text-slate-600">
                / 5
              </span>
            </p>
          </div>
        </div>

        {/* Progress */}
        <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full rounded-full bg-gradient-to-r from-violet-500 to-blue-500 transition-all duration-500"
            style={{
              width: `${percentage}%`,
            }}
          />
        </div>

        <div className="mt-3 flex items-center justify-between">
          <span className="text-[10px] text-slate-500">
            {isOpen
              ? "Hide evaluation details"
              : "View evaluation details"}
          </span>

          <ChevronDown
            size={14}
            className={`text-slate-600 transition-transform ${
              isOpen ? "rotate-180" : ""
            }`}
          />
        </div>
      </button>

      {/* Details */}
      {isOpen && (
        <div className="border-t border-white/5 px-4 pb-4 pt-4">
          {/* Judgment */}
          <div className="rounded-lg border border-white/5 bg-black/10 p-3">
            <p className="text-[9px] font-medium uppercase tracking-wider text-slate-600">
              LLM Judgment
            </p>

            <p className="mt-1.5 text-[11px] leading-5 text-slate-300">
              {judgment}
            </p>
          </div>

          {/* Evidence IDs */}
          <div className="mt-3">
            <p className="mb-2 text-[9px] font-medium uppercase tracking-wider text-slate-600">
              Supporting Evidence
            </p>

            {evidenceIds.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {evidenceIds.map((id) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() =>
                      onEvidenceClick(id)
                    }
                    className="group flex items-center gap-1.5 rounded-md border border-violet-500/20 bg-violet-500/10 px-2.5 py-1.5 text-[10px] font-medium text-violet-300 transition hover:border-violet-400/40 hover:bg-violet-500/20"
                  >
                    {id}

                    <ExternalLink
                      size={10}
                      className="opacity-50 transition group-hover:opacity-100"
                    />
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-[10px] text-slate-600">
                No evidence ID was attached to this dimension.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


/* =========================================================
   LINKED EVIDENCE
========================================================= */

function LinkedEvidence({
  evidence,
  evidenceId,
  onClose,
}) {
  return (
    <div className="mt-5 rounded-xl border border-violet-500/20 bg-violet-500/[0.04] p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-500/10 text-[10px] font-bold text-violet-300">
            {evidenceId}
          </div>

          <div>
            <p className="text-xs font-semibold text-slate-200">
              Linked Evidence
            </p>

            <p className="mt-1 text-[9px] text-slate-600">
              Evidence referenced by the LLM evaluation
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="text-[10px] text-slate-600 transition hover:text-slate-300"
        >
          Close
        </button>
      </div>

      {evidence ? (
        <div className="mt-4">
          <div className="rounded-lg border border-white/5 bg-slate-950/40 p-3">
            <div className="flex items-center gap-2">
              <FileText
                size={13}
                className="text-violet-400"
              />

              <p className="text-[10px] font-semibold text-slate-300">
                {evidence.title || "Retrieved Evidence"}
              </p>
            </div>

            <p className="mt-2 text-[11px] leading-5 text-slate-400">
              {evidence.content ||
                evidence.target ||
                evidence.source ||
                "No evidence content available."}
            </p>
          </div>

          <div className="mt-3 grid grid-cols-2 gap-2">
            <EvidenceValue
              label="Relevance"
              value={evidence.relevance}
            />

            <EvidenceValue
              label="Authority"
              value={evidence.authority}
            />

            <EvidenceValue
              label="Semantic Score"
              value={evidence.semantic_score}
            />

            <EvidenceValue
              label="Verification"
              value={evidence.verification_score}
            />
          </div>
        </div>
      ) : (
        <div className="mt-4 rounded-lg border border-amber-500/10 bg-amber-500/5 p-3">
          <p className="text-[10px] text-amber-400">
            {evidenceId} was referenced by the LLM,
            but matching retrieved evidence was not
            available in the frontend evidence list.
          </p>
        </div>
      )}
    </div>
  );
}


function EvidenceValue({ label, value }) {
  const numericValue = Number(value ?? 0);

  return (
    <div className="rounded-lg border border-white/5 bg-slate-950/30 p-2.5">
      <p className="text-[9px] text-slate-600">
        {label}
      </p>

      <p className="mt-1 text-[10px] font-semibold text-slate-300">
        {numericValue.toFixed(3)}
      </p>
    </div>
  );
}

export default LLMEvaluation;