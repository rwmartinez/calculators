import streamlit as st
import numpy as np

from calculators.mortgage_calculator import (
    calculate_monthly_mortgage,
    MortgageCalculationResult,
)
from calculators.plot_helpers import (
    plot_monthly_payment_pie,
    plot_principal_interest_schedule,
)

# Initialize session_state for the toggle flag and inputs
if 'show_calculation' not in st.session_state:
    st.session_state.show_calculation = False

# Function to reset the boolean to False when any number input is changed
def reset_toggle_on_input_change():
    if (
        st.session_state.down_payment != st.session_state.get('previous_down_payment', st.session_state.down_payment) or
        st.session_state.home_price != st.session_state.get('previous_home_price', st.session_state.home_price) or
        st.session_state.hoa_fee != st.session_state.get('previous_hoa_fee', st.session_state.hoa_fee) or
        st.session_state.interest_rate != st.session_state.get('previous_interest_rate', st.session_state.interest_rate) or
        st.session_state.tax_rate != st.session_state.get('previous_tax_rate', st.session_state.tax_rate)
    ):
        st.session_state.show_calculation = False  # Reset the toggle to False if inputs change

    # Update the previous values in session_state for future comparisons
    st.session_state.previous_down_payment = st.session_state.down_payment
    st.session_state.previous_home_price = st.session_state.home_price
    st.session_state.previous_hoa_fee = st.session_state.hoa_fee
    st.session_state.previous_interest_rate = st.session_state.interest_rate
    st.session_state.previous_tax_rate = st.session_state.tax_rate

# Set up the sidebar for user input
st.sidebar.header("Mortgage Calculator")

# Collect user inputs
down_payment = st.sidebar.number_input("Down Payment ($)", min_value=0.0, step=1000.0, key="down_payment")
home_price = st.sidebar.number_input("Home Price ($)", min_value=0.0, step=1000.0, key="home_price")
hoa_fee = st.sidebar.number_input("HOA Fee ($/mo.)", min_value=0.0, step=50.0, key="hoa_fee")
interest_rate = st.sidebar.number_input("Interest Rate (%/yr.)", min_value=0.0, step=0.1, key="interest_rate")
tax_rate = st.sidebar.number_input("Property Tax Rate (%/yr.)", min_value=0.0, step=0.1, key="tax_rate")

if st.sidebar.button("Calculate"):
    st.session_state.show_calculation = True

# Reset the toggle state when any number input changes
reset_toggle_on_input_change()

# Conditionally show content based on the toggle
if st.session_state.show_calculation:
    if all([down_payment > 0.0, home_price >= 0.0, interest_rate > 0]):
        mortgage_calculation: MortgageCalculationResult = calculate_monthly_mortgage(
            down_payment=down_payment,
            home_price=home_price,
            hoa_fee=hoa_fee,
            interest_rate=interest_rate,
            tax_rate=tax_rate,
        )

        st.write(f"# Total Monthly Payment: ${mortgage_calculation.total_monthly_payment:.2f}")
        st.write("### Monthly Payment Components")
        plot_monthly_payment_pie(mortgage_calculation)
        st.write("### Principal vs Interest Payment Over Time")
        plot_principal_interest_schedule(mortgage_calculation)

    else:
        st.write("Please enter valid loan details to calculate the monthly payment.")
else:
    st.write("Enter the loan details in the sidebar and press 'Calculate' to see the monthly payment.")
