import json

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
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        expense_name = input("Enter expense name: ")
        category = input("Enter category (Food/Travel/Shopping/Other): ")
        amount = float(input("Enter amount: "))

        expenses.append([expense_name, amount, category])
        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)
        print("Expense added:", expense_name)
        print("Amount:", amount)

    elif choice == "2":
        if len(expenses) == 0:
            print("No expenses found.")
        else:
            print("\n===== YOUR EXPENSES =====")
            for expense in expenses:
                print("Name:", expense[0], "| Amount:", expense[1], "| Category:", expense[2])

    elif choice == "3":
        if len(expenses) == 0:
            print("No expenses to delete.")
        else:
            print("\n===== DELETE EXPENSE =====")

            for i, expense in enumerate(expenses):
                print(i + 1, ".", expense[0], "-", expense[1])

            number = int(input("Enter expense number to delete: "))

            if number >= 1 and number <= len(expenses):
                deleted_expense = expenses.pop(number - 1)
                with open("expenses.json", "w") as file:
                    json.dump(expenses, file, indent=4)
                print("Deleted:", deleted_expense[0])
            else:
                print("Invalid expense number")

    elif choice == "4":
        total = 0

        for expense in expenses:
            total = total + expense[1]

        print("Total Spending:", total)

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")