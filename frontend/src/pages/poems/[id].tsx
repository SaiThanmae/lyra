import { getPoem, getAnalysis, findSimilar, getLineage } from "@/lib/api";
import AnalysisCard from "@/components/analysis/AnalysisCard";
import PoemCard from "@/components/poems/PoemCard";

interface Props {
  params: { id: string };
}

export default async function PoemPage({ params }: Props) {
  const [poem, analysis, similar, lineage] = await Promise.allSettled([
    getPoem(params.id),
    getAnalysis(params.id),
    findSimilar(params.id, 4),
    getLineage(params.id),
  ]);

  const poemData = poem.status === "fulfilled" ? poem.value : null;
  const analysisData = analysis.status === "fulfilled" ? analysis.value : null;
  const similarData = similar.status === "fulfilled" ? similar.value.results : [];

  if (!poemData) {
    return (
      <main className="max-w-2xl mx-auto px-4 py-16 text-stone-500">
        Poem not found.
      </main>
    );
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-12 space-y-10">
      {/* Poem header */}
      <header className="space-y-1">
        <h1 className="text-3xl font-bold text-stone-900">{poemData.title}</h1>
        {poemData.poets && (
          <p className="text-stone-500">
            {poemData.poets.name}
            {poemData.year ? ` · ${poemData.year}` : ""}
            {poemData.form ? ` · ${poemData.form}` : ""}
          </p>
        )}
      </header>

      {/* Poem body */}
      <section className="border-l-2 border-stone-200 pl-6">
        <p className="whitespace-pre-line text-stone-800 leading-8 text-base font-serif">
          {poemData.body}
        </p>
      </section>

      {/* AI Analysis */}
      {analysisData && <AnalysisCard analysis={analysisData} />}

      {/* Similar Poems */}
      {similarData.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold text-stone-800 mb-4">
            You might also read
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {similarData.map((p) => (
              <PoemCard key={p.id} poem={p} similarityScore={p.similarity_score} />
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
