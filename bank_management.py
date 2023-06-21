from datetime import datetime
import locale
import os
import re

# Set the locale to the user's default locale
locale.setlocale(locale.LC_ALL, '')

def is_valid_account_number(account_number):
    # Check if the account number is valid (consists of 8 digits)
    return account_number.isdigit() and len(account_number) == 8

def is_valid_transaction_amount(amount):
    # Check if the transaction amount is valid (a positive number)
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

class Account:
    def __init__(self, account_number, account_holder_name, initial_funds):
        # Initialize Account object with account number, account holder name, initial funds and transaction histor
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.initial_funds = initial_funds
        self.current_funds = initial_funds
        self.transaction_history = []
        # Format the initial funds using the user's locale
        self.initial_funds_formatted = locale.currency(self.initial_funds, grouping=True, symbol=True)

    def deposit(self, amount):
        # Deposit the specified amount into the account
        if is_valid_transaction_amount(amount):
            self.current_funds += amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            deposit_amount_formatted = locale.currency(amount, grouping=True, symbol=True)
            current_funds_formatted = locale.currency(self.current_funds, grouping=True, symbol=True)
            self.transaction_history.append(
                f"Deposit: {deposit_amount_formatted} -- {timestamp} -- Current funds: {current_funds_formatted}")

    def withdraw(self, amount):
        # Withdraw the specified amount from the account if sufficient funds are available
        if is_valid_transaction_amount(amount) and amount <= self.current_funds:
            self.current_funds -= amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            withdrawal_amount_formatted = locale.currency(amount, grouping=True, symbol=True)
            current_funds_formatted = locale.currency(self.current_funds, grouping=True, symbol=True)
            self.transaction_history.append(
                f"Withdrawal: {withdrawal_amount_formatted} -- {timestamp} -- Current funds: {current_funds_formatted}")

    def get_account_details(self):
        # Get a formatted string with account details including initial funds, current funds, total deposited, and total withdrawn
        currency_symbol = locale.localeconv()['currency_symbol']  # Get the currency symbol based on the user's locale
        
        # Initialize variables to store the total deposited and total withdrawn amounts
        total_deposited = 0.0
        total_withdrawn = 0.0

        # Iterate through the transaction history
        for transaction in self.transaction_history:
            if transaction.startswith('Deposit'):
                # If the transaction is a deposit, extract the deposited amount and add it to the total deposited
                match = re.search(r"{0}([\d,]+\.\d+)".format(currency_symbol), transaction)
                if match:
                    amount = float(match.group(1).replace(",", ""))
                    total_deposited += amount
            elif transaction.startswith('Withdrawal'):
                # If the transaction is a withdrawal, extract the withdrawn amount and add it to the total withdrawn
                match = re.search(r"{0}([\d,]+\.\d+)".format(currency_symbol), transaction)
                if match:
                    amount = float(match.group(1).replace(",", ""))
                    total_withdrawn += amount

        # Format the initial funds, current funds, total deposited, and total withdrawn using the user's locale
        initial_funds_formatted = locale.currency(self.initial_funds, grouping=True, symbol=True)
        current_funds_formatted = locale.currency(self.current_funds, grouping=True, symbol=True)
        total_deposited_formatted = locale.currency(total_deposited, grouping=True, symbol=True)
        total_withdrawn_formatted = locale.currency(total_withdrawn, grouping=True, symbol=True)

        # Return a formatted string with the account details
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder_name}\nInitial Funds: {initial_funds_formatted}\nCurrent Funds: {current_funds_formatted}\nTotal Deposited: {total_deposited_formatted}\nTotal Withdrawn: {total_withdrawn_formatted}"

    def save_transaction_history(self):
        # Save transaction history to a text file
        folder = "Transaction History"  # Specify the folder to save the transaction history files
        
        # Generate the file path for the current account's transaction history file
        file_path = get_file_path(f"{self.account_number}_transaction_history.txt", folder)
        try:
            # Create the folder if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create the folder if it doesn't exist
            # Write the transaction history to the file
            with open(file_path, "w") as file:
                file.write("\n".join(self.transaction_history))
            return True
        except FileNotFoundError:
            print("File not found while saving transaction history.")
            return False
        except PermissionError:
            print("Permission denied while saving transaction history.")
            return False

