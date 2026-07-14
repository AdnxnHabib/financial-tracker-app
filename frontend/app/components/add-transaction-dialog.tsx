"use client";

import { useActionState, useMemo, useState } from "react";

import {
  addTransactionAction,
  type AddTransactionState,
} from "../actions/transactions";
import type {
  AccountOption,
  CategoryOption,
} from "../lib/transaction-options";

type AddTransactionDialogProps = {
  accounts: AccountOption[];
  categories: CategoryOption[];
  disabled?: boolean;
};

const initialState: AddTransactionState = {
  success: false,
  error: null,
};

export function AddTransactionDialog({
  accounts,
  categories,
  disabled = false,
}: AddTransactionDialogProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [transactionType, setTransactionType] = useState("expense");
  const [state, formAction, isPending] = useActionState(
    addTransactionAction,
    initialState,
  );
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const isFormUnavailable = disabled || accounts.length === 0;

  return (
    <>
      <button
        className="h-11 rounded-md bg-[var(--blue)] px-4 font-bold text-white shadow-lg shadow-indigo-200 disabled:cursor-not-allowed disabled:opacity-50"
        disabled={isFormUnavailable}
        onClick={() => setIsOpen(true)}
        type="button"
      >
        Add transaction
      </button>

      {isOpen ? (
        <div
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4"
          role="dialog"
        >
          <div className="max-h-[calc(100vh-2rem)] w-full max-w-2xl overflow-y-auto rounded-lg border border-[var(--line)] bg-white shadow-2xl">
            <div className="flex items-start justify-between border-b border-[var(--line)] p-5">
              <div>
                <h2 className="text-xl font-bold">Add transaction</h2>
                <p className="mt-1 text-sm text-[var(--ink-muted)]">
                  Record a new expense, income item, or transfer.
                </p>
              </div>
              <button
                aria-label="Close"
                className="flex h-9 w-9 items-center justify-center rounded-md text-xl font-bold text-[var(--ink-muted)] hover:bg-[var(--surface-muted)]"
                onClick={() => setIsOpen(false)}
                type="button"
              >
                ×
              </button>
            </div>

            <form action={formAction} className="grid gap-4 p-5">
              {state.success ? (
                <p className="rounded-md border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm font-semibold text-[var(--green)]">
                  Transaction saved.
                </p>
              ) : null}

              {state.error ? (
                <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm font-semibold text-[var(--red)]">
                  {state.error}
                </p>
              ) : null}

              <div className="grid gap-4 md:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Type
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="transaction_type"
                    onChange={(event) => setTransactionType(event.target.value)}
                    value={transactionType}
                  >
                    <option value="expense">Expense</option>
                    <option value="income">Income</option>
                    <option value="transfer">Transfer</option>
                  </select>
                </label>

                <label className="grid gap-2 text-sm font-semibold">
                  Amount
                  <input
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    min="0.01"
                    name="amount"
                    placeholder="0.00"
                    required
                    step="0.01"
                    type="number"
                  />
                </label>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Account
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="account_id"
                    required
                  >
                    {accounts.map((account) => (
                      <option key={account.id} value={account.id}>
                        {account.name}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="grid gap-2 text-sm font-semibold">
                  Category
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="category_id"
                    required={transactionType === "expense"}
                  >
                    <option value="">
                      {transactionType === "expense" ? "Choose category" : "None"}
                    </option>
                    {categories.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Merchant
                  <input
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    maxLength={160}
                    name="merchant_name"
                    placeholder="Coffee shop"
                    type="text"
                  />
                </label>

                <label className="grid gap-2 text-sm font-semibold">
                  Date
                  <input
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    defaultValue={today}
                    name="transaction_date"
                    required
                    type="date"
                  />
                </label>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Payment method
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="payment_method"
                    defaultValue="card"
                  >
                    <option value="card">Card</option>
                    <option value="cash">Cash</option>
                    <option value="ach">ACH</option>
                    <option value="wire">Wire</option>
                    <option value="check">Check</option>
                    <option value="other">Other</option>
                  </select>
                </label>

                <label className="grid gap-2 text-sm font-semibold">
                  Status
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="status"
                    defaultValue="cleared"
                  >
                    <option value="cleared">Cleared</option>
                    <option value="pending">Pending</option>
                    <option value="excluded">Excluded</option>
                  </select>
                </label>
              </div>

              <label className="grid gap-2 text-sm font-semibold">
                Description
                <textarea
                  className="min-h-24 rounded-md border border-[var(--line)] bg-white px-3 py-2 outline-none focus:border-[var(--blue)]"
                  maxLength={240}
                  name="description"
                  placeholder="Optional note"
                />
              </label>

              <div className="flex flex-col-reverse gap-3 border-t border-[var(--line)] pt-4 sm:flex-row sm:justify-end">
                <button
                  className="h-11 rounded-md border border-[var(--line)] px-4 font-bold text-[var(--ink-muted)] hover:bg-[var(--surface-muted)]"
                  onClick={() => setIsOpen(false)}
                  type="button"
                >
                  Cancel
                </button>
                <button
                  className="h-11 rounded-md bg-[var(--blue)] px-4 font-bold text-white disabled:cursor-not-allowed disabled:opacity-50"
                  disabled={isPending}
                  type="submit"
                >
                  {isPending ? "Saving..." : "Save transaction"}
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </>
  );
}
