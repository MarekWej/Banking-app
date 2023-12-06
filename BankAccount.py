class BankAccount:

    def __init__(self, balance, owner):
        self.balance = balance
        self.owner = owner
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.add_transaction("Deposit", amount)
            print(f'Value {amount} has been added to your bank account, your funds in your account are {self.balance} ')
        else:
            print(f"Sorry sir, we cannot add this value: {amount} to your account")

    def payout(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.add_transaction("Payout", amount)
            print(
                f"The payment for the amount {amount} has been processed, your funds in your account are {self.balance} ")
        else:
            print("Payout must be higher than 0")

    def get_balance(self):
        return self.balance

    def add_transaction(self, transaction_type, amount):
        transaction = {"type": transaction_type, "amount": amount}
        self.transaction_history.append(transaction)

    def history_of_the_transactions(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(f"{transaction['type']} of {transaction['amount']}")


acc = BankAccount(balance=1000, owner="john")

acc.deposit(5)
acc.payout(20)
acc.deposit(2000)
acc.payout(2000)
print("Current balance:", acc.get_balance())
acc.history_of_the_transactions()