class Bank:
    # Initialize Bank object with an empty list of accounts
    def __init__(self):
        self.accounts = []

    def create_account(self, account_number, first_name, last_name, initial_balance):
        # Create a new account and add it to the list of accounts
        initial_balance = round(float(initial_balance), 2)  # Round the initial balance to 2 decimal places
        account_holder_name = f"{first_name} {last_name}"
        account = Account(account_number, account_holder_name, initial_balance)
        self.accounts.append(account)  # Add the account to the list of accounts
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
                try:
                    with open(transaction_file_path, "r") as transaction_file:
                        transaction_history = transaction_file.readlines()
                        account.transaction_history = [transaction.strip() for transaction in transaction_history]

                    # Update current_funds based on transaction history
                    for transaction in account.transaction_history:
                        match = re.search(r"{0}([\d,]+\.\d+)".format(locale.localeconv()['currency_symbol']), transaction)
                        if match:
                            amount = float(match.group(1).replace(",", ""))
                            if transaction.startswith('Deposit'):
                                account.current_funds += amount
                            elif transaction.startswith('Withdrawal'):
                                account.current_funds -= amount
                except FileNotFoundError:
                    print(f"Transaction history file not found for account {account_number}.")
                except PermissionError:
                    print(f"Permission denied while loading transaction history for account {account_number}.")

        print("Account data loaded successfully.")
    except FileNotFoundError:
        print("No account data file found.")
    except PermissionError:
        print("Permission denied while loading account data.")
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
    print("3. Transfer funds between accounts")
    print("4. Display account details")
    print("5. Display transaction history")
    print("6. Generate reports")
    print("7. Exit")

