import { useState } from "react";
import {
  Database,
  FileText,
  ChevronDown,
  Sparkles,
  Upload,
} from "lucide-react";

function EvaluationInput({ onEvaluate }) {
  const [mode, setMode] = useState("sentence");

  const [source, setSource] = useState("");
  const [translation, setTranslation] = useState("");
  const [reference, setReference] = useState("");

  const [domain, setDomain] = useState("General");

  const [error, setError] = useState("");

  const handleEvaluate = () => {
    setError("");

    if (!source.trim()) {
      setError("Please enter the source sentence.");
      return;
    }

    if (!translation.trim()) {
      setError("Please enter the machine translation.");
      return;
    }

    onEvaluate({
      mode,
      source,
      translation,
      reference,
      domain,
    });
  };

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl shadow-black/10">

      {/* Mode Selector */}
      <div className="mb-6 flex flex-wrap gap-3">

        <button
          onClick={() => {
            setMode("sentence");
            setError("");
          }}
          className={`
            flex items-center gap-2 rounded-xl border px-6 py-3
            text-sm font-semibold transition
            ${
              mode === "sentence"
                ? "border-violet-500 bg-violet-500/10 text-violet-300"
                : "border-white/10 bg-white/[0.02] text-slate-400 hover:bg-white/[0.05]"
            }
          `}
        >
          <FileText size={18} />
          Single Sentence
        </button>

        <button
          onClick={() => {
            setMode("dataset");
            setError("");
          }}
          className={`
            flex items-center gap-2 rounded-xl border px-6 py-3
            text-sm font-medium transition
            ${
              mode === "dataset"
                ? "border-violet-500 bg-violet-500/10 text-violet-300"
                : "border-white/10 bg-white/[0.02] text-slate-400 hover:bg-white/[0.05]"
            }
          `}
        >
          <Database size={18} />
          Dataset Upload
        </button>

      </div>


      {/* Dataset Mode */}
      {mode === "dataset" ? (
        <DatasetUpload onEvaluate={onEvaluate} />
      ) : (
        <>
          {/* Input Grid */}
          <div className="grid gap-5 xl:grid-cols-3">

            <TranslationField
              label="Source Sentence"
              language="English"
              placeholder="Enter the source sentence..."
              required
              value={source}
              onChange={setSource}
              languageColor="blue"
            />

            <TranslationField
              label="Machine Translation"
              language="Hindi"
              placeholder="Enter the machine translation..."
              required
              value={translation}
              onChange={setTranslation}
              languageColor="violet"
            />

            <TranslationField
              label="Reference"
              language="Hindi"
              placeholder="Enter the reference translation (optional)..."
              optional
              value={reference}
              onChange={setReference}
              languageColor="violet"
            />

          </div>


          {/* Bottom Controls */}
          <div className="mt-6 flex flex-col gap-5 border-t border-white/10 pt-6 lg:flex-row lg:items-end lg:justify-between">

            <div className="w-full lg:w-56">

              <label className="mb-2 block text-xs font-medium text-slate-400">
                Domain
              </label>

              <div className="relative">

                <select
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                  className="
                    w-full appearance-none rounded-xl
                    border border-white/10
                    bg-slate-900/80
                    px-4 py-3 pr-10
                    text-sm text-slate-300
                    outline-none
                    focus:border-violet-500/50
                  "
                >
                  <option>General</option>
                  <option>Medical</option>
                  <option>Legal</option>
                  <option>Technical</option>
                  <option>Finance</option>
                  <option>News</option>
                </select>

                <ChevronDown
                  size={16}
                  className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-500"
                />

              </div>

            </div>


            <button
              onClick={handleEvaluate}
              className="
                flex items-center justify-center gap-2
                rounded-xl
                bg-gradient-to-r from-violet-600 to-blue-600
                px-8 py-3.5
                text-sm font-semibold
                text-white
                shadow-xl shadow-violet-900/20
                transition
                hover:scale-[1.01]
                active:scale-[0.99]
              "
            >
              <Sparkles size={18} />

              Evaluate Translation

              <span className="text-lg leading-none">
                →
              </span>
            </button>

          </div>


          {/* Validation Error */}
          {error && (
            <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-xs text-red-400">
              {error}
            </div>
          )}
        </>
      )}

    </section>
  );
}


