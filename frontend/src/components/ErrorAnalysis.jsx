import { useState } from "react";
import {
  AlertTriangle,
  ChevronDown,
  ShieldAlert,
  CheckCircle2,
} from "lucide-react";

function ErrorAnalysis({ errorAnalysis = {} }) {
  const [openError, setOpenError] = useState(null);

  const errors = Array.isArray(errorAnalysis?.errors)
    ? errorAnalysis.errors
    : [];

  const totalErrors =
    Number(errorAnalysis?.total_errors ?? errors.length);

  const majorErrors =
    Number(errorAnalysis?.major_errors ?? 0);

  const minorErrors =
    Number(errorAnalysis?.minor_errors ?? 0);

  const totalPenalty =
    Number(errorAnalysis?.total_penalty ?? 0);

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <div>
          <h2 className="text-base font-semibold">
            MQM Error Analysis
          </h2>

          <p className="mt-1 text-[10px] text-slate-500">
            Detailed translation errors detected by MQM classification
          </p>
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-2">
        <SummaryCard
          label="Total"
          value={totalErrors}
        />

        <SummaryCard
          label="Major"
          value={majorErrors}
          danger
        />

        <SummaryCard
          label="Minor"
          value={minorErrors}
        />
      </div>

      {/* Penalty */}
      <div className="mt-3 flex items-center justify-between rounded-xl border border-white/5 bg-slate-900/50 px-3 py-2.5">
        <span className="text-[10px] text-slate-500">
          Total MQM Penalty
        </span>

        <span className="text-xs font-semibold text-rose-400">
          {totalPenalty.toFixed(3)}
        </span>
      </div>

      {/* No Errors */}
      {errors.length === 0 ? (
        <div className="mt-4 flex items-center gap-3 rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-4">
          <CheckCircle2
            size={18}
            className="shrink-0 text-emerald-400"
          />

          <div>
            <p className="text-xs font-semibold text-emerald-300">
              No MQM errors detected
            </p>

            <p className="mt-1 text-[10px] leading-4 text-slate-500">
              The MQM classifier did not identify any translation
              errors for this evaluation.
            </p>
          </div>
        </div>
      ) : (
        <div className="mt-4 space-y-3">
          <div className="flex items-center justify-between">
            <p className="text-[10px] font-medium uppercase tracking-wider text-slate-600">
              Detected Errors
            </p>

            <span className="text-[10px] text-slate-600">
              {errors.length} found
            </span>
          </div>

          {errors.map((error, index) => {
            const errorId =
              error?.id ||
              error?.error_id ||
              `MQM-${index + 1}`;

            const isOpen = openError === errorId;

            return (
              <ErrorCard
                key={errorId}
                error={error}
                index={index}
                isOpen={isOpen}
                onToggle={() =>
                  setOpenError(
                    isOpen ? null : errorId
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


/* -------------------------------------------------
   SUMMARY CARD
------------------------------------------------- */

function SummaryCard({
  label,
  value,
  danger = false,
}) {
  return (
    <div className="rounded-xl border border-white/5 bg-slate-900/50 p-3">
      <p className="text-[9px] uppercase tracking-wider text-slate-600">
        {label}
      </p>

      <p
        className={`mt-1 text-lg font-bold ${
          danger
            ? "text-rose-400"
            : "text-slate-200"
        }`}
      >
        {value}
      </p>
    </div>
  );
}


/* -------------------------------------------------
   ERROR CARD
------------------------------------------------- */

function ErrorCard({
  error,
  index,
  isOpen,
  onToggle,
}) {
  const severity = String(
    error?.severity || "unknown"
  ).toLowerCase();

  const severityClass =
    severity === "major"
      ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
      : severity === "minor"
      ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
      : "bg-slate-500/10 text-slate-400 border-slate-500/20";

  const category =
    error?.category ||
    error?.error_type ||
    error?.type ||
    "Unclassified";

  const message =
    error?.description ||
    error?.reason ||
    error?.message ||
    error?.explanation ||
    "No detailed explanation was provided.";

  return (
    <div
      className={`rounded-xl border bg-slate-900/50 transition ${
        isOpen
          ? "border-violet-500/30"
          : "border-white/5"
      }`}
    >
      {/* Summary */}
      <button
        type="button"
        onClick={onToggle}
        className="w-full p-4 text-left"
      >
        <div className="flex items-start gap-3">
          <div
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
              severity === "major"
                ? "bg-rose-500/10"
                : "bg-amber-500/10"
            }`}
          >
            <AlertTriangle
              size={15}
              className={
                severity === "major"
                  ? "text-rose-400"
                  : "text-amber-400"
              }
            />
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold text-slate-200">
                  Error #{index + 1}
                </p>

                <p className="mt-1 text-[10px] text-slate-500">
                  {formatLabel(category)}
                </p>
              </div>

              <span
                className={`rounded-md border px-2 py-1 text-[9px] font-semibold uppercase ${severityClass}`}
              >
                {severity}
              </span>
            </div>

            <p className="mt-3 line-clamp-2 text-[11px] leading-5 text-slate-400">
              {message}
            </p>

            <div className="mt-3 flex items-center justify-between border-t border-white/5 pt-3">
              <span className="text-[10px] text-slate-600">
                {isOpen
                  ? "Hide details"
                  : "View error details"}
              </span>

              <ChevronDown
                size={14}
                className={`text-slate-600 transition-transform ${
                  isOpen ? "rotate-180" : ""
                }`}
              />
            </div>
          </div>
        </div>
      </button>

      {/* Details */}
      {isOpen && (
        <div className="border-t border-white/5 px-4 pb-4 pt-4">
          <div className="space-y-3">
            <DetailRow
              label="Category"
              value={formatLabel(category)}
            />

            <DetailRow
              label="Severity"
              value={formatLabel(severity)}
            />

            <DetailRow
              label="Description"
              value={message}
            />

            {/* Show other actual backend fields */}
            {Object.entries(error).map(
              ([key, value]) => {
                if (
                  [
                    "severity",
                    "category",
                    "error_type",
                    "type",
                    "description",
                    "reason",
                    "message",
                    "explanation",
                  ].includes(key)
                ) {
                  return null;
                }

                if (
                  value === null ||
                  value === undefined ||
                  value === ""
                ) {
                  return null;
                }

                return (
                  <DetailRow
                    key={key}
                    label={formatLabel(key)}
                    value={formatValue(value)}
                  />
                );
              }
            )}
          </div>
        </div>
      )}
    </div>
  );
}


/* -------------------------------------------------
   DETAIL ROW
------------------------------------------------- */

function DetailRow({ label, value }) {
  return (
    <div className="rounded-lg border border-white/5 bg-black/10 p-3">
      <p className="text-[9px] font-medium uppercase tracking-wider text-slate-600">
        {label}
      </p>

      <p className="mt-1 text-[11px] leading-5 text-slate-400">
        {value}
      </p>
    </div>
  );
}


/* -------------------------------------------------
   HELPERS
------------------------------------------------- */

function formatLabel(value) {
  if (!value) return "Not available";

  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) =>
      char.toUpperCase()
    );
}


function formatValue(value) {
  if (Array.isArray(value)) {
    return value.join(", ");
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

export default ErrorAnalysis;