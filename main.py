
import json
from datetime import date, datetime

try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    expenses = []

last_deleted_expense = None

while True:
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expenses")
    print("4. Edit Expense")
    print("5. Delete Expense")
    print("6. Undo delete Expense")
    print("7. Total Spending")
    print("8. Category-wise Spending")
    print("9. Monthly Spending Summary")
    print("10. Exit")

    choice = input("Enter your choice: ").strip()

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
                expense_date = expense_date.replace("/", "-")
                expense_date = expense_date.replace(" ", "-")

                parsed_date = datetime.strptime(
                    expense_date, "%Y-%m-%d"
                )

                expense_date = parsed_date.strftime("%Y-%m-%d")
                break

            except ValueError:
                print(
                    "Invalid date! Try 2026-10-13 "
                    "or 2026 10 13."
                )

        category = input(
            "Enter category (Food/Travel/Shopping/Other): "
        )

        while True:
            try:
                amount = float(input("Enter amount: "))

                if amount <= 0:
                    print("Amount must be greater than zero!")
                    continue

                break

            except ValueError:
                print(
                    "Invalid amount! Please enter a number, like 150 or 99.50."
                )

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
            print("\n===== YOUR EXPENSES (DATE-WISE) =====")

            sorted_expenses = sorted(
                expenses,
                key=lambda expense: (
                    expense[3] if len(expense) > 3
                    else "9999-99-99"
                )
            )

            for expense in sorted_expenses:
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
        search_name = input(
            "Enter expense name to search: "
        ).strip().lower()

        found = False

        for expense in expenses:
            if (
                search_name in expense[0].lower()
                or search_name in expense[2].lower()
            ):
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

                found = True

        if not found:
            print("No matching expense found.") 

            
    elif choice == "4":
        if len(expenses) == 0:
            print("No expenses to edit.")
        else:
            for i, expense in enumerate(expenses):
                print(i + 1, ".", expense[0], "-", expense[1])

            try:
                number = int(input("Enter expense number to edit: "))

                if 1 <= number <= len(expenses):
                    expense = expenses[number - 1]

                    new_name = input(
                        f"New name [{expense[0]}]: "
                    ).strip()
                    if new_name:
                        expense[0] = new_name

                    new_amount = input(
                        f"New amount [{expense[1]}]: "
                    ).strip()
                    if new_amount:
                        try:
                            amount = float(new_amount)
                            if amount >= 0:
                                expense[1] = amount
                            else:
                                print("Amount cannot be negative.")
                        except ValueError:
                            print("Invalid amount. Keeping old amount.")

                    new_category = input(
                        f"New category [{expense[2]}]: "
                    ).strip()
                    if new_category:
                        expense[2] = new_category

                    new_date = input(
                        f"New date [{expense[3] if len(expense) > 3 else 'Old expense'}] "
                        "(YYYY-MM-DD, Enter to keep): "
                    ).strip()

                    if new_date:
                        try:
                            new_date = new_date.replace("/", "-")
                            new_date = new_date.replace(" ", "-")
                            parsed_date = datetime.strptime(
                                new_date, "%Y-%m-%d"
                            )
                            new_date = parsed_date.strftime("%Y-%m-%d")

                            if len(expense) > 3:
                                expense[3] = new_date
                            else:
                                expense.append(new_date)
                        except ValueError:
                            print("Invalid date. Keeping old date.")

                    with open("expenses.json", "w") as file:
                        json.dump(expenses, file, indent=4)

                    print("Expense updated successfully!")
                else:
                    print("Invalid expense number.")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "5":
        if len(expenses) == 0:
            print("No expenses to delete.")
        else:
            print("\n===== DELETE EXPENSE =====")

            for i, expense in enumerate(expenses):
                print(i + 1, ".", expense[0], "-", expense[1])

            try:
                number = int(input("Enter expense number to delete: "))

                if 1 <= number <= len(expenses):
                    deleted_expense = expenses.pop(number - 1)
                    last_deleted_expense = (number - 1, deleted_expense)

                    with open("expenses.json", "w") as file:
                        json.dump(expenses, file, indent=4)

                    print("Deleted:", deleted_expense[0])
                else:
                    print("Invalid expense number")

            except ValueError:
                print("Please enter a valid number.")

    elif choice == "6":
        if last_deleted_expense is None:
            print("No expense to undo.")
        else:
            index, expense = last_deleted_expense
            expenses.insert(index, expense)

            with open("expenses.json", "w") as file:
                json.dump(expenses, file, indent=4)

            print("Restored:", expense[0])
            last_deleted_expense = None


    elif choice == "7":
        total = 0

        for expense in expenses:
            total += expense[1]

        print("Total Spending:", total)
        
    elif choice == "8":
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
    
    elif choice == "9":
        selected_month = input("Enter month (YYYY-MM): ")

        monthly_total = 0

        for expense in expenses:
            if len(expense) > 3:
                if expense[3].startswith(selected_month):
                    monthly_total += expense[1]

        print(
            selected_month,
            "Total Spending:",
            monthly_total
        )
    
    elif choice == "10":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")