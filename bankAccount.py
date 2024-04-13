import os.path

from currency_exchange import get_exchange_rate
import pickle


class BankAccount:

    def __init__(self, account_id, balance, owner, payout_limit, interest_rate=0.01, password=None):
        self.account_id = account_id
        self.balance = balance
        self.owner = owner
        self.transaction_history = []
        self.payout_limit = payout_limit
        self.interest_rate = interest_rate
        self.password = password


    # Method to save account data to file
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

    # Method for loading account information from a file
    def load_account_data(self):
        if os.path.exists(f"{self.account_id}_account.pkl"):
            with open(f"{self.account_id}_account.pkl", "rb") as file:
                data = pickle.load(file)
                self.account_id = data['account_id']
                self.balance = data['balance']
                self.owner = data['owner']
                self.transaction_history = data['transaction_history']
                self.payout_limit = data['payout_limit']
                self.interest_rate = data['interest_rate']
                self.password = data['password']

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            self.save_account_data()  # Save data after deposit
            print(f'Value {amount} has been added to your bank account, your funds in your account are {self.balance} ')
        else:
            print(f"Sorry sir, we cannot add this value: {amount} to your account")

    def payout(self, amount):
        if 0 < amount <= self.balance:
            if amount <= self.payout_limit:
                self.balance -= amount
                self.add_transaction("Payout", amount)
                self.save_account_data()  # Save the data after payment
                print(
                    f"The payment for the amount {amount} has been processed, your funds in your account are {self.balance} ")
            else:
                print(f"The payout amount exceeds the limit of {self.payout_limit}")
        else:
            print("Insufficient funds for the requested payout")

    def set_transactions_limit(self, amount):
        if amount >= 0:
            self.payout_limit = amount
            print(f"The payout limit has been set to {amount}")
        else:
            print("Invalid payout limit")

    def get_balance(self):
        return self.balance

    def add_transaction(self, transaction_type, amount):
        transaction = {"type": transaction_type, "amount": amount}
        self.transaction_history.append(transaction)

    def history_of_the_transactions(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(f"{transaction['type']} of {transaction['amount']}")

    def calculate_and_add_interest(self, interest_rate):
        interest_amount = self.balance * interest_rate
        self.balance += interest_amount
        self.add_transaction("Interest rate", interest_amount)
        print(f'Interest has been added to your account in the amount of {interest_amount}. '
              f'Your account balance is now {self.balance} ')

    def calculate_and_process_payout(self, amount):
        if amount > 400:
            interest_rate = 0.02
        else:
            interest_rate = 0.01

        self.balance -= amount
        self.add_transaction("Payout", amount)
        self.calculate_and_add_interest(interest_rate)
        print(f"Your {amount} withdrawal has been processed. Your account balance is now {self.balance}.")

    def interest_transactions(self):
        print("Interest calculation:")
        interest_rate = 0.01
        self.calculate_and_add_interest(interest_rate)

    def authenticate(self, entered_password):
        if self.password is not None and entered_password == str(self.password):
            print("Authentication successful.")
            return True
        else:
            print("Wrong password")
            return False

    def account_access_by_password(self):
        entered_password = input("Please enter here your password: ")
        if self.authenticate(entered_password):
            print("Access granted")
            return True
        else:
            print("Account access blocked")

    def convert_balance(self, target_currency):
        base_currency = 'PLN'
        exchange_rate = get_exchange_rate(base_currency, target_currency)
        if exchange_rate:
            amount_to_convert = float(input(f"Enter the amount to convert to {target_currency}: "))
            converted_amount = amount_to_convert / exchange_rate
            print(f"{amount_to_convert} PLN converted to {target_currency}: {converted_amount}")
            return converted_amount
        else:
            print("Conversion failed")
            return None
