class BankAccount:

    def __init__(self, balance, owner, payout_limit):
        self.balance = balance
        self.owner = owner
        self.transaction_history = []
        self.payout_limit = payout_limit

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            print(f'Value {amount} has been added to your bank account, your funds in your account are {self.balance} ')
        else:
            print(f"Sorry sir, we cannot add this value: {amount} to your account")

    def payout(self, amount):
        if 0 < amount <= self.balance:
            if amount <= self.payout_limit:
                self.balance -= amount
                self.add_transaction("Payout", amount)
                print(
                    f"The payment for the amount {amount} has been processed, your funds in your account are {self.balance} ")
            else:
                print(f"The payout amount exceeds the limit of {self.payout_limit}")
        else:
            print("Payout must be higher than 0")

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


acc = BankAccount(balance=1000, owner="john", payout_limit=1000)
acc1 = BankAccount(balance=2000, owner="Sam", payout_limit=500)


acc.deposit(5)
acc.payout(900)
acc.deposit(2000)
acc.payout(2000)
print("Current balance:", acc.get_balance())
acc.history_of_the_transactions()
acc.payout(1100)
acc1.payout(400)
#