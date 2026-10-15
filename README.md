# Personal Expense Tracker (Python + SQLite)

A beginner-friendly terminal application for recording personal expenses and reviewing spending. Built with Python and SQLite, with no third-party packages required.

## Features

- Add expenses with amount, category, date, and optional note
- View all saved expenses
- View total spending and category-wise totals
- Generate a report for a chosen month
- Delete an expense after confirmation
- Validate amounts, dates, menu choices, and expense IDs
- Store records locally in an SQLite database file (`expenses.db`)

## Requirements

- Python 3.9 or later recommended
- SQLite support included with standard Python installations
- No `pip install` is required

## Run the project

1. Download or clone this repository.
2. Open a terminal/Command Prompt in the project folder.
3. Run:

   ```bash
   python expense_tracker.py
   ```

   On some systems, use `python3 expense_tracker.py` or `py expense_tracker.py`.

4. Choose an option from the menu.
5. The program creates `expenses.db` automatically the first time it runs.

## Example workflow

1. Choose `1` to add an expense.
2. Enter an amount such as `150.50`.
3. Enter a category such as `Food`.
4. Press Enter to use today's date, or enter a date like `2026-10-15`.
5. Add an optional note.
6. Choose `3` to view the spending summary.

The displayed totals depend on the expenses you enter; no sample financial data is preloaded.

## Database design

The `expenses` table contains:

| Column | Type | Purpose |
|---|---|---|
| `id` | INTEGER | Unique ID; primary key |
| `amount` | REAL | Expense amount greater than zero |
| `category` | TEXT | Expense category |
| `expense_date` | TEXT | Date in `YYYY-MM-DD` format |
| `note` | TEXT | Optional note |

## SQL concepts demonstrated

- `CREATE TABLE IF NOT EXISTS`
- `INSERT INTO`
- `SELECT`, `WHERE`, and `ORDER BY`
- `SUM`, `COUNT`, and `COALESCE`
- `GROUP BY`
- `DELETE`
- Parameterized SQL queries (`?`) to pass user values safely

## Quick test checklist

- [ ] Add a valid expense and confirm it appears in option 2.
- [ ] Enter `0`, a negative number, and non-numeric text for amount; confirm each is rejected.
- [ ] Enter an invalid date and confirm the program asks again.
- [ ] Add expenses in two categories and check option 3.
- [ ] Run a monthly report for a month containing an expense.
- [ ] Delete an expense and verify it no longer appears.
- [ ] Exit and run the program again; verify saved records remain.

## Project structure

```text
expense-tracker-python/
├── expense_tracker.py
├── README.md
├── .gitignore
├── LICENSE
└── LINKEDIN_POST.txt
```

The local `expenses.db` file is created at runtime and is ignored by Git so personal spending data is not uploaded accidentally.

## Limitations and future improvements

This is a local, single-user terminal project. It does not connect to a bank, sync across devices, or provide financial advice. Possible future additions include editing an expense, exporting CSV, budget limits, and automated tests.

## Author

Created as a learning project to practice Python fundamentals, SQL queries, and database operations. Update this section with your name and GitHub profile before publishing.
