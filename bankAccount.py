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
                    account.transaction_history = data.get('transaction_history', [])
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
            return f'Value {amount} has been added to your account.\nYour current balance is {self.balance:.2f} PLN.'
        else:
            return 'Deposit amount must be positive.'

    def payout(self, amount):
        if amount <= 0:
            return "The payout amount must be positive."
        if amount > self.balance:
            return "You don't have sufficient funds to payout."
        if amount > self.payout_limit:
            return f"The amount exceeds your payout limit of {self.payout_limit} PLN."
        self.balance -= amount
        self.add_transaction("Payout", amount)
        self.save_account_data()
        return True

    def get_balance(self):
        return f'{self.balance:.2f}'

    def add_transaction(self, transaction_type, amount):
        self.transaction_history.append({"type": transaction_type, "amount": amount})

    def change_password(self, old_password, new_password):
        if self.password == old_password:
            if self.password == new_password:
                return "New password cannot be the same as the old password."
            self.password = new_password
            self.save_account_data()
            return "Password changed successfully."
        else:
            return "Current password is incorrect."

