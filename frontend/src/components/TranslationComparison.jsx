import { useState } from "react";
import {
  Copy,
  Check,
  GitCompare,
  X,
  Plus,
} from "lucide-react";

function TranslationComparison({ evaluation = {} }) {
  const [showDifferences, setShowDifferences] = useState(false);
  const [copiedField, setCopiedField] = useState(null);

  const source = evaluation?.source_sentence || "";
  const translation = evaluation?.machine_translation || "";
  const reference = evaluation?.reference || "";

  const handleCopy = async (text, field) => {
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);

      setCopiedField(field);

      setTimeout(() => {
        setCopiedField(null);
      }, 1500);
    } catch (error) {
      console.error("Copy failed:", error);
    }
  };

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      {/* Header */}
      <div className="mb-5 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="h-5 w-1 rounded-full bg-violet-500" />

          <div>
            <h2 className="text-base font-semibold">
              Translation Comparison
            </h2>

            <p className="mt-1 text-[10px] text-slate-500">
              Compare source, machine translation and reference
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() =>
            setShowDifferences((previous) => !previous)
          }
          disabled={!reference}
          className={`flex items-center gap-2 rounded-lg border px-3 py-2 text-[10px] font-medium transition ${
            !reference
              ? "cursor-not-allowed border-white/5 text-slate-700"
              : showDifferences
              ? "border-violet-500/30 bg-violet-500/10 text-violet-300"
              : "border-violet-500/30 text-violet-300 hover:bg-violet-500/10"
          }`}
        >
          <GitCompare size={13} />

          {showDifferences
            ? "Hide Differences"
            : "View Differences"}
        </button>
      </div>

      {/* Translation Fields */}
      <div className="space-y-3">
        <TranslationBlock
          label="Source"
          language="English"
          value={source}
          badgeClass="bg-blue-500/10 text-blue-400"
          copied={copiedField === "source"}
          onCopy={() => handleCopy(source, "source")}
        />

        <TranslationBlock
          label="Machine Translation"
          language="Hindi"
          value={translation}
          badgeClass="bg-violet-500/10 text-violet-400"
          copied={copiedField === "translation"}
          onCopy={() =>
            handleCopy(translation, "translation")
          }
        />

        <TranslationBlock
          label="Reference"
          language="Hindi"
          value={reference}
          badgeClass="bg-violet-500/10 text-violet-400"
          copied={copiedField === "reference"}
          onCopy={() =>
            handleCopy(reference, "reference")
          }
        />
      </div>

      {/* Differences */}
      {showDifferences && reference && (
        <DifferenceView
          translation={translation}
          reference={reference}
        />
      )}

      {/* No Reference */}
      {showDifferences && !reference && (
        <div className="mt-4 rounded-xl border border-amber-500/10 bg-amber-500/5 p-4">
          <p className="text-xs font-medium text-amber-300">
            Reference translation unavailable
          </p>

          <p className="mt-1 text-[10px] leading-4 text-slate-500">
            Translation differences can only be shown when a
            reference translation is provided.
          </p>
        </div>
      )}
    </section>
  );
}


/* =========================================================
   Translation Block
========================================================= */

