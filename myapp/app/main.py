import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Connect to the database using the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)

# Load the loans data from the database
try:
    loans_df = pd.read_sql("SELECT * FROM loans", engine)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

if loans_df.empty:
    raise HTTPException(status_code=500, detail="No loans data found. Please run the ETL process first.")

# For demonstration, use interest_rate and term_years to predict loan_amount
X = loans_df[["interest_rate", "term_years"]].values
y = loans_df["loan_amount"].values
model = LinearRegression().fit(X, y)

class LoanPredictionRequest(BaseModel):
    interest_rate: float
    term_years: int

@app.post("/predict_loan_amount")
def predict_loan_amount(request: LoanPredictionRequest):
    features = np.array([[request.interest_rate, request.term_years]])
    prediction = model.predict(features)
    return {"predicted_loan_amount": prediction[0]}
