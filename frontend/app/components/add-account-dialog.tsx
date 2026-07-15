"use client";

import { useActionState, useMemo, useState } from "react";

import { addAccountAction, type AddAccountState } from "../actions/accounts";

const initialState: AddAccountState = {
  success: false,
  error: null,
};

const accountTypes = [
  { value: "checking", label: "Checking" },
  { value: "savings", label: "Savings" },
  { value: "credit_card", label: "Credit card" },
  { value: "cash", label: "Cash" },
  { value: "investment", label: "Investment" },
  { value: "loan", label: "Loan" },
  { value: "other", label: "Other" },
];

export function AddAccountDialog() {
  const [isOpen, setIsOpen] = useState(false);
  const [state, formAction, isPending] = useActionState(
    addAccountAction,
    initialState,
  );
  const dialogTitleId = useMemo(() => "add-account-title", []);

  return (
    <>
      <button
        className="h-11 rounded-md border border-[var(--line)] bg-white px-4 font-bold text-[var(--ink)] shadow-sm hover:bg-[var(--surface-muted)]"
        onClick={() => setIsOpen(true)}
        type="button"
      >
        Add account
      </button>

      {isOpen ? (
        <div
          aria-labelledby={dialogTitleId}
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4"
          role="dialog"
        >
          <div className="max-h-[calc(100vh-2rem)] w-full max-w-xl overflow-y-auto rounded-lg border border-[var(--line)] bg-white shadow-2xl">
            <div className="flex items-start justify-between border-b border-[var(--line)] p-5">
              <div>
                <h2 className="text-xl font-bold" id={dialogTitleId}>
                  Add account
                </h2>
                <p className="mt-1 text-sm text-[var(--ink-muted)]">
                  Create an account to attach transactions to.
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
                  Account saved.
                </p>
              ) : null}

              {state.error ? (
                <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm font-semibold text-[var(--red)]">
                  {state.error}
                </p>
              ) : null}

              <label className="grid gap-2 text-sm font-semibold">
                Account name
                <input
                  className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                  maxLength={120}
                  name="name"
                  placeholder="Everyday Checking"
                  required
                  type="text"
                />
              </label>

              <div className="grid gap-4 md:grid-cols-2">
                <label className="grid gap-2 text-sm font-semibold">
                  Type
                  <select
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    name="account_type"
                    required
                  >
                    {accountTypes.map((accountType) => (
                      <option key={accountType.value} value={accountType.value}>
                        {accountType.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="grid gap-2 text-sm font-semibold">
                  Opening balance
                  <input
                    className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                    defaultValue="0.00"
                    name="opening_balance"
                    step="0.01"
                    type="number"
                  />
                </label>
              </div>

              <label className="grid gap-2 text-sm font-semibold">
                Institution
                <input
                  className="h-11 rounded-md border border-[var(--line)] bg-white px-3 outline-none focus:border-[var(--blue)]"
                  maxLength={120}
                  name="institution_name"
                  placeholder="Optional"
                  type="text"
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
                  {isPending ? "Saving..." : "Save account"}
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </>
  );
}