function TranslationBlock({
  label,
  language,
  value,
  badgeClass,
  copied,
  onCopy,
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 p-3">
      <div className="flex items-start gap-3">
        {/* Language Badge */}
        <div
          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-[10px] font-bold ${badgeClass}`}
        >
          {language === "English" ? "EN" : "HI"}
        </div>

        {/* Text */}
        <div className="min-w-0 flex-1">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-[10px] font-semibold text-slate-300">
                {label}
              </p>

              <p className="mt-0.5 text-[9px] text-slate-600">
                {language}
              </p>
            </div>

            {/* Functional Copy */}
            <button
              type="button"
              onClick={onCopy}
              disabled={!value}
              title={value ? `Copy ${label}` : "Nothing to copy"}
              className={`rounded-md p-1.5 transition ${
                !value
                  ? "cursor-not-allowed text-slate-700"
                  : copied
                  ? "bg-emerald-500/10 text-emerald-400"
                  : "text-slate-600 hover:bg-white/5 hover:text-slate-300"
              }`}
            >
              {copied ? (
                <Check size={14} />
              ) : (
                <Copy size={14} />
              )}
            </button>
          </div>

          <p className="mt-2 text-xs leading-5 text-slate-400">
            {value || "Not available"}
          </p>
        </div>
      </div>
    </div>
  );
}


/* =========================================================
   Difference View
========================================================= */

function DifferenceView({
  translation,
  reference,
}) {
  const differences = compareTexts(
    translation,
    reference
  );

  const hasDifferences = differences.some(
    (item) => item.type !== "same"
  );

  return (
    <div className="mt-4 rounded-xl border border-violet-500/10 bg-violet-500/[0.03] p-4">
      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-200">
            Translation Differences
          </p>

          <p className="mt-1 text-[10px] text-slate-600">
            Machine translation compared with the reference
          </p>
        </div>

        <div className="flex items-center gap-3 text-[9px]">
          <span className="flex items-center gap-1 text-rose-400">
            <span className="h-2 w-2 rounded-sm bg-rose-500/40" />
            Removed
          </span>

          <span className="flex items-center gap-1 text-emerald-400">
            <span className="h-2 w-2 rounded-sm bg-emerald-500/40" />
            Added
          </span>
        </div>
      </div>

      {!hasDifferences ? (
        <div className="rounded-lg border border-emerald-500/10 bg-emerald-500/5 p-3">
          <p className="text-xs font-medium text-emerald-300">
            No textual differences detected.
          </p>

          <p className="mt-1 text-[10px] text-slate-500">
            Machine translation and reference contain the same
            token sequence.
          </p>
        </div>
      ) : (
        <div className="rounded-xl border border-white/5 bg-slate-950/40 p-4">
          <p className="mb-2 text-[9px] uppercase tracking-wider text-slate-600">
            Comparison
          </p>

          <div className="text-xs leading-7 text-slate-300">
            {differences.map((item, index) => {
              if (item.type === "same") {
                return (
                  <span key={index}>
                    {item.text}{" "}
                  </span>
                );
              }

              if (item.type === "removed") {
                return (
                  <span
                    key={index}
                    className="mx-0.5 rounded bg-rose-500/15 px-1 py-0.5 text-rose-300 line-through"
                    title="Present in machine translation but not in reference"
                  >
                    {item.text}
                  </span>
                );
              }

              return (
                <span
                  key={index}
                  className="mx-0.5 rounded bg-emerald-500/15 px-1 py-0.5 text-emerald-300"
                  title="Present in reference but not in machine translation"
                >
                  {item.text}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* Difference Summary */}
      {hasDifferences && (
        <div className="mt-3 grid grid-cols-2 gap-2">
          <DifferenceSummary
            icon={X}
            label="Removed from MT"
            value={countType(differences, "removed")}
            type="removed"
          />

          <DifferenceSummary
            icon={Plus}
            label="Added in Reference"
            value={countType(differences, "added")}
            type="added"
          />
        </div>
      )}
    </div>
  );
}


/* =========================================================
   Difference Summary
========================================================= */

function DifferenceSummary({
  icon: Icon,
  label,
  value,
  type,
}) {
  return (
    <div className="rounded-lg border border-white/5 bg-slate-900/50 p-3">
      <div className="flex items-center gap-2">
        <Icon
          size={13}
          className={
            type === "removed"
              ? "text-rose-400"
              : "text-emerald-400"
          }
        />

        <span className="text-[9px] text-slate-600">
          {label}
        </span>
      </div>

      <p className="mt-1 text-sm font-semibold text-slate-300">
        {value}
      </p>
    </div>
  );
}


/* =========================================================
   Simple Token Comparison
========================================================= */

function compareTexts(machineText, referenceText) {
  const machineTokens = tokenize(machineText);
  const referenceTokens = tokenize(referenceText);

  const result = [];

  let i = 0;
  let j = 0;

  while (
    i < machineTokens.length ||
    j < referenceTokens.length
  ) {
    const machineToken = machineTokens[i];
    const referenceToken = referenceTokens[j];

    if (
      machineToken &&
      referenceToken &&
      normalize(machineToken) === normalize(referenceToken)
    ) {
      result.push({
        type: "same",
        text: machineToken,
      });

      i++;
      j++;
      continue;
    }

    /*
     * Machine token removed / replaced.
     */
    if (
      machineToken &&
      (!referenceToken ||
        !referenceTokens
          .slice(j, j + 2)
          .some(
            (token) =>
              normalize(token) === normalize(machineToken)
          ))
    ) {
      result.push({
        type: "removed",
        text: machineToken,
      });

      i++;
      continue;
    }

    /*
     * Reference token added / replacement.
     */
    if (referenceToken) {
      result.push({
        type: "added",
        text: referenceToken,
      });

      j++;
      continue;
    }
  }

  return result;
}


function tokenize(text) {
  if (!text) return [];

  return text
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}


function normalize(text) {
  return String(text)
    .toLowerCase()
    .replace(/[.,!?;:"'()[\]{}]/g, "");
}


function countType(items, type) {
  return items.filter(
    (item) => item.type === type
  ).length;
}

export default TranslationComparison;