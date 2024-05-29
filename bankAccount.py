import os.path
import pickle

class BankAccount:
    def __init__(self, account_id, balance, owner, payout_limit, password=None):
        self.account_id = account_id
        self.balance = balance
        self.owner = owner
        self.transaction_history = []
        self.payout_limit = payout_limit
        self.password = password

    @classmethod
    def load_account_data(cls, account_id, password):
        filename = f"{account_id}_account.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                data = pickle.load(file)
                if data['password'] == password:
                    account = cls(account_id=data['account_id'], balance=data['balance'], owner=data['owner'],
                                  payout_limit=data['payout_limit'], password=data['password'])
                    account.transaction_history = data.get('transaction_history', [])  # Dodaj historię transakcji
                    return account
                else:
                    return None
        else:
            return None

    def save_account_data(self):
        data = {
            'account_id': self.account_id,
            'balance': self.balance,
            'owner': self.owner,
            'transaction_history': self.transaction_history,
            'payout_limit': self.payout_limit,
            'password': self.password
        }
        try:
            with open(f"{self.account_id}_account.pkl", "wb") as file:
                pickle.dump(data, file)
        except Exception as e:
            print("Error occurred while saving account data:", e)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            self.save_account_data()
            return f'Value {amount} has been added to your bank account.\nYour current balance is {self.balance:.2f} PLN.'
        else:
            return f"Sorry, we cannot add this value: {amount} to your account."

    def payout(self, amount):
        if amount <= 0:
            return "Invalid payout amount. The amount must be positive."
        if amount > self.balance:
            return "Insufficient funds. You don't have enough money for this payout."
        elif amount > self.payout_limit:
            return f"Exceeded payout limit. Your payout limit is {self.payout_limit:.2f} PLN."
        else:
            self.balance -= amount
            self.add_transaction("Payout", amount)
            self.save_account_data()
            return True

    def set_transactions_limit(self, amount):
        if amount >= 0:
            self.payout_limit = amount
            self.save_account_data()
            return f"The payout limit has been set to {amount} PLN."
        else:
            return "Invalid payout limit. It must be a non-negative value."

    def get_balance(self):
        return f"{self.balance:.2f}"

    def add_transaction(self, transaction_type, amount):
        transaction = {"type": transaction_type, "amount": amount}
        self.transaction_history.append(transaction)

    def history_of_the_transactions(self):
        history = "\n".join(
            [f"{transaction['type']} of {transaction['amount']} PLN" for transaction in self.transaction_history])
        return f"Transaction History:\n{history}"

    def authenticate(self, entered_password):
        if self.password is not None and entered_password == str(self.password):
            return "Authentication successful."
        else:
            return "Wrong password"

    def account_access_by_password(self):
        entered_password = input("Please enter your password: ")
        if self.authenticate(entered_password):
            return "Access granted"
        else:
            return "Account access blocked"

    def change_password(self, old_password, new_password):
        if old_password != self.password:
            return "Old password is incorrect."
        elif new_password == self.password:
            return "New password cannot be the same as the old password."
        else:
            self.password = new_password
            self.save_account_data()
            return "Password changed successfully."
