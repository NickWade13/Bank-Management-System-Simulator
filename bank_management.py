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

    def create_account(self, account_number, account_holder_name, initial_balance):
        account = Account(account_number, account_holder_name, initial_balance)
        self.accounts.append(account)

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

def load_data_from_file():
    accounts = []
    try:
        with open("account_data.txt", "r") as file:
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
    with open("account_data.txt", "w") as file:
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


def display_menu():
    print("---- Bank Management System Menu ----")
    print("1. Create an account")
    print("2. Perform a transaction")
    print("3. Display account details")
    print("4. Generate reports")
    print("5. Exit")


def handle_user_input(option):
    if option == "1":
        account_number = input("Enter account number: ")
        account_holder_name = input("Enter account holder name: ")
        initial_balance = float(input("Enter initial balance: "))
        bank.create_account(account_number, account_holder_name, initial_balance)
        print("Account created successfully.")
    elif option == "2":
        account_number = input("Enter account number: ")
        amount = float(input("Enter transaction amount: "))
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