def handle_user_input(option):
    # Handle user input and call appropriate methods
    if option == "1":
        # Prompt the user to enter an account number
        account_number = input("Enter account number: ")
        
        # Validate the account number format
        while True:
            if not is_valid_account_number(account_number):
                print("Invalid account number. Account number should be 8 digits.")
                account_number = input("Enter account number: ")
                continue

            # Check if the account number already exists in the bank        
            if bank.find_account(account_number) is not None:
                print("Account number already exists. Please choose a different account number.")
                account_number = input("Enter account number: ")
                continue
            break

        # Prompt the user to enter the first name        
        first_name = ""
        while not first_name.strip():
            first_name = input("Enter first name: ")
            if not first_name.strip():
                print("First name cannot be empty.")

        # Prompt the user to enter the last name
        last_name = ""
        while not last_name.strip():
            last_name = input("Enter last name: ")
            if not last_name.strip():
                print("Last name cannot be empty.")

        # Prompt the user to enter the initial balance
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
        # Prompt the user to enter an account number
        account_number = input("Enter account number: ")
        
        # Validate the account number format
        while not is_valid_account_number(account_number):
            print("Invalid account number. Account number should be 8 digits.")
            account_number = input("Enter account number: ")

        # Find the account with the provided account number
        account = bank.find_account(account_number)
        while account is None:
            print("Account not found. Please enter a valid account number.")
            account_number = input("Enter account number: ")
            account = bank.find_account(account_number)

        # Prompt the user to enter the transaction type (deposit/withdrawal)
        transaction_type = input("Enter transaction type (deposit/withdrawal): ").lower()
        while transaction_type not in ["deposit", "withdrawal"]:
            print("Invalid transaction type. Please enter either 'deposit' or 'withdrawal'.")
            transaction_type = input("Enter transaction type (deposit/withdrawal): ").lower()

        # Prompt the user to enter the transaction amount
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
            # Perform a deposit on the account
            account.deposit(amount)
            print(f"Success! {locale.currency(amount, grouping=True, symbol=True)} deposited to:")
            print(f"Account Number: {account.account_number}")
            print(f"Account Holder: {account.account_holder_name}")
            print(f"Current Funds: {locale.currency(account.current_funds, grouping=True, symbol=True)}")

        elif transaction_type == "withdrawal":
            # Perform a withdrawal from the account
            if amount <= account.current_funds:
                account.withdraw(amount)
                print(f"Success! {locale.currency(amount, grouping=True, symbol=True)} withdrawn from:")
                print(f"Account Number: {account.account_number}")
                print(f"Account Holder: {account.account_holder_name}")
                print(f"Current Funds: {locale.currency(account.current_funds, grouping=True, symbol=True)}")
            else:
                print("Insufficient funds. Withdrawal amount exceeds the current balance.")

    elif option == "3":
        # Prompt the user to enter the sender's account number
        while True:
            sender_account_number = input("Enter sender account number: ")
            if is_valid_account_number(sender_account_number):
                # Find the sender's account with the provided account number
                sender_account = bank.find_account(sender_account_number)
                if sender_account is not None:
                    break
                else:
                    print("Sender account not found. Please enter a valid account number.")
            else:
                print("Invalid account number. Please try again.")

        # Prompt the user to enter the recipient's account number
        while True:
            recipient_account_number = input("Enter recipient account number: ")
            if is_valid_account_number(recipient_account_number):
                # Find the recipient's account with the provided account number
                recipient_account = bank.find_account(recipient_account_number)
                if recipient_account is not None:
                    break
                else:
                    print("Recipient account not found. Please enter a valid account number.")
            else:
                print("Invalid account number. Please try again.")

        # Prompt the user to enter the transfer amount
        while True:
            while True:
                try:
                    amount = float(input("Enter transfer amount: "))
                    if is_valid_transaction_amount(amount):
                        # Limit the number of decimal places to 2
                        amount = round(amount, 2)
                        break
                    else:
                        print("Invalid amount. Amount should be a positive number.")
                except ValueError:
                    print("Invalid amount. Amount should be a valid number.")

            if amount <= sender_account.current_funds:
                # Perform the transfer by withdrawing from the sender's account and depositing to the recipient's account
                sender_account.withdraw(amount)
                recipient_account.deposit(amount)
                print(f"Success! {locale.currency(amount, grouping=True, symbol=True)} transferred from:")
                print(f"Sender Account Number: {sender_account.account_number}")
                print(f"Sender Account Holder: {sender_account.account_holder_name}")
                print(f"To:")
                print(f"Recipient Account Number: {recipient_account.account_number}")
                print(f"Recipient Account Holder: {recipient_account.account_holder_name}")
                break
            else:
                print("Insufficient funds. Transfer amount exceeds the current balance of the sender account.")

    elif option == "4":
        # Prompt the user to enter an account number
        while True:
            account_number = input("Enter account number: ")
            if is_valid_account_number(account_number):
                # Retrieve and display the account details with the provided account number
                account_details = bank.display_account_details(account_number)
                print(account_details)
                break
            else:
                print("Invalid account number. Please try again.")

    elif option == "5":
        # Prompt the user to enter an account number
        while True:
            account_number = input("Enter account number: ")
            if is_valid_account_number(account_number):
                # Find the account with the provided account number
                account = bank.find_account(account_number)
                if account is not None:
                    print("\nTransaction History:")
                    # Display each transaction in the account's transaction history
                    for transaction in account.transaction_history:
                        print(transaction)
                    break
                else:
                    print("Account not found. Please enter a valid account number.")
            else:
                print("Invalid account number. Please try again.")

    elif option == "6":
        # Generate and display reports for all accounts
        reports = bank.generate_reports()
        print(reports)

    elif option == "7":
        # Save account data and transaction history to files and exit the program
        save_data_to_file(bank.accounts, get_file_path("account_data.txt"))
        exit()

    else:
        print("Invalid option. Please try again.")

# Main program
if __name__ == "__main__":
    # Create a Bank object
    bank = Bank()
    # Load the account data from a file
    file_path = get_file_path("account_data.txt")
    accounts = load_data_from_file(file_path)
    bank.accounts = accounts

    while True:
        # Display the menu
        display_menu()
        option = input("Enter your choice (1-7): ")
        handle_user_input(option)