import tkinter as tk
from tkinter import simpledialog, messagebox
from bankAccount import BankAccount

class BankAccountGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.current_frame = None
        self.account = None
        self.account_id = None
        self.password = None
        self.create_login_menu()

    def create_login_menu(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Welcome to the banking system!", font=("Arial", 20)).pack(pady=20)
        login_button = tk.Button(self.current_frame, text="Login", command=self.show_login_form)
        login_button.pack()
        tk.Button(self.current_frame, text="Create Account", command=self.show_create_account_form).pack()

    def show_login_form(self):
        self.clear_current_frame()
        tk.Label(self.current_frame, text="Enter your account ID:").pack()
        self.account_id_entry = tk.Entry(self.current_frame)
        self.account_id_entry.pack()

        tk.Label(self.current_frame, text="Enter your password:").pack()
        self.password_entry = tk.Entry(self.current_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.current_frame, text="Login", command=self.login).pack()
        tk.Button(self.current_frame, text="Back", command=self.create_login_menu).pack()

    def show_create_account_form(self):
        self.clear_current_frame()
        tk.Label(self.current_frame, text="Enter your account ID:").pack()
        self.create_account_id_entry = tk.Entry(self.current_frame)
        self.create_account_id_entry.pack()

        tk.Label(self.current_frame, text="Enter your password:").pack()
        self.create_password_entry = tk.Entry(self.current_frame, show="*")
        self.create_password_entry.pack()

        tk.Label(self.current_frame, text="Enter your name:").pack()
        self.create_owner_entry = tk.Entry(self.current_frame)
        self.create_owner_entry.pack()

        tk.Label(self.current_frame, text="Enter your payout limit:").pack()
        self.create_payout_limit_entry = tk.Entry(self.current_frame)
        self.create_payout_limit_entry.pack()

        tk.Button(self.current_frame, text="Create Account", command=self.create_account).pack()
        tk.Button(self.current_frame, text="Back", command=self.create_login_menu).pack()

    def login(self):
        self.account_id = self.account_id_entry.get()
        self.password = self.password_entry.get()
        self.account = BankAccount.load_account_data(self.account_id, self.password)
        if self.account:
            self.show_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def create_account(self):
        account_id = self.create_account_id_entry.get()
        password = self.create_password_entry.get()
        owner = self.create_owner_entry.get()
        payout_limit = self.create_payout_limit_entry.get()

        # Check if any field is empty
        if not account_id or not password or not owner or not payout_limit:
            messagebox.showerror("Error", "All fields must be filled out to create an account.")
            return

        try:
            payout_limit = float(payout_limit)
            if payout_limit < 0:
                raise ValueError("Payout limit cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Payout limit must be a positive number.")
            return

        self.account = BankAccount(account_id, 0, owner, payout_limit, password=password)
        self.account.save_account_data()
        messagebox.showinfo("Success", "Account created successfully.")
        self.show_menu()

    def show_menu(self):
        self.clear_current_frame()

        self.deposit_button = tk.Button(self.current_frame, text="Deposit", command=self.deposit, font=("Helvetica", 14))
        self.deposit_button.pack(pady=10)

        self.payout_button = tk.Button(self.current_frame, text="Payout", command=self.payout, font=("Helvetica", 14))
        self.payout_button.pack(pady=10)

        self.check_balance_button = tk.Button(self.current_frame, text="Check Balance", command=self.check_balance, font=("Helvetica", 14))
        self.check_balance_button.pack(pady=10)

        self.transaction_history_button = tk.Button(self.current_frame, text="Transaction History", command=self.transaction_history, font=("Helvetica", 14))
        self.transaction_history_button.pack(pady=10)

        self.change_password_button = tk.Button(self.current_frame, text="Change Password", command=self.change_password, font=("Helvetica", 14))
        self.change_password_button.pack(pady=10)

        self.quit_button = tk.Button(self.current_frame, text="Quit", command=self.root.destroy, font=("Helvetica", 14))
        self.quit_button.pack(pady=10)

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter the deposit amount:")
        if amount is not None:
            message = self.account.deposit(amount)
            self.account.save_account_data()
            messagebox.showinfo("Deposit", message)

    def payout(self):
        amount = simpledialog.askfloat("Payout", "Enter the payout amount:")
        if amount is not None:
            result = self.account.payout(amount)
            if result is True:
                self.account.save_account_data()
                messagebox.showinfo("Payout", f"The payment for the amount {amount} has been processed.\nYour current balance is {self.account.get_balance()} PLN.")
            else:
                messagebox.showwarning("Error", result)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is {self.account.get_balance()} PLN.")

    def transaction_history(self):
        history = "\n".join([f"{transaction['type']} of {transaction['amount']} PLN" for transaction in self.account.transaction_history])
        messagebox.showinfo("Transaction History", f"Transaction History:\n{history}")

    def change_password(self):
        old_password = simpledialog.askstring("Change Password", "Enter your current password:", show="*")
        new_password = simpledialog.askstring("Change Password", "Enter your new password:", show="*")
        if old_password and new_password:
            result = self.account.change_password(old_password, new_password)
            messagebox.showinfo("Change Password", result)

    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()
