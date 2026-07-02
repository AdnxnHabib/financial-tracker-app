export type Expense = {
  id: string;
  merchant: string;
  amount: number;
  currency: string;
  category: string;
  date: string;
  account: string;
  paymentMethod: string;
};

export type MonthlyExpense = {
  month: string;
  amount: number;
  budget: number | null;
  currency: string;
};

export type CategorySpend = {
  id: string;
  category: string;
  amount: number;
  currency: string;
  percentOfTotal: number;
  color: string;
};

export type DashboardData = {
  monthlyExpenses: MonthlyExpense[];
  categorySpend: CategorySpend[];
  recentExpenses: Expense[];
};
