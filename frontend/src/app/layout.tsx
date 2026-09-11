import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lyra — Poetry Preservation",
  description: "AI-driven ecosystem for culturally sustainable poetry preservation and analysis",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white text-stone-900 antialiased">
        <nav className="border-b border-stone-200 px-6 py-4 flex items-center justify-between">
          <a href="/" className="text-xl font-bold tracking-tight text-stone-900">
            🎭 Lyra
          </a>
          <a href="/poems/submit" className="text-sm text-violet-700 hover:underline font-medium">
            Submit a Poem
          </a>
        </nav>
        {children}
      </body>
    </html>
  );
}
