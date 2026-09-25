import { useState } from "react";
import {
  Database,
  ChevronDown,
  FileText,
  ShieldCheck,
  Search,
} from "lucide-react";

function RetrievedEvidence({ evidence = [] }) {
  const [openEvidence, setOpenEvidence] = useState(null);

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <div>
          <h2 className="text-base font-semibold">
            Retrieved Evidence
          </h2>

          <p className="mt-1 text-[10px] text-slate-500">
            Evidence retrieved from the evaluation knowledge base
          </p>
        </div>
      </div>

      {evidence.length === 0 ? (
        <div className="rounded-xl border border-white/5 bg-slate-900/40 p-5 text-center">
          <Database
            size={20}
            className="mx-auto text-slate-600"
          />

          <p className="mt-2 text-xs text-slate-500">
            No retrieval evidence was returned.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {evidence.map((item, index) => {
            const isOpen = openEvidence === item.id;

            return (
              <EvidenceCard
                key={`${item.id}-${index}`}
                item={item}
                isOpen={isOpen}
                onToggle={() =>
                  setOpenEvidence(
                    isOpen ? null : item.id
                  )
                }
              />
            );
          })}
        </div>
      )}
    </section>
  );
}


function EvidenceCard({
  item,
  isOpen,
  onToggle,
}) {
  return (
    <div
      className={`rounded-xl border bg-slate-900/50 transition ${
        isOpen
          ? "border-violet-500/30"
          : "border-white/5"
      }`}
    >
      {/* Main */}
      <div className="p-4">
        <div className="flex items-start gap-3">
          {/* ID */}
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-violet-500/10 text-[10px] font-bold text-violet-400">
            {item.id}
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold text-slate-200">
                  {formatLabel(item.title)}
                </p>

                <div className="mt-1 flex flex-wrap gap-2">
                  {item.query_type && (
                    <span className="rounded-md bg-blue-500/10 px-2 py-0.5 text-[9px] text-blue-400">
                      {formatLabel(item.query_type)}
                    </span>
                  )}

                  {item.chunk_type && (
                    <span className="rounded-md bg-violet-500/10 px-2 py-0.5 text-[9px] text-violet-400">
                      {formatLabel(item.chunk_type)}
                    </span>
                  )}
                </div>
              </div>

              <div className="shrink-0 text-right">
                <p className="text-xs font-semibold text-emerald-400">
                  {(Number(item.relevance || 0) * 100).toFixed(1)}%
                </p>

                <p className="text-[9px] text-slate-600">
                  relevance
                </p>
              </div>
            </div>

            {/* Evidence Content */}
            {item.content && (
              <div className="mt-3 rounded-lg border border-white/5 bg-black/10 p-3">
                <p className="text-[11px] leading-5 text-slate-400">
                  {item.content}
                </p>
              </div>
            )}

            {/* Expand */}
            <button
              type="button"
              onClick={onToggle}
              className="mt-3 flex w-full items-center justify-between border-t border-white/5 pt-3 text-left"
            >
              <span className="flex items-center gap-2 text-[10px] font-medium text-slate-500 hover:text-slate-300">
                <Search size={12} />

                {isOpen
                  ? "Hide evidence details"
                  : "View evidence details"}
              </span>

              <ChevronDown
                size={14}
                className={`text-slate-600 transition-transform ${
                  isOpen ? "rotate-180" : ""
                }`}
              />
            </button>
          </div>
        </div>
      </div>

      {/* Details */}
      {isOpen && (
        <div className="border-t border-white/5 px-4 pb-4 pt-4">
          {/* Source / Target */}
          {(item.source || item.target) && (
            <div className="grid gap-3">
              {item.source && (
                <div>
                  <div className="mb-1 flex items-center gap-2">
                    <FileText
                      size={12}
                      className="text-blue-400"
                    />

                    <span className="text-[10px] font-medium uppercase tracking-wider text-slate-600">
                      Source
                    </span>
                  </div>

                  <p className="rounded-lg bg-blue-500/5 p-2.5 text-[11px] leading-5 text-slate-400">
                    {item.source}
                  </p>
                </div>
              )}

              {item.target && (
                <div>
                  <div className="mb-1 flex items-center gap-2">
                    <FileText
                      size={12}
                      className="text-violet-400"
                    />

                    <span className="text-[10px] font-medium uppercase tracking-wider text-slate-600">
                      Retrieved Target
                    </span>
                  </div>

                  <p className="rounded-lg bg-violet-500/5 p-2.5 text-[11px] leading-5 text-slate-400">
                    {item.target}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Retrieval Scores */}
          <div className="mt-4">
            <p className="mb-2 text-[10px] font-medium uppercase tracking-wider text-slate-600">
              Retrieval Scores
            </p>

            <div className="grid grid-cols-2 gap-2">
              <ScoreItem
                label="Relevance"
                value={item.relevance}
              />

              <ScoreItem
                label="Semantic"
                value={item.semantic_score}
              />

              <ScoreItem
                label="Source Similarity"
                value={item.source_similarity}
              />

              <ScoreItem
                label="Hypothesis Similarity"
                value={item.hypothesis_similarity}
              />

              <ScoreItem
                label="Terminology"
                value={item.terminology_score}
              />

              <ScoreItem
                label="Entity"
                value={item.entity_score}
              />

              <ScoreItem
                label="Authority"
                value={item.authority}
              />

              <ScoreItem
                label="Verification"
                value={item.verification_score}
              />
            </div>
          </div>

          {/* Metadata */}
          <div className="mt-4 border-t border-white/5 pt-4">
            <p className="mb-2 text-[10px] font-medium uppercase tracking-wider text-slate-600">
              Retrieval Metadata
            </p>

            <div className="space-y-2 text-[10px]">
              <MetaRow
                label="Query Type"
                value={formatLabel(item.query_type)}
              />

              <MetaRow
                label="Chunk Type"
                value={formatLabel(item.chunk_type)}
              />

              <MetaRow
                label="Source Type"
                value={formatLabel(item.title)}
              />

              {item.source && (
                <MetaRow
                  label="Source ID"
                  value={item.source}
                />
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


function ScoreItem({ label, value }) {
  const score = Number(value || 0);

  return (
    <div className="rounded-lg border border-white/5 bg-black/10 p-2.5">
      <div className="flex items-center justify-between gap-2">
        <span className="text-[9px] text-slate-600">
          {label}
        </span>

        <span className="text-[10px] font-semibold text-slate-300">
          {score.toFixed(3)}
        </span>
      </div>

      <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-violet-500"
          style={{
            width: `${Math.min(
              Math.max(score * 100, 0),
              100
            )}%`,
          }}
        />
      </div>
    </div>
  );
}


function MetaRow({ label, value }) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-slate-600">
        {label}
      </span>

      <span className="max-w-[65%] truncate text-right text-slate-400">
        {value || "Not available"}
      </span>
    </div>
  );
}


function formatLabel(value) {
  if (!value) return "Not available";

  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) =>
      char.toUpperCase()
    );
}

export default RetrievedEvidence;