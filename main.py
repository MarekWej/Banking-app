import tkinter as tk
from bank_account_GUI import BankAccountGUI


def main():
    root = tk.Tk()
    app = BankAccountGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
