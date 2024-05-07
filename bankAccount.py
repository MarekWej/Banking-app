import os.path
import pickle
from currency_exchange import get_exchange_rate

class BankAccount:
    def __init__(self, account_id, balance, owner, payout_limit, interest_rate=0.01, password=None):
        self.account_id = account_id
        self.balance = balance
        self.owner = owner
        self.transaction_history = []
        self.payout_limit = payout_limit
        self.interest_rate = interest_rate
        self.password = password

    @classmethod
    def load_account_data(cls, account_id, password):
        filename = f"{account_id}_account.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                data = pickle.load(file)
                if data['password'] == password:
                    return cls(account_id=data['account_id'], balance=data['balance'], owner=data['owner'],
                               payout_limit=data['payout_limit'], interest_rate=data['interest_rate'],
                               password=data['password'])
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
            'interest_rate': self.interest_rate,
            'password': self.password
        }
        with open(f"{self.account_id}_account.pkl", "wb") as file:
            pickle.dump(data, file)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            self.save_account_data()  # Save data after deposit
            return f'Value {amount} has been added to your bank account.\nYour current balance is {self.balance} PLN.'
        else:
            return f"Sorry, we cannot add this value: {amount} to your account."

    def payout(self, amount):
        if 0 < amount <= self.balance:
            if amount <= self.payout_limit:
                self.balance -= amount
                self.add_transaction("Payout", amount)
                self.save_account_data()  # Save the data after payment
                return True
            else:
                return False
        else:
            return False

    def set_transactions_limit(self, amount):
        if amount >= 0:
            self.payout_limit = amount
            return f"The payout limit has been set to {amount} PLN."
        else:
            return "Invalid payout limit."

    def get_balance(self):
        return self.balance

    def add_transaction(self, transaction_type, amount):
        transaction = {"type": transaction_type, "amount": amount}
        self.transaction_history.append(transaction)

    def history_of_the_transactions(self):
        history = "\n".join([f"{transaction['type']} of {transaction['amount']} PLN" for transaction in self.transaction_history])
        return f"Transaction History:\n{history}"

    def calculate_and_add_interest(self, interest_rate):
        interest_amount = self.balance * interest_rate
        self.balance += interest_amount
        self.add_transaction("Interest rate", interest_amount)
        return f'Interest has been added to your account in the amount of {interest_amount} PLN.\nYour account balance is now {self.balance} PLN.'

    def calculate_and_process_payout(self, amount):
        if amount > 400:
            interest_rate = 0.02
        else:
            interest_rate = 0.01

        self.balance -= amount
        self.add_transaction("Payout", amount)
        self.calculate_and_add_interest(interest_rate)
        return f"Your {amount} PLN withdrawal has been processed.\nYour account balance is now {self.balance} PLN."

    def interest_transactions(self):
        interest_rate = 0.01
        return self.calculate_and_add_interest(interest_rate)

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

    def convert_balance(self, target_currency):
        base_currency = 'PLN'
        exchange_rate = get_exchange_rate(base_currency, target_currency)
        if exchange_rate:
            amount_to_convert = float(input(f"Enter the amount to convert to {target_currency}: "))
            converted_amount = amount_to_convert / exchange_rate
            return f"{amount_to_convert} PLN converted to {target_currency}: {converted_amount}"
        else:
            return "Conversion failed"



