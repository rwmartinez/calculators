from dataclasses import dataclass

LOAN_TERM_YEARS = 30


@dataclass
class MortgageCalculationResult:
    mortgage_payment: float
    pmi: float
    monthly_tax: float
    hoa_fee: float
    total_monthly_payment: float
    principal_interest_schedule: list[tuple[float, float]]

def calculate_monthly_mortgage(
    down_payment: float, 
    home_price: float, 
    interest_rate: float,
    hoa_fee: float=0.0, 
    tax_rate: float=0.9,
) -> MortgageCalculationResult:
    # Calculate loan amount (home price - down payment)
    loan_amount = home_price - down_payment
    
    # Monthly interest rate
    monthly_interest_rate = interest_rate / 100 / 12
    
    # Total number of payments (loan term in years * 12 months)
    number_of_payments = LOAN_TERM_YEARS * 12
    
    # Mortgage payment calculation using the formula.
    # https://www.rocketmortgage.com/learn/how-to-calculate-mortgage
    if monthly_interest_rate > 0:
        mortgage_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    else:
        mortgage_payment = loan_amount / number_of_payments
    
    # Calculate PMI (Private Mortgage Insurance) if the down payment is less than 20% of home price
    pmi = 0
    if down_payment < 0.2 * home_price:
        pmi = loan_amount * (0.6 / 100) / 12
    
    # Calculate property taxes (annual property tax rate / 12)
    monthly_tax = (home_price * (tax_rate / 100)) / 12
    
    # Total monthly payment includes mortgage, PMI, taxes, and HOA fee
    total_monthly_payment = mortgage_payment + pmi + monthly_tax + hoa_fee

    # Calculate principal and interest breakdown for each month
    balance = loan_amount
    principal_interest_schedule = []
    
    for _ in range(number_of_payments):
        interest_payment = balance * monthly_interest_rate
        principal_payment = mortgage_payment - interest_payment
        balance -= principal_payment
        principal_interest_schedule.append((principal_payment, interest_payment))
    
    
    return MortgageCalculationResult(
        total_monthly_payment=total_monthly_payment,
        pmi=pmi,
        monthly_tax=monthly_tax,
        hoa_fee=hoa_fee,
        mortgage_payment=mortgage_payment,
        principal_interest_schedule=principal_interest_schedule,
    )