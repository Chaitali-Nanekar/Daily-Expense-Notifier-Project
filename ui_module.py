import tkinter as tk
from tkinter import ttk, messagebox
import database_module as db
import logic_module as logic

# ---------------- LOGIN / REGISTER ---------------- #
def register_user(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "All fields required")
        return
    if db.add_user(username, password):
        messagebox.showinfo("Success", "Registration Successful! You can now login.")
    else:
        messagebox.showerror("Error", "Username already exists")

def login_user(username_entry, password_entry, login_window):
    username = username_entry.get()
    password = password_entry.get()
    if db.validate_user(username, password):
        logic.logged_in_user = username
        messagebox.showinfo("Success", f"Welcome {username}!")
        login_window.destroy()
        open_expense_tracker()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# ---------------- EXPENSE TRACKER GUI ---------------- #
def open_expense_tracker():
    app = tk.Toplevel()
    app.title("Daily Expense Notifier")
    app.state("zoomed")
    app.configure(bg="#f0f0f0")

    tk.Label(app, text=f"DAILY EXPENSE NOTIFIER - {logic.logged_in_user}",
             font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=20)

    frame = tk.Frame(app, bg="#f0f0f0")
    frame.pack(pady=10)

    # Amount
    tk.Label(frame, text="Amount", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    amount_entry = tk.Entry(frame, font=("Arial", 14))
    amount_entry.grid(row=0, column=1, pady=10)

    # Category
    tk.Label(frame, text="Category", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, sticky="w")
    category_entry = ttk.Combobox(frame, values=["Food", "Travel", "Shopping", "Bills", "Other"], font=("Arial", 14))
    category_entry.grid(row=1, column=1)
    category_entry.current(0)

    # Description
    tk.Label(frame, text="Description", font=("Arial", 14), bg="#f0f0f0").grid(row=2, column=0, padx=10, sticky="w")
    desc_entry = tk.Entry(frame, font=("Arial", 14))
    desc_entry.grid(row=2, column=1)

    # Table
    columns = ("Date", "Amount", "Category", "Description")
    table = ttk.Treeview(app, columns=columns, show="headings", height=20)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=200)
    table.pack(pady=20, fill="both", expand=True)

    # Buttons
    tk.Button(frame, text="Add Expense", font=("Arial", 14, "bold"), bg="#27ae60", fg="white",
              command=lambda: add_expense_ui(amount_entry, category_entry, desc_entry, table)).grid(row=3, column=0, columnspan=2, pady=15)

    tk.Label(frame, text="Daily Budget", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=2, padx=10, sticky="w")
    budget_entry = tk.Entry(frame, font=("Arial", 14))
    budget_entry.grid(row=0, column=3)
    tk.Button(frame, text="Set Budget", font=("Arial", 14), bg="#2980b9", fg="white",
              command=lambda: set_budget_ui(budget_entry)).grid(row=1, column=3, pady=5)

    tk.Label(frame, text="Month (YYYY-MM)", font=("Arial", 14), bg="#f0f0f0").grid(row=2, column=2, padx=10, sticky="w")
    month_entry = tk.Entry(frame, font=("Arial", 14))
    month_entry.grid(row=2, column=3)
    tk.Button(frame, text="Monthly Report", font=("Arial", 14), bg="#8e44ad", fg="white",
              command=lambda: monthly_report_ui(month_entry)).grid(row=3, column=3, pady=15)

    load_expenses(table)

# ---------------- UI LOGIC ---------------- #
def add_expense_ui(amount_entry, category_entry, desc_entry, table):
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        desc = desc_entry.get()
        if not category or not desc:
            messagebox.showerror("Error", "All fields required")
            return
        exceeded = logic.add_expense(amount, category, desc)
        load_expenses(table)
        if exceeded:
            messagebox.showwarning("Alert", "Daily Budget Exceeded!")
        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter valid amount")

def set_budget_ui(budget_entry):
    try:
        amount = float(budget_entry.get())
        logic.set_budget(amount)
        messagebox.showinfo("Budget Set", f"Daily Budget Set: ₹{amount}")
    except ValueError:
        messagebox.showerror("Error", "Invalid budget")

def monthly_report_ui(month_entry):
    month = month_entry.get()
    total = logic.get_monthly_total(month)
    messagebox.showinfo("Monthly Report", f"Total Expense for {month}: ₹{total}")

def load_expenses(table):
    for row in table.get_children():
        table.delete(row)
    data = logic.get_all_expenses()
    for row in data:
        table.insert("", tk.END, values=row)
