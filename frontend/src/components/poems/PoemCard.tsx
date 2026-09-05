import type { Poem } from "@/lib/api";
import Link from "next/link";

interface Props {
  poem: Poem;
  similarityScore?: number;
}

export default function PoemCard({ poem, similarityScore }: Props) {
  // Show first 4 lines as preview
  const preview = poem.body.split("\n").slice(0, 4).join("\n");
  const truncated = poem.body.split("\n").length > 4;

  return (
    <Link href={`/poems/${poem.id}`} className="group block">
      <div className="rounded-2xl border border-stone-200 bg-white hover:border-stone-400 transition-colors p-5 h-full flex flex-col gap-3">
        {/* Header */}
        <div className="flex items-start justify-between gap-2">
          <div>
            <h3 className="font-semibold text-stone-900 group-hover:text-violet-700 transition-colors">
              {poem.title}
            </h3>
            {poem.poets && (
              <p className="text-xs text-stone-500 mt-0.5">
                {poem.poets.name}
                {poem.year ? ` · ${poem.year}` : ""}
              </p>
            )}
          </div>
          {poem.form && (
            <span className="shrink-0 rounded-full bg-stone-100 px-2.5 py-0.5 text-xs text-stone-600 capitalize">
              {poem.form}
            </span>
          )}
        </div>

        {/* Poem preview */}
        <p className="text-sm text-stone-600 whitespace-pre-line leading-relaxed flex-1">
          {preview}
          {truncated && <span className="text-stone-400"> …</span>}
        </p>

        {/* Tags */}
        {poem.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {poem.tags.slice(0, 3).map((t) => (
              <span
                key={t}
                className="rounded-full bg-violet-50 text-violet-700 text-xs px-2 py-0.5"
              >
                {t}
              </span>
            ))}
          </div>
        )}

        {/* Similarity badge (discovery results) */}
        {similarityScore !== undefined && (
          <div className="text-xs text-teal-700 font-medium">
            {Math.round(similarityScore * 100)}% similar
          </div>
        )}
      </div>
    </Link>
  );
}
