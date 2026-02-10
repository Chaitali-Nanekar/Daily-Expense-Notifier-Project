import tkinter as tk
from ui_module import register_user, login_user
import database_module as db

db.init_db()  # Initialize database

login_window = tk.Tk()
login_window.title("Daily Expense Notifier - Login/Register")
login_window.state("zoomed")
login_window.configure(bg="#f0f0f0")

tk.Label(login_window, text="DAILY EXPENSE NOTIFIER", font=("Helvetica", 30, "bold"), fg="#2c3e50", bg="#f0f0f0").pack(pady=50)

frame_login = tk.Frame(login_window, bg="#f0f0f0")
frame_login.pack(pady=10)

tk.Label(frame_login, text="Username", font=("Helvetica", 16), bg="#f0f0f0").grid(row=0, column=0, pady=10, sticky="w")
username_entry = tk.Entry(frame_login, font=("Helvetica", 16), width=30, bd=2, relief="groove")
username_entry.grid(row=0, column=1, pady=10)

tk.Label(frame_login, text="Password", font=("Helvetica", 16), bg="#f0f0f0").grid(row=1, column=0, pady=10, sticky="w")
password_entry = tk.Entry(frame_login, font=("Helvetica", 16), width=30, show="*", bd=2, relief="groove")
password_entry.grid(row=1, column=1, pady=10)

button_frame = tk.Frame(login_window, bg="#f0f0f0")
button_frame.pack(pady=30)

tk.Button(button_frame, text="Login", font=("Helvetica", 16, "bold"), bg="#27ae60", fg="white", width=15,
          command=lambda: login_user(username_entry, password_entry, login_window)).grid(row=0, column=0, padx=20, pady=10)
tk.Button(button_frame, text="Register", font=("Helvetica", 16, "bold"), bg="#2980b9", fg="white", width=15,
          command=lambda: register_user(username_entry, password_entry)).grid(row=0, column=1, padx=20, pady=10)

login_window.mainloop()
