# project1.py
# Furkan Karabulut (fkarabu)
# Class: CSC 205-002
# Date: 2/11/2024

import rate_dict as rd
import table_header as th

import math;

# constant values for the loan term
TEN_YEARS = 10;
FIFTEEN_YEARS = 15;
TWENTY_YEARS = 20;
THIRTY_YEARS = 30;

# constant values for LTV
EIGHTY_PERCENT = 80;
EIGHTY_FIVE_PERCENT = 85;
NINETY_PERCENT = 90;
NINETY_FIVE_PERCENT = 95;
HUNDRED_PERCENT = 100;

# Constant value for Percentage calculator
HUNDRENT = 100;

# Constant value for PMI Rate
PMI_RATE_95 = 1.030;
PMI_RATE_90_95 = 0.875;
PMI_RATE_85_90 = 0.675;
PMI_RATE_80_85 = 0.375;

# Constant value for year
YEAR = 12;



'''
    First of all write the loan calculator function
    This function will take the loan amount, the term and the rate as input
    - The loan amount (P) or principal is the amount of money you borrow
    - The annual interest rate (r) not APR
    - The number of years (t) as a term
    - The number of payments per year (n) is 12
    
    
    Payment = P * (r/n) * (1 + r/n)^(n*t) / ((1 + r/n)^(n*t) - 1)
    
    example::
    Suppose you borrow $100,000 at 6% for 30 years, to be repaid monthly.
    {100,000 x (.06 / 12) x [1 + (.06 / 12)^12(30)]} / {[1 + (.06 / 12)^12(30)] - 1}
    
'''
def loan_calculator (p, r, t, n):
    payment = p * (r/n) * (1 + r/n)**(n*t) / ((1 + r/n)**(n*t) - 1)
    return round(payment, 2);
    
    
# THat will print the loan information that is getting key and it is going to return
#  the loan type and the interest rate
def output_loan_info(loan_type_key):
    # print(f'inside output_loan_info function {loan_type_key}')
    interest_rate = rd.rates[loan_type_key]
    print(f'Loan type: {loan_type_key} at {interest_rate:.3f}% APR')

def loan_details (rd, loan_term, LTV):
    if LTV <= EIGHTY_PERCENT and loan_term == TEN_YEARS:
        loan_type = "10-Year Fixed, 80% or less LTV";
    elif LTV > EIGHTY_PERCENT and LTV <= 90 and loan_term == TEN_YEARS:
        loan_type = "10-Year Fixed, 80.1-90% LTV";
    elif LTV > 90 and LTV <= 100 and loan_term == TEN_YEARS:
        loan_type = "10-Year Fixed, 90.1-100% LTV";
    elif LTV <= 90 and loan_term == FIFTEEN_YEARS:
        loan_type = "15-Year Fixed, 90% or less LTV";
    elif LTV > 90 and LTV <= 100 and loan_term == FIFTEEN_YEARS:
        loan_type = "15-Year Fixed, 90.1-100% LTV";
    elif LTV <= 90 and loan_term == TWENTY_YEARS:
        loan_type = "20-Year Fixed, 90% or less LTV";
    elif LTV > 90 and LTV <= 100 and loan_term == TWENTY_YEARS:
        loan_type = "20-Year Fixed, 90.1-100% LTV";
    elif LTV <= 90 and loan_term == THIRTY_YEARS:
        loan_type = "30-Year Fixed, 90% or less LTV";
    elif LTV > 90 and LTV <= 100 and loan_term == THIRTY_YEARS:
        loan_type = "30-Year Fixed, 90.1-100% LTV";
        
    if loan_type in rd:
        interest_rate = rd[loan_type];
        return loan_type, interest_rate;


'''
LTV Range of Initial Loan Annual PMI Rate
95% < LTV <= 100% 1.030%
90% < LTV <= 95% 0.875%
85% < LTV <= 90% 0.675%
80% < LTV <= 85% 0.375%
LTV <= 80% 0.000%
'''
# That will return the PMI rate
# This function is passed the purchase price and down payment percentage
# it will return PMI Payment
def get_PMI(purchase_price, down_payment):
    LTV = (purchase_price - down_payment) / purchase_price * HUNDRENT;
    monthly_PMI = 0;
    if LTV > NINETY_FIVE_PERCENT:
        PMI = PMI_RATE_95 / HUNDRENT;
    elif LTV > NINETY_PERCENT and LTV <= NINETY_FIVE_PERCENT:
        PMI = PMI_RATE_90_95 / HUNDRENT;
    elif LTV > EIGHTY_FIVE_PERCENT and LTV <= 90:
        PMI = PMI_RATE_85_90 / HUNDRENT;
    elif LTV > EIGHTY_PERCENT and LTV <= EIGHTY_FIVE_PERCENT:
        PMI = PMI_RATE_80_85 / HUNDRENT;
    else:
        PMI = 0.000;
    
    monthly_PMI = round(((purchase_price - down_payment) * PMI / YEAR), 2);
    return monthly_PMI;

