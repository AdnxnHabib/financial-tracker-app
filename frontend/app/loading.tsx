export default function Loading() {
  return (
    <main className="min-h-screen p-4 text-[var(--ink)] md:p-6">
      <div className="mx-auto min-h-[calc(100vh-3rem)] max-w-[90rem] animate-pulse rounded-lg border border-[var(--line)] bg-[var(--surface-muted)] p-6 md:p-8">
        <div className="h-9 w-48 rounded bg-slate-200" />
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {[0, 1, 2].map((item) => (
            <div className="h-32 rounded-lg bg-white" key={item} />
          ))}
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <div className="h-96 rounded-lg bg-white" />
          <div className="h-96 rounded-lg bg-white" />
        </div>
      </div>
    </main>
  );
}
