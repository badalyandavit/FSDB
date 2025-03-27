import streamlit as st
import requests

st.title("Loan Amount Predictor")

interest_rate = st.number_input("Enter interest rate (e.g., 0.05 for 5%):", value=0.05, step=0.01, format="%.2f")
term_years = st.number_input("Enter term in years:", value=10, step=1)

if st.button("Predict Loan Amount"):
    # Use the service name 'fastapi_app' as the hostname in Docker Compose
    response = requests.post("http://fastapi_app/predict_loan_amount", json={"interest_rate": interest_rate, "term_years": int(term_years)})
    if response.ok:
        result = response.json()
        st.write("Predicted loan amount is:", result["predicted_loan_amount"])
    else:
        st.error("Failed to get prediction. Status code: " + str(response.status_code))
