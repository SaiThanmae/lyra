import { notFound } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getPoem(id: string) {
  const res = await fetch(`${API}/poems/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

async function getAnalysis(id: string) {
  const res = await fetch(`${API}/analysis/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

async function getSimilar(id: string) {
  const res = await fetch(`${API}/discovery/similar/${id}?top_k=3`, { cache: "no-store" });
  if (!res.ok) return [];
  const data = await res.json();
  return data.results ?? [];
}

export default async function PoemPage({ params }: { params: { id: string } }) {
  const [poem, analysis] = await Promise.all([
    getPoem(params.id),
    getAnalysis(params.id),
  ]);

  if (!poem) notFound();

  return (
    <main className="max-w-3xl mx-auto px-4 py-12 space-y-10">

      {/* Header */}
      <header className="space-y-1">
        <h1 className="text-3xl font-bold text-stone-900">{poem.title}</h1>
        <p className="text-stone-500">
          {poem.poets?.name ?? "Unknown poet"}
          {poem.year ? ` · ${poem.year}` : ""}
          {poem.form ? ` · ${poem.form}` : ""}
        </p>
      </header>

      {/* Poem body */}
      <section className="border-l-4 border-violet-200 pl-6">
        <p className="whitespace-pre-line text-stone-800 leading-8 text-base font-serif">
          {poem.body}
        </p>
      </section>

      {/* Analysis */}
      {analysis && (
        <section className="rounded-2xl border border-stone-200 bg-stone-50 p-6 space-y-5">
          <h2 className="text-sm font-bold text-stone-500 uppercase tracking-widest">
            Literary Analysis
          </h2>

          {analysis.summary && (
            <p className="text-stone-600 italic text-sm leading-relaxed">{analysis.summary}</p>
          )}

          <div className="grid grid-cols-2 gap-4 text-sm">
            {analysis.meter && (
              <div>
                <p className="text-xs font-semibold text-stone-400 uppercase tracking-wider mb-0.5">Meter</p>
                <p className="text-stone-800">{analysis.meter}</p>
              </div>
            )}
            {analysis.rhyme_scheme && (
              <div>
                <p className="text-xs font-semibold text-stone-400 uppercase tracking-wider mb-0.5">Rhyme Scheme</p>
                <p className="text-stone-800">{analysis.rhyme_scheme}</p>
              </div>
            )}
          </div>

          {analysis.tone?.length > 0 && (
            <TagRow label="Tone" tags={analysis.tone} colour="amber" />
          )}
          {analysis.themes?.length > 0 && (
            <TagRow label="Themes" tags={analysis.themes} colour="teal" />
          )}
          {analysis.influences?.length > 0 && (
            <TagRow label="Influences" tags={analysis.influences} colour="violet" />
          )}

          {analysis.cultural_context && (
            <div>
              <p className="text-xs font-semibold text-stone-400 uppercase tracking-wider mb-1">
                Cultural Context
              </p>
              <p className="text-stone-700 text-sm leading-relaxed">{analysis.cultural_context}</p>
            </div>
          )}
        </section>
      )}
    </main>
  );
}

const COLOURS: Record<string, string> = {
  amber: "bg-amber-100 text-amber-800",
  teal: "bg-teal-100 text-teal-800",
  violet: "bg-violet-100 text-violet-800",
};

function TagRow({ label, tags, colour }: { label: string; tags: string[]; colour: string }) {
  return (
    <div>
      <p className="text-xs font-semibold text-stone-400 uppercase tracking-wider mb-1.5">{label}</p>
      <div className="flex flex-wrap gap-2">
        {tags.map((t: string) => (
          <span key={t} className={`rounded-full px-3 py-0.5 text-xs font-medium ${COLOURS[colour]}`}>
            {t}
          </span>
        ))}
      </div>
    </div>
  );
}
