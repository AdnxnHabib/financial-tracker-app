import { API_URL } from "./api";

export type AccountOption = {
  id: string;
  name: string;
};

export type CategoryOption = {
  id: string;
  name: string;
  color: string;
};

type AccountResponse = {
  id: string;
  name: string;
  is_archived: boolean;
};

type CategoryResponse = {
  id: string;
  name: string;
  color: string;
  is_archived: boolean;
};

export type TransactionFormOptions = {
  accounts: AccountOption[];
  categories: CategoryOption[];
};

export async function getTransactionFormOptions(): Promise<TransactionFormOptions> {
  const [accountsResponse, categoriesResponse] = await Promise.all([
    fetch(`${API_URL}/accounts`, { cache: "no-store" }),
    fetch(`${API_URL}/categories`, { cache: "no-store" }),
  ]);

  if (!accountsResponse.ok || !categoriesResponse.ok) {
    throw new Error("Transaction form options request failed.");
  }

  const accounts = (await accountsResponse.json()) as AccountResponse[];
  const categories = (await categoriesResponse.json()) as CategoryResponse[];

  return {
    accounts: accounts
      .filter((account) => !account.is_archived)
      .map((account) => ({
        id: account.id,
        name: account.name,
      })),
    categories: categories
      .filter((category) => !category.is_archived)
      .map((category) => ({
        id: category.id,
        name: category.name,
        color: category.color,
      })),
  };
}
