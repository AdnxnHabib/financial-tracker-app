export type ExpenseCategory =
  | "Housing"
  | "Groceries"
  | "Transportation"
  | "Dining"
  | "Subscriptions"
  | "Utilities";

export type Expense = {
  id: string;
  merchant: string;
  amount: number;
  category: ExpenseCategory;
  date: string;
  account: string;
  paymentMethod: "Card" | "ACH" | "Cash";
};

export type MonthlyExpense = {
  month: string;
  amount: number;
  budget: number;
};

export type CategorySpend = {
  category: ExpenseCategory;
  amount: number;
  color: string;
};

export type DashboardData = {
  monthlyExpenses: MonthlyExpense[];
  categorySpend: CategorySpend[];
  recentExpenses: Expense[];
};

export const dashboardData: DashboardData = {
  monthlyExpenses: [
    { month: "Jan", amount: 3120, budget: 3900 },
    { month: "Feb", amount: 3510, budget: 3900 },
    { month: "Mar", amount: 2840, budget: 3900 },
    { month: "Apr", amount: 3760, budget: 3900 },
    { month: "May", amount: 3290, budget: 3900 },
    { month: "Jun", amount: 2415, budget: 3900 },
  ],
  categorySpend: [
    { category: "Housing", amount: 1425, color: "#4f5cf6" },
    { category: "Groceries", amount: 615, color: "#12a150" },
    { category: "Transportation", amount: 342, color: "#f3b51b" },
    { category: "Dining", amount: 286, color: "#ff7a3d" },
    { category: "Subscriptions", amount: 164, color: "#a855f7" },
    { category: "Utilities", amount: 238, color: "#2fd8d2" },
  ],
  recentExpenses: [
    {
      id: "exp-001",
      merchant: "Whole Foods",
      amount: 86.24,
      category: "Groceries",
      date: "2026-06-16",
      account: "Everyday Checking",
      paymentMethod: "Card",
    },
    {
      id: "exp-002",
      merchant: "Netflix",
      amount: 22.99,
      category: "Subscriptions",
      date: "2026-06-15",
      account: "Everyday Checking",
      paymentMethod: "Card",
    },
    {
      id: "exp-003",
      merchant: "Con Edison",
      amount: 118.37,
      category: "Utilities",
      date: "2026-06-14",
      account: "Household",
      paymentMethod: "ACH",
    },
    {
      id: "exp-004",
      merchant: "Blue Bottle Coffee",
      amount: 7.65,
      category: "Dining",
      date: "2026-06-13",
      account: "Everyday Checking",
      paymentMethod: "Card",
    },
    {
      id: "exp-005",
      merchant: "MTA",
      amount: 34,
      category: "Transportation",
      date: "2026-06-12",
      account: "Everyday Checking",
      paymentMethod: "Card",
    },
  ],
};
