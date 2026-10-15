"""
Personal Expense Tracker
A beginner-friendly terminal application using Python and SQLite.

Run:
    python expense_tracker.py
"""

import sqlite3
from datetime import date, datetime
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")
DATE_FORMAT = "%Y-%m-%d"


def connect_db():
    """Open a connection to the local SQLite database."""
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the expenses table if it does not already exist."""
    with connect_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                note TEXT DEFAULT ''
            )
            """
        )


def read_amount(prompt="Enter amount: "):
    """Ask for a positive amount and reject invalid input."""
    while True:
        raw_value = input(prompt).strip()
        try:
            amount = float(raw_value)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number, such as 125.50.")


def read_date(prompt="Enter date (YYYY-MM-DD), or press Enter for today: "):
    """Read a valid date. Empty input uses today's date."""
    while True:
        raw_value = input(prompt).strip()
        if not raw_value:
            return date.today().isoformat()
        try:
            parsed = datetime.strptime(raw_value, DATE_FORMAT).date()
            return parsed.isoformat()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-10-15.")


def add_expense():
    """Collect expense details and save them to SQLite."""
    print("\n--- Add Expense ---")
    amount = read_amount()
    category = input("Enter category (e.g., Food, Travel): ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    expense_date = read_date()
    note = input("Enter note (optional): ").strip()

    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO expenses (amount, category, expense_date, note)
            VALUES (?, ?, ?, ?)
            """,
            (amount, category, expense_date, note),
        )
    print("Expense saved successfully.")


def get_all_expenses():
    """Return all expenses, newest date first."""
    with connect_db() as connection:
        return connection.execute(
            """
            SELECT id, amount, category, expense_date, note
            FROM expenses
            ORDER BY expense_date DESC, id DESC
            """
        ).fetchall()


def print_expenses(rows):
    """Display expense rows in a readable table."""
    if not rows:
        print("\nNo expenses found.")
        return

    print("\n{:<5} {:<12} {:>10}  {:<18} {}".format(
        "ID", "Date", "Amount", "Category", "Note"
    ))
    print("-" * 72)
    for row in rows:
        note = row["note"] or ""
        print("{:<5} {:<12} {:>10.2f}  {:<18} {}".format(
            row["id"], row["expense_date"], row["amount"],
            row["category"][:18], note
        ))
    total = sum(row["amount"] for row in rows)
    print("-" * 72)
    print(f"Number of expenses: {len(rows)} | Total: {total:.2f}")


def view_expenses():
    """Display all saved expenses."""
    print_expenses(get_all_expenses())


def spending_summary():
    """Show overall spending and totals grouped by category."""
    with connect_db() as connection:
        total_row = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS count FROM expenses"
        ).fetchone()
        categories = connection.execute(
            """
            SELECT category, SUM(amount) AS total, COUNT(*) AS count
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            """
        ).fetchall()

    print("\n--- Spending Summary ---")
    print(f"Total spent: {total_row['total']:.2f}")
    print(f"Number of expenses: {total_row['count']}")
    if not categories:
        print("No expenses to summarize yet.")
        return

    print("\nBy category:")
    for row in categories:
        print(f"- {row['category']}: {row['total']:.2f} ({row['count']} entries)")


def monthly_report():
    """Show expense totals for a month entered by the user."""
    while True:
        month = input("Enter month (YYYY-MM), e.g. 2026-10: ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            break
        except ValueError:
            print("Invalid month. Use YYYY-MM.")

    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT id, amount, category, expense_date, note
            FROM expenses
            WHERE substr(expense_date, 1, 7) = ?
            ORDER BY expense_date DESC, id DESC
            """,
            (month,),
        ).fetchall()

    print(f"\n--- Monthly Report: {month} ---")
    print_expenses(rows)


def delete_expense():
    """Delete one expense after asking for confirmation."""
    raw_id = input("Enter the ID of the expense to delete: ").strip()
    try:
        expense_id = int(raw_id)
        if expense_id <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid positive ID.")
        return

    with connect_db() as connection:
        row = connection.execute(
            "SELECT id, amount, category, expense_date FROM expenses WHERE id = ?",
            (expense_id,),
        ).fetchone()
        if row is None:
            print("No expense found with that ID.")
            return

        print(
            f"Selected: ID {row['id']} | {row['expense_date']} | "
            f"{row['category']} | {row['amount']:.2f}"
        )
        confirm = input("Delete this expense? (y/N): ").strip().lower()
        if confirm == "y":
            connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            print("Expense deleted.")
        else:
            print("Delete cancelled.")


def show_menu():
    """Print the application menu."""
    print("\n" + "=" * 34)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 34)
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Spending summary")
    print("4. Monthly report")
    print("5. Delete an expense")
    print("0. Exit")


def main():
    initialize_database()
    print(f"Database file: {DB_FILE.name}")
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            spending_summary()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            delete_expense()
        elif choice == "0":
            print("Thanks for using Personal Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 0, 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
