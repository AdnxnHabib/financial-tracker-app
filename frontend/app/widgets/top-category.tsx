import { formatCurrency } from "../lib/format";
import type { DashboardData } from "../data/finance";

export function TopCategoryWidget({ data }: { data: DashboardData }) {
  const total = data.categorySpend.reduce((sum, item) => sum + item.amount, 0);
  const topCategory = [...data.categorySpend].sort(
    (a, b) => b.amount - a.amount,
  )[0];

  if (!topCategory || total === 0) {
    return (
      <section className="widget-card p-5">
        <p className="text-sm font-semibold text-[var(--ink-muted)]">
          Top category
        </p>
        <p className="mt-8 text-sm text-[var(--ink-muted)]">
          No categorized expenses this month.
        </p>
      </section>
    );
  }

  const gradient = data.categorySpend
    .reduce(
      (segments, item) => {
        const start = segments.offset;
        const size = (item.amount / total) * 100;
        const end = start + size;

        return {
          offset: end,
          values: [
            ...segments.values,
            `${item.color} ${start}% ${end}%`,
            `transparent ${end}% ${Math.min(end + 2, 100)}%`,
          ],
        };
      },
      { offset: 0, values: [] as string[] },
    )
    .values.join(", ");

  return (
    <section className="widget-card p-5">
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[var(--ink-muted)]">
            Top category
          </p>
          <h2 className="mt-1 text-2xl font-bold">{topCategory.category}</h2>
        </div>
        <p className="rounded-full bg-green-50 px-3 py-1 text-sm font-semibold text-[var(--green)]">
          {formatCurrency(topCategory.amount, topCategory.currency)}
        </p>
      </div>

      <div className="grid items-center gap-6 md:grid-cols-[14rem_1fr]">
        <div
          aria-label="Spending by category"
          className="mx-auto aspect-square w-full max-w-56 rounded-full"
          style={{
            background: `conic-gradient(${gradient})`,
            mask: "radial-gradient(circle, transparent 43%, black 45%)",
            WebkitMask: "radial-gradient(circle, transparent 43%, black 45%)",
          }}
        />

        <div className="space-y-3">
          {data.categorySpend.map((item) => (
            <div
              className="grid grid-cols-[0.75rem_minmax(0,1fr)_auto] items-center gap-3 text-sm"
              key={item.id}
            >
              <span
                className="h-5 rounded-full"
                style={{ backgroundColor: item.color }}
              />
              <span className="min-w-0 truncate font-medium">
                {item.category}
              </span>
              <span className="font-semibold">
                {formatCurrency(item.amount, item.currency)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
