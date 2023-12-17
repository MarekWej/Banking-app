from bankAccount import BankAccount
from savingsBankAccount import SavingsAccount

acc = BankAccount(balance=1000, owner="john", payout_limit=1000)
acc1 = BankAccount(balance=2000, owner="Sam", payout_limit=500)

acc.deposit(5)
acc.payout(900)
acc.deposit(2000)
acc.payout(2000)
print("Current balance:", acc.get_balance())
acc.history_of_the_transactions()
acc.interest_transactions()
acc.payout(1100)
acc1.payout(400)

print("\nOperations on the savings account:")
savings_acc = SavingsAccount(balance=2000, owner="Alice", payout_limit=500, interest_rate=0.03, withdrawal_limit=2)
savings_acc.deposit(500)
savings_acc.payout(200)
savings_acc.payout(100)
savings_acc.payout(50)
savings_acc.payout(50)  # Exceeding the withdrawal limit
savings_acc.interest_transactions()
print("Current balance of the savings account:", savings_acc.get_balance())
savings_acc.history_of_the_transactions()