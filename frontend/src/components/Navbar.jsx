import {
  Sparkles,
  Languages,
  ChevronDown,
} from "lucide-react";

function Navbar() {
  return (
    <header className="border-b border-white/10 bg-[#050816]/95">
      <div className="mx-auto flex h-[72px] max-w-[1500px] items-center justify-between px-6">

        {/* Logo */}
        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-blue-500 shadow-lg shadow-violet-900/30">
            <Sparkles size={20} />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-wide">
              RAG-MTE
            </h1>

            <p className="text-[10px] text-slate-500">
              Retrieval-Augmented Machine Translation Evaluation
            </p>
          </div>

        </div>


        {/* Navigation */}
        <nav className="hidden items-center gap-2 md:flex">

          <button className="rounded-lg bg-violet-600 px-6 py-2.5 text-sm font-semibold shadow-lg shadow-violet-900/20">
            Evaluate
          </button>

          <button className="rounded-lg px-5 py-2.5 text-sm text-slate-400 transition hover:bg-white/5 hover:text-white">
            How it works
          </button>

          <button className="rounded-lg px-5 py-2.5 text-sm text-slate-400 transition hover:bg-white/5 hover:text-white">
            About
          </button>

        </nav>


        {/* Language */}
        <button className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.02] px-4 py-2.5 text-sm text-slate-300 transition hover:border-violet-500/40">

          <Languages size={16} />

          <span>English → Hindi</span>

          <ChevronDown size={15} className="text-slate-500" />

        </button>

      </div>
    </header>
  );
}

export default Navbar;