import { MonthlyExpensesWidget } from "./monthly-expenses";
import { RecentExpensesWidget } from "./recent-expenses";
import { TopCategoryWidget } from "./top-category";
import type { DashboardWidget } from "./types";

export const dashboardWidgets: DashboardWidget[] = [
  {
    id: "monthly-expenses",
    title: "Monthly expenses",
    size: "wide",
    Component: MonthlyExpensesWidget,
  },
  {
    id: "top-category",
    title: "Top category",
    size: "standard",
    Component: TopCategoryWidget,
  },
  {
    id: "recent-expenses",
    title: "Recent expenses",
    size: "wide",
    Component: RecentExpensesWidget,
  },
];
