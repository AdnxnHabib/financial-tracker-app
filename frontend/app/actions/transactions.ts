"use server";

import { revalidatePath } from "next/cache";

import { API_URL } from "../lib/api";

export type AddTransactionState = {
  success: boolean;
  error: string | null;
};

export async function addTransactionAction(
  _previousState: AddTransactionState,
  formData: FormData,
): Promise<AddTransactionState> {
  const transactionType = String(formData.get("transaction_type") ?? "expense");
  const amount = Number(formData.get("amount") ?? 0);
  const categoryId = String(formData.get("category_id") ?? "");
  const merchantName = String(formData.get("merchant_name") ?? "").trim();
  const description = String(formData.get("description") ?? "").trim();

  if (!Number.isFinite(amount) || amount <= 0) {
    return { success: false, error: "Enter an amount greater than zero." };
  }

  if (transactionType === "expense" && !categoryId) {
    return { success: false, error: "Choose a category for this expense." };
  }

  const payload = {
    account_id: String(formData.get("account_id") ?? ""),
    category_id: categoryId || null,
    transaction_type: transactionType,
    amount_cents: Math.round(amount * 100),
    currency: "USD",
    transaction_date: String(formData.get("transaction_date") ?? ""),
    merchant_name: merchantName || null,
    description: description || null,
    payment_method: String(formData.get("payment_method") ?? "other"),
    status: String(formData.get("status") ?? "cleared"),
  };

  const response = await fetch(`${API_URL}/transactions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    return {
      success: false,
      error: "Transaction could not be added. Check the form and try again.",
    };
  }

  revalidatePath("/");
  return { success: true, error: null };
}
