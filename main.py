import json
import os

CAREER_FILE = "career_data.json"
FINANCE_FILE = "finance_data.json"


def load_data(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main_menu():
    while True:
        print("\n=== CareerLaunch ===")
        print("1. Career progress")
        print("2. Finance tracker")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            career_menu()
        elif choice == "2":
            finance_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


def career_menu():
    career_data = load_data(CAREER_FILE, {"applications": []})

    while True:
        print("\n--- Career Progress ---")
        print("1. Add application")
        print("2. List applications")
        print("3. Update application status")
        print("4. Show stats")
        print("5. Show upcoming deadlines")
        print("6. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            add_application(career_data)
            save_data(CAREER_FILE, career_data)
        elif choice == "2":
            list_applications(career_data)
        elif choice == "3":
            update_application_status(career_data)
            save_data(CAREER_FILE, career_data)
        elif choice == "4":
            show_career_stats(career_data)
        elif choice == "5":
            show_upcoming_deadlines(career_data)
        elif choice == "6":
            break
        else:
            print("Invalid choice, try again.")


def finance_menu():
    finance_data = load_data(FINANCE_FILE, {
        "income": [],
        "expenses": [],
        "saving_goals": []
    })

    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add income")
        print("2. Add expense")
        print("3. Show summary")
        print("4. Manage saving goals")
        print("5. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            add_income(finance_data)
            save_data(FINANCE_FILE, finance_data)
        elif choice == "2":
            add_expense(finance_data)
            save_data(FINANCE_FILE, finance_data)
        elif choice == "3":
            show_finance_summary(finance_data)
        elif choice == "4":
            manage_saving_goals(finance_data)
            save_data(FINANCE_FILE, finance_data)
        elif choice == "5":
            break
        else:
            print("Invalid choice, try again.")


# ---- Career functions (to implement) ----

def add_application(career_data):
    print("\nAdd new application")
    company = input("Company: ")
    role = input("Role: ")
    location = input("Location: ")
    applied_date = input("Applied date (YYYY-MM-DD): ")
    deadline = input("Deadline (YYYY-MM-DD, optional): ")

    new_id = len(career_data["applications"]) + 1

    app = {
        "id": new_id,
        "company": company,
        "role": role,
        "location": location,
        "applied_date": applied_date,
        "deadline": deadline,
        "status": "applied",
        "notes": ""
    }

    career_data["applications"].append(app)
    print("Application added.")


def list_applications(career_data):
    print("\nYour applications:")
    if not career_data["applications"]:
        print("No applications yet.")
        return

    for app in career_data["applications"]:
        print(f"[{app['id']}] {app['company']} - {app['role']} ({app['status']})")


def update_application_status(career_data):
    list_applications(career_data)
    if not career_data["applications"]:
        return

    try:
        app_id = int(input("Enter application ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    app = next((a for a in career_data["applications"] if a["id"] == app_id), None)
    if not app:
        print("Application not found.")
        return

    print("New status options: applied, interview, offer, rejected")
    new_status = input("New status: ").strip().lower()

    if new_status not in ["applied", "interview", "offer", "rejected"]:
        print("Invalid status.")
        return

    app["status"] = new_status
    print("Status updated.")


def show_career_stats(career_data):
    apps = career_data["applications"]
    total = len(apps)
    print("\nCareer stats:")
    print(f"Total applications: {total}")

    status_counts = {"applied": 0, "interview": 0, "offer": 0, "rejected": 0}
    for app in apps:
        if app["status"] in status_counts:
            status_counts[app["status"]] += 1

    for status, count in status_counts.items():
        print(f"{status.capitalize()}: {count}")

    if total > 0:
        success_rate = status_counts["offer"] / total * 100
        print(f"Success rate (offers/applications): {success_rate:.1f}%")
    else:
        print("Success rate: N/A")


def show_upcoming_deadlines(career_data):
    print("\n(For now, this will just list applications with a deadline set.)")
    has_deadline = [a for a in career_data["applications"] if a["deadline"]]
    if not has_deadline:
        print("No deadlines stored.")
        return

    for app in has_deadline:
        print(f"{app['company']} - {app['role']} | Deadline: {app['deadline']}")


# ---- Finance functions (to implement) ----

def add_income(finance_data):
    print("\nAdd income")
    source = input("Source (e.g., internship): ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")

    new_id = len(finance_data["income"]) + 1
    income = {
        "id": new_id,
        "source": source,
        "amount": amount,
        "date": date
    }
    finance_data["income"].append(income)
    print("Income added.")


def add_expense(finance_data):
    print("\nAdd expense")
    category = input("Category (e.g., rent, food): ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    note = input("Note (optional): ")

    new_id = len(finance_data["expenses"]) + 1
    expense = {
        "id": new_id,
        "category": category,
        "amount": amount,
        "date": date,
        "note": note
    }
    finance_data["expenses"].append(expense)
    print("Expense added.")


def show_finance_summary(finance_data):
    total_income = sum(i["amount"] for i in finance_data["income"])
    total_expenses = sum(e["amount"] for e in finance_data["expenses"])
    balance = total_income - total_expenses

    print("\nFinance summary:")
    print(f"Total income: {total_income:.2f}")
    print(f"Total expenses: {total_expenses:.2f}")
    print(f"Balance: {balance:.2f}")


def manage_saving_goals(finance_data):
    print("\nSaving goals:")
    goals = finance_data["saving_goals"]
    if not goals:
        print("No saving goals yet.")
    else:
        for g in goals:
            print(f"[{g['id']}] {g['name']} - {g['current_amount']}/{g['target_amount']}")

    print("1. Add new goal")
    print("2. Update existing goal")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Goal name: ")
        target = float(input("Target amount: "))
        new_id = len(goals) + 1
        goal = {
            "id": new_id,
            "name": name,
            "target_amount": target,
            "current_amount": 0.0
        }
        goals.append(goal)
        print("Goal added.")
    elif choice == "2":
        if not goals:
            print("No goals to update.")
            return
        try:
            goal_id = int(input("Goal ID to update: "))
        except ValueError:
            print("Invalid ID.")
            return
        goal = next((g for g in goals if g["id"] == goal_id), None)
        if not goal:
            print("Goal not found.")
            return
        add = float(input("How much to add to this goal? "))
        goal["current_amount"] += add
        print("Goal updated.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
