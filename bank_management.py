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
    # Load account data and transaction history from file
    pass


def save_data_to_file():
    # Save account data and transaction history to file
    pass


def display_menu():
    # Display menu options
    pass


def handle_user_input(option):
    # Handle user input and call appropriate methods
    pass


# Main program
if __name__ == "__main__":
    # Load data from file
    # Display menu
    # Handle user input
    # Save data to file