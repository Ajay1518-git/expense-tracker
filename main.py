
import json
from datetime import date, datetime

try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    expenses = []

while True:
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Total Spending")
    print("5. Category-wise Spending")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        expense_name = input("Enter expense name: ")

        today = date.today().strftime("%Y-%m-%d")

        while True:
            expense_date = input(
                f"Enter expense date (YYYY-MM-DD) [{today}]: "
            ).strip()

            if expense_date == "":
                expense_date = today
                break

            try:
                datetime.strptime(expense_date, "%Y-%m-%d")
                break
            except ValueError:
                print(
                    "Invalid date! Use YYYY-MM-DD, "
                    "e.g. 2026-10-12."
                )

        category = input(
            "Enter category (Food/Travel/Shopping/Other): "
        )
        amount = float(input("Enter amount: "))

        expenses.append(
            [expense_name, amount, category, expense_date]
        )

        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)

        print("Expense added:", expense_name)
        print("Amount:", amount)
        print("Date:", expense_date)

    elif choice == "2":
        if len(expenses) == 0:
            print("No expenses found.")
        else:
            print("\n===== YOUR EXPENSES =====")

            for expense in expenses:
                expense_date = (
                    expense[3] if len(expense) > 3
                    else "Old expense"
                )

                print(
                    "Name:", expense[0],
                    "| Amount:", expense[1],
                    "| Category:", expense[2],
                    "| Date:", expense_date
                )

    elif choice == "3":
        if len(expenses) == 0:
            print("No expenses to delete.")
        else:
            print("\n===== DELETE EXPENSE =====")

            for i, expense in enumerate(expenses):
                print(
                    i + 1, ".", expense[0],
                    "-", expense[1]
                )

            try:
                number = int(
                    input("Enter expense number to delete: ")
                )

                if 1 <= number <= len(expenses):
                    deleted_expense = expenses.pop(number - 1)

                    with open("expenses.json", "w") as file:
                        json.dump(expenses, file, indent=4)

                    print("Deleted:", deleted_expense[0])
                else:
                    print("Invalid expense number")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "4":
        total = 0

        for expense in expenses:
            total += expense[1]

        print("Total Spending:", total)

    elif choice == "5":
        if len(expenses) == 0:
            print("No expenses found.")
        else:
            category_totals = {}

            for expense in expenses:
                category = expense[2]
                amount = expense[1]

                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount

            print("\n===== CATEGORY-WISE SPENDING =====")

            for category, total in category_totals.items():
                print(category, ":", total)

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")