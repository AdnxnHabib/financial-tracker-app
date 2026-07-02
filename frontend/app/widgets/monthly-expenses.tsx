import { formatCurrency } from "../lib/format";
import type { DashboardData } from "../data/finance";

export function MonthlyExpensesWidget({ data }: { data: DashboardData }) {
  const currentMonth = data.monthlyExpenses[data.monthlyExpenses.length - 1];
  const previousMonth = data.monthlyExpenses[data.monthlyExpenses.length - 2];
  const delta =
    currentMonth && previousMonth && previousMonth.amount > 0
      ? ((currentMonth.amount - previousMonth.amount) / previousMonth.amount) *
        100
      : null;
  const maxValue = Math.max(
    1,
    ...data.monthlyExpenses.flatMap((item) => [
      item.amount,
      item.budget ?? 0,
    ]),
  );

  if (!currentMonth) {
    return (
      <section className="widget-card p-5">
        <p className="text-sm font-semibold text-[var(--ink-muted)]">
          Monthly expenses
        </p>
        <p className="mt-8 text-sm text-[var(--ink-muted)]">
          No monthly spending data yet.
        </p>
      </section>
    );
  }

  return (
    <section className="widget-card p-5">
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[var(--ink-muted)]">
            Monthly expenses
          </p>
          <h2 className="mt-1 text-3xl font-bold">
            {formatCurrency(currentMonth.amount, currentMonth.currency)}
          </h2>
        </div>
        {delta === null ? (
          <p className="rounded-full bg-[var(--surface-muted)] px-3 py-1 text-sm font-semibold text-[var(--ink-muted)]">
            No prior spending
          </p>
        ) : (
          <p
            className={`rounded-full px-3 py-1 text-sm font-semibold ${
            delta <= 0
              ? "bg-green-50 text-[var(--green)]"
              : "bg-red-50 text-[var(--red)]"
          }`}
          >
            {Math.abs(delta).toFixed(1)}% {delta <= 0 ? "under" : "over"} last
            month
          </p>
        )}
      </div>

      <div className="flex h-64 items-end gap-4">
        {data.monthlyExpenses.map((item) => {
          const budgetHeight =
            item.budget === null ? null : `${(item.budget / maxValue) * 100}%`;
          const amountHeight = `${(item.amount / maxValue) * 100}%`;

          return (
            <div
              className="flex h-full min-w-0 flex-1 flex-col items-center justify-end gap-3"
              key={item.month}
            >
              <div
                aria-label={`${item.month}: ${formatCurrency(item.amount, item.currency)}`}
                className="relative h-full w-full max-w-14 overflow-hidden rounded-t-2xl bg-[#e7e8fb]"
              >
                <div
                  className="absolute bottom-0 left-0 right-0 rounded-t-2xl bg-[var(--blue)]"
                  style={{ height: amountHeight }}
                />
                {budgetHeight !== null && (
                  <div
                    className="pointer-events-none absolute bottom-0 left-0 right-0 border-t border-dashed border-white/80"
                    style={{ height: budgetHeight }}
                  />
                )}
              </div>
              <span className="text-sm text-[var(--ink-muted)]">
                {item.month}
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