/* =========================================================
   Translation Field
========================================================= */

function TranslationField({
  label,
  language,
  placeholder,
  required,
  optional,
  languageColor,
  value,
  onChange,
}) {
  const badgeClass =
    languageColor === "blue"
      ? "bg-blue-500/10 text-blue-400"
      : "bg-violet-500/10 text-violet-400";

  return (
    <div>

      <div className="mb-2 flex items-center justify-between">

        <label className="text-sm font-semibold text-slate-200">

          {label}

          {required && (
            <span className="ml-1 text-red-400">*</span>
          )}

          {optional && (
            <span className="ml-2 text-xs font-normal text-slate-500">
              Optional
            </span>
          )}

        </label>

        <span
          className={`
            rounded-md px-2.5 py-1
            text-[11px] font-medium
            ${badgeClass}
          `}
        >
          {language}
        </span>

      </div>


      <div className="relative">

        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          maxLength={500}
          className="
            h-32 w-full resize-none
            rounded-xl border border-white/10
            bg-[#080d20]
            p-4
            text-sm leading-6 text-slate-200
            outline-none
            placeholder:text-slate-600
            transition
            focus:border-violet-500/60
            focus:ring-2 focus:ring-violet-500/10
          "
        />

        <span className="absolute bottom-2 right-3 text-[10px] text-slate-600">
          {value.length} / 500
        </span>

      </div>

    </div>
  );
}


/* =========================================================
   Dataset Upload
========================================================= */

function DatasetUpload({ onEvaluate }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    setError("");
    setFile(selectedFile);
  };

  const handleDatasetEvaluate = () => {
  setError("");

  if (!file) {
    setError("Please select a dataset file first.");
    return;
  }

  console.log("Dataset evaluation started:", file.name);

  onEvaluate({
    mode: "dataset",
    file: file,
    domain: "General",
  });
};

  return (
    <div>

      {/* Upload Area */}
      <div
        className="
          flex min-h-[230px]
          cursor-pointer flex-col
          items-center justify-center
          rounded-2xl
          border border-dashed border-violet-500/30
          bg-violet-500/[0.02]
          transition
          hover:border-violet-500/60
          hover:bg-violet-500/[0.04]
        "
        onClick={() =>
          document.getElementById("dataset-file").click()
        }
      >

        <input
          id="dataset-file"
          type="file"
          accept=".csv,.xlsx,.jsonl,.txt,.tmx"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />

        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-500/10">
          <Upload
            size={25}
            className="text-violet-400"
          />
        </div>

        {file ? (
          <>
            <p className="text-sm font-semibold text-white">
              {file.name}
            </p>

            <p className="mt-2 text-xs text-emerald-400">
              File selected successfully
            </p>

            <p className="mt-1 text-[10px] text-slate-600">
              Click to choose another file
            </p>
          </>
        ) : (
          <>
            <p className="text-sm font-semibold text-slate-200">
              Drop your dataset here
            </p>

            <p className="mt-2 text-xs text-slate-500">
              or click to browse files
            </p>

            <p className="mt-4 text-[10px] text-slate-600">
              Supported: CSV · XLSX · JSONL · TXT · TMX
            </p>
          </>
        )}

      </div>


      {/* Dataset Configuration + Button */}
      <div className="mt-6 flex flex-col gap-5 border-t border-white/10 pt-6 lg:flex-row lg:items-end lg:justify-between">

        <div>
          <p className="text-xs font-medium text-slate-400">
            Dataset
          </p>

          <p className="mt-1 text-sm text-slate-300">
            {file ? file.name : "No file selected"}
          </p>
        </div>


        <button
          onClick={handleDatasetEvaluate}
          className="
            flex items-center justify-center gap-2
            rounded-xl
            bg-gradient-to-r from-violet-600 to-blue-600
            px-8 py-3.5
            text-sm font-semibold
            text-white
            shadow-xl shadow-violet-900/20
            transition
            hover:scale-[1.01]
            active:scale-[0.99]
          "
        >
          <Sparkles size={18} />

          Start Dataset Evaluation

          <span className="text-lg leading-none">
            →
          </span>
        </button>

      </div>


      {/* Error */}
      {error && (
        <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-xs text-red-400">
          {error}
        </div>
      )}

    </div>
  );
}

export default EvaluationInput;