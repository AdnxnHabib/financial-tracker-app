import { formatCurrency, formatDate } from "../lib/format";
import type { DashboardData } from "../data/finance";

export function RecentExpensesWidget({ data }: { data: DashboardData }) {
  return (
    <section className="widget-card overflow-hidden p-5">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[var(--ink-muted)]">
            Recent expenses
          </p>
          <h2 className="mt-1 text-2xl font-bold">Latest activity</h2>
        </div>
        <button className="rounded-md border border-[var(--line)] px-3 py-2 text-sm font-semibold hover:bg-[var(--surface-muted)]">
          Filter
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[42rem] border-collapse text-left text-sm">
          <thead>
            <tr className="border-b border-[var(--line)] text-[var(--ink-muted)]">
              <th className="pb-3 pr-4 font-semibold">Merchant</th>
              <th className="pb-3 pr-4 font-semibold">Category</th>
              <th className="pb-3 pr-4 font-semibold">Account</th>
              <th className="pb-3 pr-4 font-semibold">Date</th>
              <th className="pb-3 pr-4 font-semibold">Method</th>
              <th className="pb-3 text-right font-semibold">Amount</th>
            </tr>
          </thead>
          <tbody>
            {data.recentExpenses.map((expense) => (
              <tr
                className="border-b border-[var(--line)] last:border-b-0"
                key={expense.id}
              >
                <td className="py-3 pr-4 font-semibold">{expense.merchant}</td>
                <td className="py-3 pr-4">{expense.category}</td>
                <td className="py-3 pr-4 text-[var(--ink-muted)]">
                  {expense.account}
                </td>
                <td className="py-3 pr-4 text-[var(--ink-muted)]">
                  {formatDate(expense.date)}
                </td>
                <td className="py-3 pr-4">{expense.paymentMethod}</td>
                <td className="py-3 text-right font-bold">
                  {formatCurrency(expense.amount)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
