from datetime import date
import winsound
import database_module as db

daily_budget = 0
logged_in_user = ""

def set_budget(amount):
    global daily_budget
    daily_budget = amount

def add_expense(amount, category, description):
    today = str(date.today())
    db.add_expense(logged_in_user, today, amount, category, description)
    if daily_budget > 0 and db.get_today_total(logged_in_user, today) > daily_budget:
        winsound.Beep(1000, 500)
        return True  # Budget exceeded
    return False

def get_today_total():
    today = str(date.today())
    return db.get_today_total(logged_in_user, today)

def get_monthly_total(month):
    return db.get_monthly_total(logged_in_user, month)

def get_all_expenses():
    return db.get_expenses(logged_in_user)
