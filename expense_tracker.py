
# --- Functions ---


from expense import Expsense
import csv
import datetime
import calendar

def color_text(text, color="green"):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "bold": "\033[1m",
    }
    RESET = "\033[0m"
    color_code = colors.get(color.lower(), "")
    return f"{color_code}{text}{RESET}"

def get_user_expense():
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc"
    ]

    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        selected_index = int(input("Enter category number (1-5): "))

        if 1 <= selected_index <= len(expense_categories):
            selected_category = expense_categories[selected_index - 1]
            print(color_text(f"✅ Selected category: {selected_category}","green"))
            new_expense= Expsense(name=expense_name,category=selected_category,amount=expense_amount)
            break
        else:
           print(color_text("❌ Invalid choice, please try again!", "red"))

    
    return new_expense
    
                           
def save_expense_to_file(expense:Expsense,expense_file_path):
    print(f"🎯 Saving User Expense {expense} To File: {expense_file_path}")
    with open(expense_file_path,"a",encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")




def summarize_expenses(expense_file_path,budget):
    print("🎯 Summarizing Expenses")
    expenses:list[Expsense] = []

    with open(expense_file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for lineno, row in enumerate(reader, start=1):
            if not row:
                continue
            if len(row) == 3 and row[0].lower() == "name":
                continue  # header
            if len(row) != 3:
                print(f"⚠️ Skipping malformed line {lineno}: {row!r}")
                continue

            expense_name, expense_amount, expense_category = [c.strip() for c in row]
            try:
                line_expense = Expsense(expense_name, expense_category, expense_amount)
            except ValueError:
                print(f"⚠️ Skipping line {lineno} due to bad amount: {expense_amount!r}")
                continue

            
            expenses.append(line_expense)
    amount_by_category={}
    for expense in expenses:
        key=expense.category
        if key in amount_by_category:
            amount_by_category[key]+=expense.amount
        else:
            amount_by_category[key]=expense.amount
    
    for key,amount in amount_by_category.items():
        print(f"   {key}: ${amount:.2f}")
    

    total_spent=sum([ex.amount for ex in expenses])
    print(f"💵 You've spent: {total_spent:.2f}$")

    balance=budget-total_spent
    print(f"💰 Balance: {balance:.2f}$ ")

    today = datetime.date.today()

    days_in_month = calendar.monthrange(today.year, today.month)[1]

    remaining_days = days_in_month - today.day
    print(f"⏳ Remaining {remaining_days} days until the end of the month")

    if remaining_days > 0:
      daily_budget = balance / remaining_days
      print(f"❗ Budget Per Day: {daily_budget:.2f}")
    else:
      print("✅ Today is the last day of the month — no remaining days to split the budget.")



def show_menu():
    print()
    print(color_text("==== Expense Tracker Menu ====", "bold"))
    print(" 1) Add expense")
    print(" 2) Set budget")
    print(" 3) Summarize expenses")
    print(" 4) List expenses")
    print(" 5) Exit")

def get_choice():
    while True:
        choice = input(color_text("Select an option (1-5): ", "cyan"))
        if choice in {"1", "2", "3", "4", "5"}:
            return int(choice)
        print(color_text("❌ Invalid choice, please try again!", "red"))

def run_menu_loop():
    expense_file_path = "expenses.csv"
    budget = None  # store user budget

    while True:
        show_menu()
        choice = get_choice()

        if choice == 1:
            print(color_text("→ Add expense selected", "green"))
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)

        elif choice == 2:
            print(color_text("→ Set budget selected", "green"))
            try:
                budget = float(input(color_text("Set monthly budget ($): ", "cyan")))
                print(color_text(f"✅ Budget set to ${budget:.2f}", "green"))
            except ValueError:
                print(color_text("❌ Invalid amount. Please enter a number.", "red"))

        elif choice == 3:
            print(color_text("→ Summarize expenses selected", "green"))
            if budget is None:
                print(color_text("⚠️ Please set your budget first (option 2).", "yellow"))
            else:
                summarize_expenses(expense_file_path, budget)

        elif choice == 4:
            print(color_text("→ Show all expenses selected", "green"))
            # You can later add a list_expenses(expense_file_path) function
            with open(expense_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(color_text("\n--- All Expenses ---", "bold"))
                for line in lines:
                    print(color_text(line.strip(), "cyan"))

        elif choice == 5:
            print(color_text("👋 Exiting. Goodbye!", "yellow"))
            break

def main():
    print(color_text("🎯 Running Expense Tracker!", "bold"))
    run_menu_loop()

if __name__=="__main__":
    main()

