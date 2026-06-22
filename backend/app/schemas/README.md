# Backend Schemas

Schemas define the API contract. They should stay independent from the database
provider so the app can move from SQLite to Postgres, Supabase, or another store
without rewriting request and response shapes.

## Current Rules

- Store money as integer cents, never floats.
- Keep create, update, and read schemas separate.
- Use enums for values the UI should not invent.
- Keep route handlers thin: routes receive schemas, services do business logic.
- Treat dashboard schemas as read models derived from transactions.

## First Domain Slice

- `accounts.py`: where money lives.
- `categories.py`: how expenses are grouped.
- `transactions.py`: the source of truth for spending/income activity.
- `dashboard.py`: response shapes for UI widgets.
