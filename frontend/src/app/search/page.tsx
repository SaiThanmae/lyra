const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function search(q: string) {
  const res = await fetch(`${API}/discovery/search?q=${encodeURIComponent(q)}&top_k=6`, { cache: "no-store" });
  if (!res.ok) return [];
  const data = await res.json();
  return data.results ?? [];
}

export default async function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const q = searchParams.q ?? "";
  const results = q ? await search(q) : [];

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-2xl font-bold text-stone-900 mb-2">
        Search results for <span className="text-violet-700">"{q}"</span>
      </h1>
      <p className="text-stone-500 text-sm mb-8">Semantic search across the Lyra corpus</p>

      {results.length === 0 ? (
        <p className="text-stone-400 py-20 text-center">No results found. Try "memory", "exile", or "rivers".</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {results.map((poem: any) => (
            <a key={poem.id} href={`/poems/${poem.id}`} className="group block">
              <div className="rounded-2xl border border-stone-200 bg-white hover:border-violet-300 hover:shadow-sm transition-all p-5 flex flex-col gap-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h2 className="font-semibold text-stone-900 group-hover:text-violet-700 transition-colors">
                      {poem.title}
                    </h2>
                    <p className="text-xs text-stone-500 mt-0.5">
                      {poem.poets?.name ?? "Unknown"}
                      {poem.year ? ` · ${poem.year}` : ""}
                    </p>
                  </div>
                  {poem.form && (
                    <span className="shrink-0 rounded-full bg-stone-100 px-2.5 py-0.5 text-xs text-stone-600 capitalize">
                      {poem.form}
                    </span>
                  )}
                </div>
                <p className="text-xs text-teal-700 font-medium">
                  {Math.round((poem.similarity_score ?? 0) * 100)}% match
                </p>
              </div>
            </a>
          ))}
        </div>
      )}
    </main>
  );
}
