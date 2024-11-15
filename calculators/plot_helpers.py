import streamlit as st
import matplotlib.pyplot as plt

from calculators.mortgage_calculator import (
    MortgageCalculationResult,
)

# Pie Chart of Monthly Payment Components
def plot_monthly_payment_pie(result: MortgageCalculationResult):
    labels = ['Mortgage Payment', 'Monthly Tax']
    sizes = [result.mortgage_payment, result.monthly_tax]

    if result.hoa_fee > 0.0:
        labels.append("HOA Fee")
        sizes.append(result.hoa_fee)
    if result.pmi > 0.0:
        labels.append("PMI")
        sizes.append(result.pmi)
    
    # Create label strings with actual values for legend
    legend_labels = [f"{label}: ${size:,.2f}" for label, size in zip(labels, sizes)]

    # Plot the pie chart
    fig, ax = plt.subplots()
    wedges, _, _ = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    
    # Customize the legend
    ax.legend(wedges, legend_labels, title="Components", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Ensure pie is drawn as a circle and display it
    ax.axis('equal')
    st.pyplot(fig)

# Line Chart of Principal vs Interest Payments Over Time
def plot_principal_interest_schedule(result: MortgageCalculationResult):
    months = list(range(1, len(result.principal_interest_schedule) + 1))
    principal_payments = [p[0] for p in result.principal_interest_schedule]
    interest_payments = [p[1] for p in result.principal_interest_schedule]
    
    fig, ax = plt.subplots()
    ax.plot(months, principal_payments, label="Principal Payment")
    ax.plot(months, interest_payments, label="Interest Payment")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Monthly Principal vs Interest Payment Over Time")
    ax.legend()
    st.pyplot(fig)