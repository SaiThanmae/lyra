import type { PoemAnalysis } from "@/lib/api";

interface Props {
  analysis: PoemAnalysis;
}

export default function AnalysisCard({ analysis }: Props) {
  return (
    <div className="rounded-2xl border border-stone-200 bg-stone-50 p-6 space-y-5 text-sm leading-relaxed">
      <h2 className="text-base font-semibold text-stone-800 tracking-wide uppercase">
        Literary Analysis
      </h2>

      {analysis.summary && (
        <p className="text-stone-600 italic">{analysis.summary}</p>
      )}

      <div className="grid grid-cols-2 gap-4">
        {analysis.meter && (
          <Field label="Meter" value={analysis.meter} />
        )}
        {analysis.rhyme_scheme && (
          <Field label="Rhyme Scheme" value={analysis.rhyme_scheme} />
        )}
      </div>

      {analysis.tone.length > 0 && (
        <TagRow label="Tone" tags={analysis.tone} colour="amber" />
      )}
      {analysis.themes.length > 0 && (
        <TagRow label="Themes" tags={analysis.themes} colour="teal" />
      )}
      {analysis.influences.length > 0 && (
        <TagRow label="Influences" tags={analysis.influences} colour="violet" />
      )}

      {analysis.cultural_context && (
        <div>
          <p className="text-xs font-semibold text-stone-500 uppercase tracking-widest mb-1">
            Cultural Context
          </p>
          <p className="text-stone-700">{analysis.cultural_context}</p>
        </div>
      )}
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-semibold text-stone-500 uppercase tracking-widest mb-0.5">
        {label}
      </p>
      <p className="text-stone-800">{value}</p>
    </div>
  );
}

const COLOUR_MAP: Record<string, string> = {
  amber: "bg-amber-100 text-amber-800",
  teal: "bg-teal-100 text-teal-800",
  violet: "bg-violet-100 text-violet-800",
};

function TagRow({
  label,
  tags,
  colour,
}: {
  label: string;
  tags: string[];
  colour: string;
}) {
  return (
    <div>
      <p className="text-xs font-semibold text-stone-500 uppercase tracking-widest mb-1.5">
        {label}
      </p>
      <div className="flex flex-wrap gap-2">
        {tags.map((t) => (
          <span
            key={t}
            className={`rounded-full px-3 py-0.5 text-xs font-medium ${COLOUR_MAP[colour] ?? ""}`}
          >
            {t}
          </span>
        ))}
      </div>
    </div>
  );
}
