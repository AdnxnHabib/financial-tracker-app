import type { DashboardData } from "../data/finance";
import { API_URL } from "./api";

export type DashboardResponse = {
  monthly_expenses: Array<{
    month: string;
    spent_cents: number;
    budget_cents: number | null;
    currency: string;
  }>;
  top_categories: Array<{
    category_id: string;
    category_name: string;
    color: string;
    spent_cents: number;
    percent_of_total: number;
    currency: string;
  }>;
  recent_expenses: Array<{
    id: string;
    merchant_name: string | null;
    category_name: string;
    account_name: string;
    amount_cents: number;
    currency: string;
    transaction_date: string;
    payment_method: string;
  }>;
};

export async function getDashboardData(): Promise<DashboardData> {
  const response = await fetch(`${API_URL}/dashboard/summary`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Dashboard request failed with status ${response.status}`);
  }

  const data = (await response.json()) as DashboardResponse;

  return {
    monthlyExpenses: data.monthly_expenses.map((expense) => ({
      month: formatMonth(expense.month),
      amount: centsToDollars(expense.spent_cents),
      budget:
        expense.budget_cents === null
          ? null
          : centsToDollars(expense.budget_cents),
      currency: expense.currency,
    })),
    categorySpend: data.top_categories.map((category) => ({
      id: category.category_id,
      category: category.category_name,
      amount: centsToDollars(category.spent_cents),
      currency: category.currency,
      percentOfTotal: category.percent_of_total,
      color: category.color,
    })),
    recentExpenses: data.recent_expenses.map((expense) => ({
      id: expense.id,
      merchant: expense.merchant_name ?? "Unnamed expense",
      amount: centsToDollars(expense.amount_cents),
      currency: expense.currency,
      category: expense.category_name,
      date: expense.transaction_date,
      account: expense.account_name,
      paymentMethod: formatPaymentMethod(expense.payment_method),
    })),
  };
}

function centsToDollars(cents: number): number {
  return cents / 100;
}

function formatMonth(value: string): string {
  const [year, month] = value.split("-").map(Number);

  return new Intl.DateTimeFormat("en-US", { month: "short" }).format(
    new Date(Date.UTC(year, month - 1, 1)),
  );
}

function formatPaymentMethod(value: string): string {
  if (value.toLowerCase() === "ach") {
    return "ACH";
  }

  return value.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}
