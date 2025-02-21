from faker import Faker
import pandas as pd
import random
import logging
import os
from loguru import logger
from datetime import datetime

fake = Faker()


def generate_employee(employee_id):
    """
    Generate an employee record for roles in financial services.
    """
    roles = ["Loan Officer", "Risk Manager", "Financial Advisor", "Customer Service"]
    return {
        "employee_id": employee_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "role": random.choice(roles),
        "salary": random.randint(50000, 150000)
    }

def generate_customer(customer_id):
    """
    Generate a customer record with financial attributes.
    """
    employment_status = random.choice(["Employed", "Self-Employed", "Unemployed", "Retired"])
    credit_score = random.randint(300, 850)
    annual_income = random.randint(20000, 200000)
    return {
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "address": fake.street_address(),
        "city": fake.city(),
        "zip_code": fake.zipcode(),
        "employment_status": employment_status,
        "credit_score": credit_score,
        "annual_income": annual_income
    }

def generate_account(account_id, customer_id):
    """
    Generate a bank account record.
    For Loan accounts, the balance is represented as a negative value.
    """
    account_types = ["Checking", "Savings", "Credit", "Loan"]
    account_type = random.choice(account_types)
    if account_type == "Loan":
        balance = -round(random.uniform(1000.0, 50000.0), 2)
    else:
        balance = round(random.uniform(0.0, 20000.0), 2)
    open_date = fake.date_between(start_date='-10y', end_date='today')
    return {
        "account_id": account_id,
        "customer_id": customer_id,
        "account_type": account_type,
        "balance": balance,
        "open_date": open_date
    }

def generate_transaction(transaction_id, account_id):
    """
    Generate a transaction record for an account.
    """
    transaction_types = ["Deposit", "Withdrawal", "Payment", "Transfer", "Purchase"]
    transaction_type = random.choice(transaction_types)
    amount = round(random.uniform(10.0, 10000.0), 2)
    transaction_date = fake.date_time_between(start_date='-5y', end_date='now')
    return {
        "transaction_id": transaction_id,
        "account_id": account_id,
        "transaction_date": transaction_date,
        "transaction_type": transaction_type,
        "amount": amount,
        "description": fake.sentence()
    }

def generate_loan(loan_id, customer_id, employee_id):
    """
    Generate a loan record that includes risk indicators and default status.
    """
    loan_amount = round(random.uniform(5000.0, 500000.0), 2)
    interest_rate = round(random.uniform(0.03, 0.2), 4)
    term_years = random.choice([5, 10, 15, 30])
    default_probability = round(random.uniform(0.0, 1.0), 2)
    # Mark as defaulted if the default probability is high
    defaulted = True if default_probability > 0.8 else False
    risk_rating = random.choice(["Low", "Medium", "High"])
    issue_date = fake.date_between(start_date='-5y', end_date='today')
    return {
        "loan_id": loan_id,
        "customer_id": customer_id,
        "employee_id": employee_id,  # Officer handling the loan
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "term_years": term_years,
        "default_probability": default_probability,
        "defaulted": defaulted,
        "risk_rating": risk_rating,
        "issue_date": issue_date
    }

def generate_risk_assessment(risk_id, customer_id):
    """
    Generate a risk assessment record for a customer.
    """
    assessment_date = fake.date_time_between(start_date='-2y', end_date='now')
    credit_score = random.randint(300, 850)
    risk_rating = random.choice(["Low", "Medium", "High"])
    recommendation = random.choice(["Approve", "Review", "Decline"])
    return {
        "risk_id": risk_id,
        "customer_id": customer_id,
        "assessment_date": assessment_date,
        "credit_score": credit_score,
        "risk_rating": risk_rating,
        "recommendation": recommendation
    }
