import pandas as pd
from loguru import logger
import random
from myapp.etl.Database.models import *
from myapp.etl.Database.database import engine, Base
from myapp.etl.Database.data_generator import (
    generate_employee,
    generate_customer,
    generate_account,
    generate_transaction,
    generate_loan,
    generate_risk_assessment
)
import glob
from os import path

NUMBER_OF_EMPLOYEES = 100
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_ACCOUNTS = 3000
NUMBER_OF_TRANSACTIONS = 5000
NUMBER_OF_LOANS = 500
NUMBER_OF_RISK_ASSESSMENTS = 1000


# Generate Employee Data
employees = pd.DataFrame(
    [generate_employee(employee_id) for employee_id in range(1, NUMBER_OF_EMPLOYEES + 1)]
)
logger.info("Employee Data")
logger.info(employees.head(1))
employees.to_csv("data/employees.csv", index=False)
logger.info(f"Employee data saved to CSV: {employees.shape}")

# Generate Customer Data
customers = pd.DataFrame(
    [generate_customer(customer_id) for customer_id in range(1, NUMBER_OF_CUSTOMERS + 1)]
)
logger.info("Customer Data")
logger.info(customers.head(1))
customers.to_csv("data/customers.csv", index=False)
logger.info(f"Customer data saved to CSV: {customers.shape}")

# Generate Account Data
accounts = pd.DataFrame(
    [generate_account(account_id, random.randint(1, NUMBER_OF_CUSTOMERS)) for account_id in
     range(1, NUMBER_OF_ACCOUNTS + 1)]
)
logger.info("Account Data")
logger.info(accounts.head(1))
accounts.to_csv("data/accounts.csv", index=False)
logger.info(f"Account data saved to CSV: {accounts.shape}")

# Generate Transaction Data
transactions = []
for transaction_id in range(1, NUMBER_OF_TRANSACTIONS + 1):
    account_id = random.randint(1, NUMBER_OF_ACCOUNTS)
    transactions.append(generate_transaction(transaction_id, account_id))
transactions = pd.DataFrame(transactions)
logger.info("Transaction Data")
logger.info(transactions.head(1))
transactions.to_csv("data/transactions.csv", index=False)
logger.info(f"Transaction data saved to CSV: {transactions.shape}")

# Generate Loan Data
loans = pd.DataFrame(
    [generate_loan(loan_id, random.randint(1, NUMBER_OF_CUSTOMERS), random.randint(1, NUMBER_OF_EMPLOYEES))
     for loan_id in range(1, NUMBER_OF_LOANS + 1)]
)
logger.info("Loan Data")
logger.info(loans.head(1))
loans.to_csv("data/loans.csv", index=False)
logger.info(f"Loan data saved to CSV: {loans.shape}")

# Generate Risk Assessment Data
risk_assessments = pd.DataFrame(
    [generate_risk_assessment(risk_id, random.randint(1, NUMBER_OF_CUSTOMERS))
     for risk_id in range(1, NUMBER_OF_RISK_ASSESSMENTS + 1)]
)
logger.info("Risk Assessment Data")
logger.info(risk_assessments.head(1))
risk_assessments.to_csv("data/risk_assessments.csv", index=False)
logger.info(f"Risk Assessment data saved to CSV: {risk_assessments.shape}")


def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.

    Parameters:
        - table_name (str): The name of the database table.
        - csv_path (str): The path to the CSV file containing data.

    Returns:
        None
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Loading data into table: {table_name}")


# Get all CSV file paths in the data folder
folder_path = "data/*.csv"
files = glob.glob(folder_path)
base_names = [path.splitext(path.basename(file))[0] for file in files]

# Load data from CSV files into their respective tables
for table in base_names:
    try:
        load_csv_to_table(table, path.join("data", f"{table}.csv"))
    except Exception as e:
        logger.error(f"Failed to ingest table {table}. Error: {e}")
        print(f"Failed to ingest table {table}. Moving to the next!")

print("Tables are populated.")
