import { useMemo, useState } from "react";
import {
  ChevronRight,
  Search,
  SlidersHorizontal,
} from "lucide-react";

function getQualityLabel(score) {
  if (typeof score !== "number") {
    return "Not Available";
  }

  if (score >= 90) return "Excellent";
  if (score >= 75) return "Good";
  if (score >= 60) return "Needs Review";

  return "Poor";
}

function SentenceResultsTable({
  results = [],
  onSelectSentence,
}) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");

  const filteredResults = useMemo(() => {
    return results.filter((item) => {
      const searchText =
        search.toLowerCase();

      const matchesSearch =
        String(item?.sentence_id)
          .toLowerCase()
          .includes(searchText) ||
        item?.source
          ?.toLowerCase()
          .includes(searchText) ||
        item?.translation
          ?.toLowerCase()
          .includes(searchText);

      const matchesFilter =
        filter === "All" ||
        item?.quality_label === filter;

      return (
        matchesSearch &&
        matchesFilter
      );
    });
  }, [results, search, filter]);

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">

        <div>
          <h2 className="text-lg font-semibold text-white">
            Sentence Results
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Select a sentence to view its complete evaluation.
          </p>
        </div>

        {/* Search + Filter */}
        <div className="flex gap-2">

          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-slate-900/70 px-3 py-2.5">

            <Search
              size={14}
              className="text-slate-600"
            />

            <input
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              placeholder="Search sentences..."
              className="
                w-40
                bg-transparent
                text-xs
                text-slate-300
                outline-none
                placeholder:text-slate-600
              "
            />

          </div>

          <div className="relative">

            <SlidersHorizontal
              size={14}
              className="
                pointer-events-none
                absolute
                left-3
                top-1/2
                -translate-y-1/2
                text-slate-500
              "
            />

            <select
              value={filter}
              onChange={(e) =>
                setFilter(e.target.value)
              }
              className="
                appearance-none
                rounded-xl
                border border-white/10
                bg-slate-900/70
                py-2.5
                pl-9
                pr-8
                text-xs
                text-slate-400
                outline-none
                focus:border-violet-500/50
              "
            >
              <option value="All">
                All
              </option>

              <option value="Excellent">
                Excellent
              </option>

              <option value="Good">
                Good
              </option>

              <option value="Needs Review">
                Needs Review
              </option>

              <option value="Poor">
                Poor
              </option>
            </select>

          </div>

        </div>

      </div>

      {/* Count */}
      <div className="mt-4 text-[10px] text-slate-600">
        Showing {filteredResults.length} of{" "}
        {results.length} sentences
      </div>

      {/* Table */}
      <div className="mt-3 overflow-x-auto">

        <table className="w-full min-w-[850px] border-collapse">

          <thead>
            <tr className="border-b border-white/10">

              <th className="px-3 py-3 text-left text-[10px] font-medium uppercase tracking-wider text-slate-600">
                ID
              </th>

              <th className="px-3 py-3 text-left text-[10px] font-medium uppercase tracking-wider text-slate-600">
                Source
              </th>

              <th className="px-3 py-3 text-left text-[10px] font-medium uppercase tracking-wider text-slate-600">
                Translation
              </th>

              <th className="px-3 py-3 text-center text-[10px] font-medium uppercase tracking-wider text-slate-600">
                Score
              </th>

              <th className="px-3 py-3 text-center text-[10px] font-medium uppercase tracking-wider text-slate-600">
                Quality
              </th>

              <th className="px-3 py-3 text-center text-[10px] font-medium uppercase tracking-wider text-slate-600">
                Errors
              </th>

              <th className="px-3 py-3" />

            </tr>
          </thead>

          <tbody>

            {filteredResults.map((item) => (

              <tr
                key={item.sentence_id}
                onClick={() =>
                  onSelectSentence(item)
                }
                className="
                  cursor-pointer
                  border-b border-white/5
                  transition
                  hover:bg-violet-500/[0.04]
                "
              >

                {/* ID */}
                <td className="px-3 py-4">
                  <span className="text-xs font-semibold text-violet-400">
                    #
                    {String(
                      item.sentence_id
                    ).padStart(3, "0")}
                  </span>
                </td>

                {/* Source */}
                <td className="max-w-[230px] px-3 py-4">
                  <p className="truncate text-xs text-slate-400">
                    {item.source}
                  </p>
                </td>

                {/* Translation */}
                <td className="max-w-[230px] px-3 py-4">
                  <p className="truncate text-xs text-slate-300">
                    {item.translation}
                  </p>
                </td>

                {/* Score */}
                <td className="px-3 py-4 text-center">
                  <span className="text-sm font-bold text-slate-200">
                    {typeof item.overall_score ===
                    "number"
                      ? item.overall_score.toFixed(2)
                      : "—"}
                  </span>
                </td>

                {/* Quality */}
                <td className="px-3 py-4 text-center">
                  <QualityBadge
                    label={
                      item.quality_label ||
                      getQualityLabel(
                        item.overall_score
                      )
                    }
                  />
                </td>

                {/* Errors */}
                <td className="px-3 py-4 text-center">

                  <span
                    className={
                      item.error_count === 0
                        ? "text-xs font-medium text-emerald-400"
                        : "text-xs font-medium text-orange-400"
                    }
                  >
                    {item.error_count}
                  </span>

                </td>

                {/* Arrow */}
                <td className="px-3 py-4 text-right">

                  <ChevronRight
                    size={16}
                    className="text-slate-600"
                  />

                </td>

              </tr>

            ))}

            {filteredResults.length === 0 && (

              <tr>

                <td
                  colSpan="7"
                  className="px-4 py-10 text-center"
                >

                  <p className="text-sm text-slate-400">
                    No sentences found.
                  </p>

                  <p className="mt-1 text-xs text-slate-600">
                    Try a different search or filter.
                  </p>

                </td>

              </tr>

            )}

          </tbody>

        </table>

      </div>

    </section>
  );
}


function QualityBadge({ label }) {
  const styles = {
    Excellent:
      "bg-emerald-500/10 text-emerald-400 border-emerald-500/10",

    Good:
      "bg-blue-500/10 text-blue-400 border-blue-500/10",

    "Needs Review":
      "bg-orange-500/10 text-orange-400 border-orange-500/10",

    Poor:
      "bg-rose-500/10 text-rose-400 border-rose-500/10",
  };

  return (
    <span
      className={`
        inline-flex rounded-full
        border px-2.5 py-1
        text-[9px] font-semibold
        ${
          styles[label] ||
          "bg-slate-500/10 text-slate-400 border-slate-500/10"
        }
      `}
    >
      {label}
    </span>
  );
}

export default SentenceResultsTable;