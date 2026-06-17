import type { DashboardData } from "../data/finance";

export type WidgetSize = "wide" | "standard";

export type DashboardWidget = {
  id: string;
  title: string;
  size: WidgetSize;
  Component: (props: { data: DashboardData }) => React.ReactNode;
};
