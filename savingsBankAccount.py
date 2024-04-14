from bankAccount import BankAccount

class SavingsAccount(BankAccount):

    def __init__(self, balance, owner, payout_limit, interest_rate=0.02, withdrawal_limit=3, password=None):
        super().__init__(balance, owner, payout_limit, interest_rate, password)
        self.withdrawal_limit = withdrawal_limit
        self.withdrawal_count = 0

    def payout(self, amount):
        if self.withdrawal_count < self.withdrawal_limit:
            super().payout(amount)
            self.withdrawal_count += 1
        else:
            print(f"You have exceeded the withdrawal limit for your savings account ({self.withdrawal_limit}).")

    def add_transaction(self, transaction_type, amount):
        super().add_transaction(transaction_type, amount)


