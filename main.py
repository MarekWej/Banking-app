from bankAccount import BankAccount
from savingsBankAccount import SavingsAccount

def create_account():
    print("Creating a new account:")
    account_id = input("Enter your account ID: ")
    owner = input("Enter your name: ")
    initial_balance = float(input("Enter the initial balance: "))
    payout_limit = float(input("Enter the payout limit: "))
    password = str(input("Set a password for your account: "))

    account_type = input("Do you want to create a Savings account? (yes/no): ".lower())

    if account_type == "yes":
        interest_rate = float(input("Enter the interest rate for the Saving account: "))
        withdrawal_limit = int(input("Enter the withdrawal limit for the Savings Account: "))
        new_account = SavingsAccount(account_id, balance=initial_balance, owner=owner, payout_limit=payout_limit,
                                                   interest_rate=interest_rate, withdrawal_limit=withdrawal_limit,
                                                   password=password)
    else:
        new_account = BankAccount(account_id, balance=initial_balance, owner=owner, payout_limit=payout_limit, password=password)
    # Save your account details to a pickle file
    new_account.save_account_data()

    print("Account created successfully.")
    return new_account

def login():
    print("Login to your account:")
    account_id = input("Enter your account ID: ")
    password = input("Enter your password: ")

    account = BankAccount(account_id, balance=0, owner="", payout_limit=0, password="")
    account.load_account_data()

    if account.password == password:
        print("Login successful!")
        return account
    else:
        print("Invalid password.")
        return None

def main():
    print("Welcome to the banking system!")

    while True:
        user_choice = input("Do you have an account? (yes/no): ").lower()

        if user_choice == "yes":
            account = login()
            if account:
                break
        elif user_choice == "no":
            account = create_account()
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

    while True:
        print("\nMenu:")
        print("1. Deposit")
        print("2. Payout")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Currency conversion")
        print("6. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            amount = float(input("Enter the deposit amount: "))
            account.deposit(amount)
            print("Current balance: {}".format(account.get_balance()))

        elif choice == "2":
            amount = float(input("Enter the payout amount: "))
            account.payout(amount)
            print("Current balance: {}".format(account.get_balance()))

        elif choice == "3":
            print("Current balance: {}".format(account.get_balance()))

        elif choice == "4":
            account.history_of_the_transactions()

        elif choice == "5":
            target_currency = input("Enter the target currency (e.g., USD, EUR): ").upper()
            if account.balance > 0:
                account.convert_balance(target_currency)
            else:
                print("You don't have sufficient funds to convert.")

        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5")

if __name__ == "__main__":
    main()