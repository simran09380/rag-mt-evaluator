import {
  Target,
  BookOpen,
  Tag,
  FileCheck,
} from "lucide-react";

function DimensionScores({ scores }) {
  const dimensions = [
    {
      name: "Accuracy",
      value: scores.accuracy,
      icon: Target,
      color: "blue",
    },
    {
      name: "Fluency",
      value: scores.fluency,
      icon: FileCheck,
      color: "emerald",
    },
    {
      name: "Terminology",
      value: scores.terminology,
      icon: BookOpen,
      color: "violet",
    },
    {
      name: "Named Entities",
      value: scores.named_entities,
      icon: Tag,
      color: "orange",
    },
  ];

  return (
    <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">

      <div className="mb-5 flex items-center gap-3">
        <div className="h-5 w-1 rounded-full bg-violet-500" />

        <h2 className="text-base font-semibold">
          Dimension Scores
        </h2>
      </div>


      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">

        {dimensions.map((dimension) => {
          const Icon = dimension.icon;

          return (
            <ScoreCard
              key={dimension.name}
              name={dimension.name}
              value={dimension.value}
              Icon={Icon}
              color={dimension.color}
            />
          );
        })}

      </div>

    </section>
  );
}


function ScoreCard({
  name,
  value,
  Icon,
  color,
}) {
  const styles = {
    blue: {
      icon: "bg-blue-500/10 text-blue-400",
      bar: "bg-blue-500",
    },

    emerald: {
      icon: "bg-emerald-500/10 text-emerald-400",
      bar: "bg-emerald-500",
    },

    violet: {
      icon: "bg-violet-500/10 text-violet-400",
      bar: "bg-violet-500",
    },

    orange: {
      icon: "bg-orange-500/10 text-orange-400",
      bar: "bg-orange-500",
    },
  };

  const style = styles[color];

  return (
    <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">

      <div className="flex items-center gap-3">

        <div
          className={`flex h-9 w-9 items-center justify-center rounded-lg ${style.icon}`}
        >
          <Icon size={18} />
        </div>

        <div>
          <p className="text-xs text-slate-500">
            {name}
          </p>

          <p className="text-lg font-bold">
            {value}
            <span className="ml-1 text-xs font-normal text-slate-500">
              / 100
            </span>
          </p>
        </div>

      </div>


      <div className="mt-3 h-1.5 rounded-full bg-slate-800">

        <div
          className={`h-full rounded-full ${style.bar}`}
          style={{
            width: `${value}%`,
          }}
        />

      </div>

    </div>
  );
}

export default DimensionScores;