from datetime import datetime
import os
import re

def is_valid_account_number(account_number):
    return account_number.isdigit() and len(account_number) == 8

def is_valid_transaction_amount(amount):
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

class Account:
    def __init__(self, account_number, account_holder_name, initial_funds):
        # Initialize Account object with account number, account holder name, initial funds and transaction history
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.initial_funds = initial_funds
        self.current_funds = initial_funds
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.current_funds += amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transaction_history.append(f"Deposit: £{amount:,.2f} -- {timestamp} -- Current funds: £{self.current_funds:,.2f}")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.current_funds:
            self.current_funds -= amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transaction_history.append(f"Withdrawal: £{amount:,.2f} -- {timestamp} -- Current funds: £{self.current_funds:,.2f}")

    def get_account_details(self):
        # Format the balance with a pound sign (£) and comma separators for thousands within the f-string
        total_deposited = sum(float(d.split(': ')[1].split(' -- ')[0].replace('£', '').replace(',', '')) for d in self.transaction_history if d.startswith('Deposit'))
        total_withdrawn = sum(float(w.split(': ')[1].split(' -- ')[0].replace('£', '').replace(',', '')) for w in self.transaction_history if w.startswith('Withdrawal'))

        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder_name}\nInitial Funds: £{self.initial_funds:,.2f}\nCurrent Funds: £{self.current_funds:,.2f}\nTotal Deposited: £{total_deposited:,.2f}\nTotal Withdrawn: £{total_withdrawn:,.2f}"

    def save_transaction_history(self):
        # Save transaction history to a text file
        folder = "Transaction History"
        file_path = get_file_path(f"{self.account_number}_transaction_history.txt", folder)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create the folder if it doesn't exist
            with open(file_path, "w") as file:
                file.write("\n".join(self.transaction_history))
            return True
        except IOError:
            print("Error saving transaction history.")
            return False

class Bank:
    # Initialize Bank object with an empty list of accounts
    def __init__(self):
        self.accounts = []

    def create_account(self, account_number, first_name, last_name, initial_balance):
        initial_balance = round(float(initial_balance), 2)
        account_holder_name = f"{first_name} {last_name}"
        account = Account(account_number, account_holder_name, initial_balance)
        self.accounts.append(account)
        print("Account created successfully.")

    def perform_transaction(self, account_number, amount, transaction_type):
        # Perform a transaction (deposit/withdrawal) on an account
        account = self.find_account(account_number)
        if account is not None:
            if transaction_type == "deposit":
                account.deposit(amount)
            elif transaction_type == "withdrawal":
                account.withdraw(amount)

    def display_account_details(self, account_number):
        # Display account details
        account = self.find_account(account_number)
        if account is not None:
            return account.get_account_details()

    def generate_reports(self):
        # Generate reports for all accounts
        report = ""
        for account in self.accounts:
            report += account.get_account_details() + "\n"
        return report

    def find_account(self, account_number):
        # Find an account by account number
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

def get_file_path(filename, folder=""):
    # Get the file path of the specified file in the specified folder
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    return os.path.join(current_dir, folder, filename)

def load_data_from_file(file_path):
    # Load account data and transaction history from a text file
    accounts = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                account_data = line.strip().split(",")
                account_number = account_data[0]
                account_holder_name = account_data[1]
                balance = float(account_data[2])
                account = Account(account_number, account_holder_name, balance)
                accounts.append(account)

                # Load transaction history for the account
                transaction_file_path = get_file_path(f"{account_number}_transaction_history.txt", "Transaction History")
                if os.path.exists(transaction_file_path):
                    with open(transaction_file_path, "r") as transaction_file:
                        transaction_history = transaction_file.readlines()
                        account.transaction_history = [transaction.strip() for transaction in transaction_history]

                    # Update current_funds based on transaction history
                    for transaction in account.transaction_history:
                        match = re.search(r"£([\d,]+\.\d+)", transaction)
                        if match:
                            amount = float(match.group(1).replace(",", ""))
                            if transaction.startswith('Deposit'):
                                account.current_funds += amount
                            elif transaction.startswith('Withdrawal'):
                                account.current_funds -= amount

        print("Account data loaded successfully.")
    except FileNotFoundError:
        print("No account data file found.")
    return accounts