# This function will print the amortization table
# It will take the principal, annual rate, years, payments per year and monthly PMI as input
# It will calculate the monthly rate and monthly payment
# It will calculate the current balance, total interest and total principal
# It will calculate the interest payment and principal payment
# It will calculate the total interest and total principal
# It will calculate the monthly PMI
# It will print the payment number, interest payment, principal payment, current balance and monthly PMI
# It will stop PMI payments once LTV < EIGHTY_PERCENT%
def print_amortization_table(principal, annual_rate, years, payments_per_year, purchase_price, down_payment):
    monthly_rate = annual_rate / 12
    monthly_payment = loan_calculator(principal, annual_rate, years, payments_per_year)
    
    
    monthly_PMI = get_PMI(purchase_price, down_payment)
    
    current_balance = principal
    total_interest = 0
    total_PMI = 0
    
    

    for payment_number in range(1, years * payments_per_year + 1):
        interest_payment = current_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        principal_payment = round(principal_payment, 2);
        current_balance -= principal_payment
        current_balance = round(current_balance, 2)


        current_LTV = (current_balance / purchase_price) * HUNDRENT
        
        total_PMI += monthly_PMI;
        
        
            
        if current_balance < 0:
            principal_payment += current_balance  # Adjust last principal payment
            current_balance = 0
        
        
        
        
        total_interest += interest_payment
        
               
        
        print(f"{payment_number:>4d} {interest_payment:>16,.2f} {principal_payment:>18,.2f} {current_balance:>21,.2f} {monthly_PMI:>15,.2f}")
        if current_LTV <= EIGHTY_PERCENT:
            monthly_PMI = 0;

        if current_balance <= 0:
            break  # Exit loop when balance is paid off

    print('==============================================================================');
    print();
    print('Mortgage Summary');
    print(f"{'Total interest paid:'} ${total_interest:>56,.2f}")
    print(f"{'Total payment to principal:':} ${principal:>49,.2f}")
    print(f"{'Total PMI paid:'} ${total_PMI:>61,.2f}")
    print(f"{'Total payments:'} ${total_interest + principal + total_PMI:>61,.2f}")
    print();

# That is the main function
# It will call the loan_calculator function the make_table_header function the output_loan_info function the get_PMI function
# It will also call the make_table_footer function. 
# It will prompt the user toenter the purchase price, the down payment abd tern of the laon in years which will be 
# 10, 15, 20 or 30 years.
def main():
    house_price = float(input("Enter the purchase price of your home: $"))
    loan_term = int(input("Enter the term of the loan in years: "))
    while loan_term not in [TEN_YEARS, FIFTEEN_YEARS, TWENTY_YEARS, THIRTY_YEARS]:
        loan_term = int(input("Enter the term of the loan in years again (10, 15, 20, 30): "))
    
    down_payment_percentage = float(input("Enter the down payment percentage: "))
    while down_payment_percentage < 0 or down_payment_percentage > HUNDRENT:
        down_payment_percentage = float(input("Enter the down payment percentage again: "))
    
    down_payment = house_price * down_payment_percentage / HUNDRENT;
    loan_amount = house_price - down_payment;
    
    print();
    print(f'Loan amount: ${loan_amount:,.2f}')
    
    LTV = loan_amount / house_price * HUNDRENT;
    # print(f'Loan to Value Ratio: {LTV:.2f}%')  
    
    loan_detail_str, interest_rate = loan_details(rd.rates, loan_term, LTV)
    loan_detail_str = "" + loan_detail_str;
    
    # print the loan information   
    output_loan_info(loan_detail_str);
    interest_rate = interest_rate / HUNDRENT;   
    montly_payment = round(loan_calculator(loan_amount, interest_rate, loan_term, YEAR), 2);
    print(f'Monthly Payment: ${montly_payment:.2f}')
    
    # Now using table_header.py to print the table header
    th.make_table_header();
    print(f'   0 {loan_amount:>57,.2f}');
    
    
    # Now using print_amortization_table to print the amortization table
    print_amortization_table(loan_amount, interest_rate, loan_term, YEAR, house_price, down_payment);
    
    
    
    
if __name__ == "__main__":
    main();