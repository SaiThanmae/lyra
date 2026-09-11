import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getPoems() {
  const res = await fetch(`${API}/poems/?limit=20`, { cache: "no-store" });
  if (!res.ok) return [];
  const data = await res.json();
  return data.poems ?? [];
}

export default async function HomePage() {
  const poems = await getPoems();

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      {/* Hero */}
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-stone-900 mb-3">
          A Living Archive of World Poetry
        </h1>
        <p className="text-stone-500 text-lg max-w-xl mx-auto">
          Lyra preserves, analyses, and connects poetic works across cultures,
          traditions, and centuries — powered by AI that respects artistic authenticity.
        </p>
      </div>

      {/* Search bar */}
      <form action="/search" className="mb-10 flex gap-2">
        <input
          name="q"
          type="text"
          placeholder='Search poems — try "exile" or "urban solitude"'
          className="flex-1 rounded-xl border border-stone-300 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-400"
        />
        <button
          type="submit"
          className="rounded-xl bg-violet-700 text-white px-5 py-2.5 text-sm font-semibold hover:bg-violet-800"
        >
          Search
        </button>
      </form>

      {/* Poem grid */}
      {poems.length === 0 ? (
        <p className="text-stone-400 text-center py-20">No poems yet.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {poems.map((poem: any) => (
            <Link key={poem.id} href={`/poems/${poem.id}`} className="group block">
              <div className="rounded-2xl border border-stone-200 bg-white hover:border-violet-300 hover:shadow-sm transition-all p-5 h-full flex flex-col gap-3">
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
                {poem.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-auto">
                    {poem.tags.slice(0, 3).map((t: string) => (
                      <span key={t} className="rounded-full bg-violet-50 text-violet-700 text-xs px-2 py-0.5">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
