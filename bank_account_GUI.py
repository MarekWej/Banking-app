import tkinter as tk
from tkinter import simpledialog, messagebox
from bankAccount import BankAccount

class BankAccountGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("500x800")  # Ustawienie rozmiaru okna
        self.account = None
        self.create_widgets()

    def create_widgets(self):
        # Zmiana rozmiaru czcionki etykiety
        self.label = tk.Label(self.root, text="Welcome to the banking system!", font=("Helvetica", 16))
        self.label.pack(pady=20)  # Dodanie odstępu na górze

        # Zwiększenie rozmiaru przycisków
        self.login_button = tk.Button(self.root, text="Login", command=self.login, height=2, width=20, font=("Helvetica", 12))
        self.login_button.pack()

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account, height=2, width=20, font=("Helvetica", 12))
        self.create_account_button.pack()

    def login(self):
        account_id = simpledialog.askstring("Login", "Enter your account ID:")
        password = simpledialog.askstring("Login", "Enter your password:", show="*")
        self.account = BankAccount.load_account_data(account_id, password)
        if self.account:
            self.show_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def create_account(self):
        account_id = simpledialog.askstring("Create Account", "Enter your account ID:")
        owner = simpledialog.askstring("Create Account", "Enter your name:")
        initial_balance = float(simpledialog.askstring("Create Account", "Enter the initial balance:"))
        payout_limit = float(simpledialog.askstring("Create Account", "Enter the payout limit:"))
        password = simpledialog.askstring("Create Account", "Set a password for your account:", show="*")

        self.account = BankAccount(account_id, balance=initial_balance, owner=owner, payout_limit=payout_limit,
                                   password=password)

        self.account.save_account_data()
        messagebox.showinfo("Success", "Account created successfully.")
        self.show_menu()

    def show_menu(self):
        self.label.pack_forget()
        self.login_button.pack_forget()
        self.create_account_button.pack_forget()

        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.deposit, height=2, width=20,
                                        font=("Helvetica", 12))
        self.deposit_button.pack()

        self.payout_button = tk.Button(self.root, text="Payout", command=self.payout, height=2, width=20,
                                       font=("Helvetica", 12))
        self.payout_button.pack()

        self.check_balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance, height=2,
                                              width=20, font=("Helvetica", 12))
        self.check_balance_button.pack()

        self.transaction_history_button = tk.Button(self.root, text="Transaction History",
                                                    command=self.transaction_history, height=2, width=20,
                                                    font=("Helvetica", 12))
        self.transaction_history_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, height=2, width=20,
                                     font=("Helvetica", 12))
        self.quit_button.pack()

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter the deposit amount:")
        if amount is not None:
            confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to deposit {amount} PLN?")
            if confirm:
                self.account.deposit(amount)
                messagebox.showinfo("Deposit",
                                    f"Value {amount} has been added to your bank account.\nYour current balance is {self.account.balance} PLN.")

    def payout(self):
        amount = simpledialog.askfloat("Payout", "Enter the payout amount:")
        if amount is not None:
            if amount <= self.account.payout_limit:
                confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to payout {amount} PLN?")
                if confirm:
                    if self.account.payout(amount):  # Aktualizacja stanu konta po wypłacie
                        messagebox.showinfo("Payout",
                                            f"The payment for the amount {amount} has been processed.\nYour current balance is {self.account.balance} PLN.")
                    else:
                        messagebox.showwarning("Insufficient Funds", "You don't have sufficient funds to payout.")
            else:
                messagebox.showwarning("Exceeded Payout Limit", f"The payout amount exceeds the payout limit of {self.account.payout_limit} PLN.")

    def check_balance(self):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to check your balance?")
        if confirm:
            messagebox.showinfo("Balance", f"Your current balance is {self.account.balance} PLN.")

    def transaction_history(self):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to view transaction history?")
        if confirm:
            history = "\n".join([f"{transaction['type']} of {transaction['amount']} PLN" for transaction in
                                 self.account.transaction_history])
            messagebox.showinfo("Transaction History", f"Transaction History:\n{history}")


