import { dashboardData } from "./data/finance";
import { dashboardWidgets } from "./widgets/registry";

const navigationGroups = [
  {
    label: "General",
    items: ["Dashboard", "All expenses", "Budgets", "Accounts"],
  },
  {
    label: "Tools",
    items: ["Insights", "Reports", "Imports"],
  },
  {
    label: "Other",
    items: ["Settings", "Help"],
  },
];

export default function Home() {
  return (
    <main className="min-h-screen p-4 text-[var(--ink)] md:p-6">
      <div className="mx-auto grid max-w-[90rem] overflow-hidden rounded-[28px] border border-white/70 bg-[var(--surface-muted)] shadow-2xl shadow-slate-300/60 lg:grid-cols-[17rem_1fr]">
        <aside className="border-b border-[var(--line)] bg-white/70 p-5 lg:min-h-[calc(100vh-3rem)] lg:border-b-0 lg:border-r">
          <div className="mb-10 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[var(--blue)] text-lg font-black text-white">
              F
            </div>
            <div>
              <p className="text-lg font-black tracking-normal">FinTrack</p>
              <p className="text-xs font-semibold text-[var(--ink-muted)]">
                Personal finance
              </p>
            </div>
          </div>

          <nav className="space-y-7">
            {navigationGroups.map((group) => (
              <div key={group.label}>
                <p className="mb-2 text-xs font-bold uppercase text-[var(--ink-muted)]">
                  {group.label}
                </p>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <button
                      className={`flex min-h-10 w-full items-center rounded-md px-3 text-left text-sm font-semibold ${
                        item === "Dashboard"
                          ? "bg-[#eceefd] text-[var(--blue)]"
                          : "text-[var(--ink-muted)] hover:bg-white"
                      }`}
                      key={item}
                    >
                      {item}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </nav>
        </aside>

        <section className="min-w-0 p-5 md:p-8">
          <header className="mb-8 flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <h1 className="text-3xl font-bold">Dashboard</h1>
              <p className="mt-1 text-[var(--ink-muted)]">
                Track monthly spend, category pressure, and recent activity.
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <label className="relative block">
                <span className="sr-only">Search expenses</span>
                <input
                  className="h-11 w-full rounded-md border border-[var(--line)] bg-white px-4 pr-10 outline-none transition focus:border-[var(--blue)] sm:w-80"
                  placeholder="Search expenses"
                  type="search"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--ink-muted)]">
                  /
                </span>
              </label>
              <button className="h-11 rounded-md bg-[var(--blue)] px-4 font-bold text-white shadow-lg shadow-indigo-200">
                Add expense
              </button>
            </div>
          </header>

          <div className="mb-4 grid gap-4 md:grid-cols-3">
            <SummaryMetric label="This month" value="$2,415" trend="38% under budget" />
            <SummaryMetric label="Top category" value="Housing" trend="$1,425 spent" />
            <SummaryMetric label="Transactions" value="128" trend="5 added this week" />
          </div>

          <div className="dashboard-grid">
            {dashboardWidgets.map((widget) => {
              const WidgetComponent = widget.Component;

              return (
                <div
                  className={widget.size === "wide" ? "min-w-0" : "min-w-0"}
                  key={widget.id}
                >
                  <WidgetComponent data={dashboardData} />
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </main>
  );
}

function SummaryMetric({
  label,
  value,
  trend,
}: {
  label: string;
  value: string;
  trend: string;
}) {
  return (
    <section className="widget-card p-4">
      <p className="text-sm font-semibold text-[var(--ink-muted)]">{label}</p>
      <p className="mt-2 text-2xl font-bold">{value}</p>
      <p className="mt-3 text-sm font-semibold text-[var(--green)]">{trend}</p>
    </section>
  );
}
