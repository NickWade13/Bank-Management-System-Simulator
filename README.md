Bank Management System

This project is a Bank Management System that allows users to create accounts, perform transactions (deposits and withdrawals), transfer funds between accounts, and generate reports. The system provides a simple command-line interface for users to interact with.

Installation:

To install and run the project locally, follow these steps:

Make sure you have Python installed on your system. You can download Python from the official website: Python.org.

Download the project files and save them in a directory of your choice.

Open a terminal or command prompt and navigate to the directory where you saved the project files.

Run the following command to install the required dependencies:

pip install datetime

Once the dependencies are installed, you can run the project by executing the following command:

python bank_management_system.py

Usage:

After installing and running the project, you can use the following menu options to interact with the Bank Management System:

Create an account: This option allows you to create a new bank account. You will be prompted to enter an account number, first name, last name, and initial balance. Make sure to enter a valid 8-digit account number and a positive initial balance.

Perform a transaction: This option allows you to perform a transaction on an existing account. Enter the account number, transaction type (deposit or withdrawal), and transaction amount. The transaction amount should be a positive number. If the transaction is successful, the program will display the updated account details.

Transfer funds between accounts: This option allows you to transfer funds from one account to another. Enter the sender's account number, recipient's account number, and the transfer amount. Both account numbers should be valid 8-digit numbers, and the transfer amount should be a positive number. If the transfer is successful, the program will display the updated account details for both the sender and recipient.

Display account details: This option allows you to view the details of an account. Enter the account number, and the program will display the account holder's name, initial funds, current funds, total deposited amount, and total withdrawn amount.

Display transaction history: This option allows you to view the transaction history of an account. Enter the account number, and the program will display a list of transactions performed on the account, including the transaction type, amount, timestamp, and current funds after the transaction.

Generate reports: This option will display a report for each account, including the account holder's name, initial funds, current funds, total deposited amount, and total withdrawn amount.

Exit: This option allows you to exit the Bank Management System.

Note: The project uses the user's default locale for formatting currency amounts. The account details and transaction history are saved in text files within a "Transaction History" folder.

Feel free to explore the functionality of the Bank Management System and manage bank accounts efficiently!
