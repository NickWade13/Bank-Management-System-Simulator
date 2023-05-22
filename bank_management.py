import os

class Account:
    def __init__(self, account_number, account_holder_name, balance=0.0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposit: {amount}")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal: {amount}")

    def get_account_details(self):
        return f"Account Number: {self.account_number}\nAccount Holder: {self.account_holder_name}\nBalance: {self.balance}"

class Bank:
    def __init__(self):
        self.accounts = []

    def create_account(self, account_number, first_name, last_name, initial_balance):
        # Check if account number is valid
        if not account_number.isdigit() or len(account_number) != 8:
            print("Invalid account number. Account number should be 8 digits.")
            return

        # Check if first name and last name are provided
        if not first_name.strip() or not last_name.strip():
            print("Invalid name. First name and last name cannot be empty.")
            return

        # Check if initial balance is a positive number
        try:
            initial_balance = float(initial_balance)
            if initial_balance < 0:
                print("Invalid initial balance. Initial balance should be a non-negative number.")
                return
        except ValueError:
            print("Invalid initial balance. Initial balance should be a valid number.")
            return

        # Store initial balance with two decimal places
        initial_balance = round(initial_balance, 2)

        # Create the account
        account_holder_name = f"{first_name} {last_name}"
        account = Account(account_number, account_holder_name, initial_balance)
        self.accounts.append(account)

        print("Account created successfully.")

    def perform_transaction(self, account_number, amount, transaction_type):
        account = self.find_account(account_number)
        if account is not None:
            if transaction_type == "deposit":
                account.deposit(amount)
            elif transaction_type == "withdrawal":
                account.withdraw(amount)

    def display_account_details(self, account_number):
        account = self.find_account(account_number)
        if account is not None:
            return account.get_account_details()

    def generate_reports(self):
        report = ""
        for account in self.accounts:
            report += account.get_account_details() + "\n"
        return report

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

def get_file_path():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    return os.path.join(current_dir, "account_data.txt")

def load_data_from_file():
    accounts = []
    file_path = get_file_path()
    try:
        with open(file_path, "r") as file:
            for line in file:
                account_data = line.strip().split(",")
                account_number = account_data[0]
                account_holder_name = account_data[1]
                balance = float(account_data[2])
                transaction_history = account_data[3:]
                account = Account(account_number, account_holder_name, balance)
                account.transaction_history = transaction_history
                accounts.append(account)
        print("Account data loaded successfully.")
    except FileNotFoundError:
        print("No account data file found.")
    return accounts


def save_data_to_file(accounts):
    file_path = get_file_path()
    try:
        with open(file_path, "w") as file:
            for account in accounts:
                account_data = [
                    account.account_number,
                    account.account_holder_name,
                    str(account.balance),
                ]
                transaction_history = ",".join(account.transaction_history)
                account_data.append(transaction_history)
                line = ",".join(account_data)
                file.write(line + "\n")
        print("Account data saved successfully.")
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file_path))
        save_data_to_file(accounts)


def display_menu():
    print("---- Bank Management System Menu ----")
    print("1. Create an account")
    print("2. Perform a transaction")
    print("3. Display account details")
    print("4. Generate reports")
    print("5. Exit")


def handle_user_input(option):
    if option == "1":
        while True:
            account_number = input("Enter account number: ")
            if account_number.isdigit() and len(account_number) == 8:
                break
            else:
                print("Invalid account number. Account number should be 8 digits.")
        
        while True:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            if first_name.strip() and last_name.strip():
                break
            else:
                print("Invalid name. First name and last name cannot be empty.")
        
        while True:
            try:
                initial_balance = float(input("Enter initial balance: "))
                if initial_balance >= 0:
                    break
                else:
                    print("Invalid initial balance. Initial balance should be a non-negative number.")
            except ValueError:
                print("Invalid initial balance. Initial balance should be a valid number.")
                
        bank.create_account(account_number, first_name, last_name, initial_balance)

    elif option == "2":
        account_number = input("Enter account number: ")
        while True:
            try:
                amount = float(input("Enter transaction amount: "))
                if amount > 0:
                    break
                else:
                    print("Invalid transaction amount. It should be a positive number.")
            except ValueError:
                print("Invalid transaction amount. It should be a valid number.")
        transaction_type = input("Enter transaction type (deposit/withdrawal): ")
        bank.perform_transaction(account_number, amount, transaction_type)
    elif option == "3":
        account_number = input("Enter account number: ")
        account_details = bank.display_account_details(account_number)
        if account_details is not None:
            print(account_details)
        else:
            print("Account not found.")
    elif option == "4":
        reports = bank.generate_reports()
        print(reports)
    elif option == "5":
        save_data_to_file(bank.accounts)
        exit()
    else:
        print("Invalid option. Please try again.")


# Main program
if __name__ == "__main__":
    bank = Bank()
    accounts = load_data_from_file()
    bank.accounts = accounts

    while True:
        display_menu()
        user_option = input("Enter your choice (1-5): ")
        handle_user_input(user_option)
