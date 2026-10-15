
import sqlite3
from datetime import date

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    expense_date TEXT NOT NULL,
    note TEXT
)
""")
conn.commit()


def add_expense():
    try:
        amount = float(input("Amount: ₹"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        category = input("Category: ").strip()
        if not category:
            print("Category cannot be empty.")
            return

        expense_date = input(
            f"Date (YYYY-MM-DD, default {date.today()}): "
        ).strip() or str(date.today())

        date.fromisoformat(expense_date)
        note = input("Note (optional): ").strip()

        cursor.execute(
            """INSERT INTO expenses
            (amount, category, expense_date, note)
            VALUES (?, ?, ?, ?)""",
            (amount, category, expense_date, note)
        )
        conn.commit()
        print("Expense added successfully!")

    except ValueError:
        print("Please enter a valid amount or date.")


def view_expenses():
    cursor.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC"
    )
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found.")
        return

    for row in rows:
        print(row)


def show_total():
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    print(f"Total spending: ₹{cursor.fetchone()[0]:.2f}")


while True:
    print("\n--- Personal Expense Tracker ---")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Show total spending")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        show_total()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Try again.")

conn.close()
