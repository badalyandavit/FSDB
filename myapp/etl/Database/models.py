from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    ssn = Column(String(11), unique=True)
    address = Column(String(200))
    created_at = Column(Date)

    accounts = relationship("Account", back_populates="customer")


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    account_number = Column(String(20), unique=True)
    account_type = Column(String(20))  # e.g., checking, savings, investment
    balance = Column(Numeric(15, 2))
    opened_date = Column(Date)

    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Numeric(15, 2))
    transaction_type = Column(String(20))  # e.g., deposit, withdrawal, transfer
    date = Column(Date)
    description = Column(String(200))

    account = relationship("Account", back_populates="transactions")


class Security(Base):
    __tablename__ = 'securities'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True)
    name = Column(String(100))
    security_type = Column(String(50))  # e.g., stock, bond, etf
    price = Column(Numeric(15, 2))
    currency = Column(String(3))


def get_engine():
    from sqlalchemy import create_engine
    import os
    return create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)