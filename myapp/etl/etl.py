import os
import pandas as pd
from sqlalchemy import create_engine
from Database.models import Base, Customer, Account, Transaction, Security


def load_data():
    engine = create_engine(os.getenv('DATABASE_URL'))
    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load customers
    customers = pd.read_csv('./data/customers.csv')
    for _, row in customers.iterrows():
        session.add(Customer(**row.to_dict()))

    # Load accounts
    accounts = pd.read_csv('./data/accounts.csv')
    for _, row in accounts.iterrows():
        session.add(Account(**row.to_dict()))

    # Load transactions
    transactions = pd.read_csv('./data/transactions.csv')
    for _, row in transactions.iterrows():
        session.add(Transaction(**row.to_dict()))

    # Load securities
    securities = pd.read_csv('./data/securities.csv')
    for _, row in securities.iterrows():
        session.add(Security(**row.to_dict()))

    session.commit()
    session.close()


load_data()
