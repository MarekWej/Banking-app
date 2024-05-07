import tkinter as tk
from tkinter import simpledialog, messagebox
from bankAccount import BankAccount
from savingsBankAccount import SavingsAccount


class CurrencyConversionDialog(simpledialog.Dialog):
    def __init__(self, parent, currencies):
        self.currencies = currencies
        self.amount = None
        super().__init__(parent)

    def body(self, master):
        self.title("Currency Conversion")
        tk.Label(master, text="Choose the target currency:").grid(row=0, column=0, padx=10, pady=5)
        self.currency_var = tk.StringVar(master, value=self.currencies[0])
        self.currency_menu = tk.OptionMenu(master, self.currency_var, *self.currencies)
        self.currency_menu.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(master, text="Enter the amount:").grid(row=1, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(master)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)
        return self.amount_entry

    def validate(self):
        try:
            self.amount = float(self.amount_entry.get())
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return False

    def convert(self):
        if self.validate():  # Waliduj wprowadzoną wartość przed konwersją
            target_currency = self.currency_var.get()
            messagebox.showinfo("Currency Conversion",
                                f"{self.amount} PLN converted to {target_currency}: {self.amount}")
            self.destroy()  # Zamyka okno dialogowe po poprawnej konwersji


class BankAccountGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.account = None
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to the banking system!")
        self.label.pack()
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()
        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account)
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

        account_type = simpledialog.askstring("Create Account",
                                              "Do you want to create a Savings account? (yes/no):").lower()

        if account_type == "yes":
            interest_rate = float(
                simpledialog.askstring("Create Account", "Enter the interest rate for the Saving account:"))
            withdrawal_limit = int(
                simpledialog.askstring("Create Account", "Enter the withdrawal limit for the Savings Account:"))
            self.account = SavingsAccount(account_id, balance=initial_balance, owner=owner, payout_limit=payout_limit,
                                          interest_rate=interest_rate, withdrawal_limit=withdrawal_limit,
                                          password=password)
        else:
            self.account = BankAccount(account_id, balance=initial_balance, owner=owner, payout_limit=payout_limit,
                                       password=password)

        self.account.save_account_data()
        messagebox.showinfo("Success", "Account created successfully.")
        self.show_menu()

    def show_menu(self):
        self.label.pack_forget()
        self.login_button.pack_forget()
        self.create_account_button.pack_forget()

        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.payout_button = tk.Button(self.root, text="Payout", command=self.payout)
        self.payout_button.pack()

        self.check_balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack()

        self.transaction_history_button = tk.Button(self.root, text="Transaction History",
                                                    command=self.transaction_history)
        self.transaction_history_button.pack()

        self.currency_conversion_button = tk.Button(self.root, text="Currency Conversion",
                                                    command=self.currency_conversion)
        self.currency_conversion_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
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
            confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to payout {amount} PLN?")
            if confirm:
                if amount <= self.account.payout_limit:
                    if self.account.payout(amount):  # Aktualizacja stanu konta po wypłacie
                        messagebox.showinfo("Payout",
                                            f"The payment for the amount {amount} has been processed.\nYour current balance is {self.account.balance} PLN.")
                    else:
                        messagebox.showwarning("Insufficient Funds", "You don't have sufficient funds to payout.")
                else:
                    messagebox.showwarning("Exceeded Payout Limit",
                                           f"The payout amount {amount} PLN exceeds the limit of {self.account.payout_limit} PLN.")

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

    def currency_conversion(self):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to convert currency?")
        if confirm:
            currencies = ["USD", "EUR", "GBP", "AUD"]  # Lista dostępnych walut
            dialog = CurrencyConversionDialog(self.root, currencies)
            dialog.wait_window(dialog.top)  # Czekaj na zamknięcie okna dialogowego


root = tk.Tk()
app = BankAccountGUI(root)
root.mainloop()