def save_data_to_file(accounts, file_path):
    # Save account data to a text file
    try:
        with open(file_path, "w") as file:
            for account in accounts:
                account_data = [
                    account.account_number,
                    account.account_holder_name,
                    str(account.initial_funds)
                ]
                file.write(",".join(account_data) + "\n")
        
        # Save transaction history for each account
        for account in accounts:
            account.save_transaction_history()
        
        print("Account data and transaction history saved successfully.")
    except IOError:
        print("Error saving account data.")

def display_menu():
    # Display menu options
    print("---- Bank Management System Menu ----")
    print("1. Create an account")
    print("2. Perform a transaction")
    print("3. Display account details")
    print("4. Generate reports")
    print("5. Exit")

def handle_user_input(option):
    # Handle user input and call appropriate methods
    if option == "1":
        account_number = input("Enter account number: ")
        while True:
            if not is_valid_account_number(account_number):
                print("Invalid account number. Account number should be 8 digits.")
                account_number = input("Enter account number: ")
                continue

            if bank.find_account(account_number) is not None:
                print("Account number already exists. Please choose a different account number.")
                account_number = input("Enter account number: ")
                continue
            break

        first_name = ""
        while not first_name.strip():
            first_name = input("Enter first name: ")
            if not first_name.strip():
                print("First name cannot be empty.")

        last_name = ""
        while not last_name.strip():
            last_name = input("Enter last name: ")
            if not last_name.strip():
                print("Last name cannot be empty.")

        while True:
            try:
                initial_balance = float(input("Enter initial balance: "))
                if initial_balance >= 0:
                    break
                else:
                    print("Invalid initial balance. Initial balance should be a positive number.")
            except ValueError:
                print("Invalid initial balance. Initial balance should be a valid number.")

        # Create an account with the provided input values
        bank.create_account(account_number, first_name, last_name, initial_balance)

    elif option == "2":
        account_number = input("Enter account number: ")
        while not is_valid_account_number(account_number):
            print("Invalid account number. Account number should be 8 digits.")
            account_number = input("Enter account number: ")

        account = bank.find_account(account_number)
        while account is None:
            print("Account not found. Please enter a valid account number.")
            account_number = input("Enter account number: ")
            account = bank.find_account(account_number)

        transaction_type = input("Enter transaction type (deposit/withdrawal): ").lower()
        while transaction_type not in ["deposit", "withdrawal"]:
            print("Invalid transaction type. Please enter either 'deposit' or 'withdrawal'.")
            transaction_type = input("Enter transaction type (deposit/withdrawal): ").lower()

        while True:
            try:
                amount = float(input("Enter transaction amount: "))
                if is_valid_transaction_amount(amount):
                    # Limit the number of decimal places to 2
                    amount = round(amount, 2)
                    break
                else:
                    print("Invalid amount. Amount should be a positive number.")
            except ValueError:
                print("Invalid amount. Amount should be a valid number.")

        if transaction_type == "deposit":
            account.deposit(amount)
            print(f"Success! £{amount:,.2f} deposited to: ")
        elif transaction_type == "withdrawal":
            if amount <= account.current_funds:
                account.withdraw(amount)
                print(f"Success! £{amount:,.2f} withdrawn from: ")
            else:
                print("Insufficient funds. Withdrawal amount exceeds the current balance.")

        # Display updated account details
        account_details = bank.display_account_details(account_number)
        print(account_details)

    elif option == "3":
        account_number = input("Enter account number: ")

        # Retrieve and display the account details
        account_details = bank.display_account_details(account_number)
        if account_details is not None:
            print(account_details)
        else:
            print("Account not found.")

    elif option == "4":
        # Generate and display reports for all accounts
        reports = bank.generate_reports()
        print(reports)

    elif option == "5":
        # Save account data and transaction history to files and exit the program
        save_data_to_file(bank.accounts, get_file_path("account_data.txt"))
        exit()

    else:
        print("Invalid option. Please try again.")

# Main program
if __name__ == "__main__":
    bank = Bank()
    file_path = get_file_path("account_data.txt")
    accounts = load_data_from_file(file_path)
    bank.accounts = accounts

    while True:
        display_menu()
        user_option = input("Enter your choice (1-5): ")
        handle_user_input(user_option)