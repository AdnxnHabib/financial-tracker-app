"use server";

import { revalidatePath } from "next/cache";

import { API_URL } from "../lib/api";

export type AddAccountState = {
  success: boolean;
  error: string | null;
};

export async function addAccountAction(
  _previousState: AddAccountState,
  formData: FormData,
): Promise<AddAccountState> {
  const name = String(formData.get("name") ?? "").trim();
  const institutionName = String(formData.get("institution_name") ?? "").trim();
  const openingBalance = Number(formData.get("opening_balance") ?? 0);

  if (!name) {
    return { success: false, error: "Enter an account name." };
  }

  if (!Number.isFinite(openingBalance)) {
    return { success: false, error: "Enter a valid opening balance." };
  }

  const payload = {
    name,
    account_type: String(formData.get("account_type") ?? "checking"),
    currency: "USD",
    institution_name: institutionName || null,
    opening_balance_cents: Math.round(openingBalance * 100),
  };

  const response = await fetch(`${API_URL}/accounts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    return {
      success: false,
      error: "Account could not be added. Check the form and try again.",
    };
  }

  revalidatePath("/");
  return { success: true, error: null };
}
