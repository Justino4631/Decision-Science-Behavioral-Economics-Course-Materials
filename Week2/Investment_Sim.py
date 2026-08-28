"""
This is a simple investment simulation illustrating risk vs reward in real life.
Users are able to invest a certain amount of money into three investments: S&P 500, Bonds, and MSCIEF.
Data is taken based on each of these returns over the last 30 years (shown in the CSV file) to shape
how their investments evolve over time.

author: Justin Baratta
date: 5/30/2026
version: 3.14
"""

import pandas as pd
import matplotlib.pyplot as plt
import random as r
import time

INITIAL_MONEY = 10_000.0
investment_SP = 0.0
investment_Bonds = 0.0
investment_MSCIEF = 0.0

EXPECTED_RATES = {
    "SP500": 0.1193,
    "Bonds": 0.0341,
    "MSCIEF": 0.1041,
    "Cash": 0.0
}

with open("./Week2/hist_annual_returns.csv") as file:
    df = pd.read_csv(file)

historical_returns = {
    "SP500": df["SP500"].tolist(),
    "Bonds": df["Bonds"].tolist(),
    "MSCIEF": df["MSCIEF"].tolist()
}

def welcome() -> None:
    message = """
Welcome to your Week 2 Simulation! This simulation illustrates real-life risk management by simulating the returns of three different investments: the S&P 500, Bonds, and the MSCI Emerging Markets Index Fund (MSCIEF).\n
You will start with $10,000 and can choose how to allocate your money among these three investments. Each investment has its own historical returns, which will be randomly sampled to simulate the performance of your portfolio over time. Here are some basic returns and risks with each investment:\n
The average return of the S&P 500 is 11.93% per year. It is usually a good long-term investment but can be susceptible to huge gains or losses in the short term.
The average return of Bonds is 3.41% per year. Bonds almost always have a positive return and are considered much more stable, however their returns are significantly lower than the S&P 500.
The average return of MSCIEF is 10.41% per year. While it's average annual return is high, it can be even more volatile than the S&P 500, with almost half of all returns being negative. The highest return can be 79.02% and the lowest return can be -53.18%.\n
At the start of the simulation, you can distribute your money however you want among these three investments (you can even choose to not invest some funds). Each time step represents one year. After each year, the returns of your investments will be calculated based on the historical returns, and your total portfolio value will be updated. You can choose to adjust your investments at the end of each year or keep them the same.
YOU WILL ONLY BE ABLE TO REALLOCATE FUNDS ONCE.\n
Have fun and consider risk vs reward!
"""

    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.02)
    return

def get_valid_float(prompt: str, max_allowed: float) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Invalid input: Investment amounts cannot be negative. Try again.")
                continue
            if val > max_allowed:
                print(f"Invalid input: You only have ${max_allowed:.2f} available to allocate. Try again.")
                continue
            return val
        except ValueError:
            print("Invalid input: Please enter a valid numerical dollar amount.")

def allocate_funds() -> None:
    global INITIAL_MONEY, investment_SP, investment_Bonds, investment_MSCIEF
    remaining = INITIAL_MONEY
    print(f"\nTotal available funds to allocate: ${remaining:.2f}")

    investment_SP = get_valid_float("Amount to invest in S&P 500: $", remaining)
    remaining -= investment_SP

    print(f"Remaining funds: ${remaining:.2f}")
    investment_Bonds = get_valid_float("Amount to invest in Bonds: $", remaining)
    remaining -= investment_Bonds

    print(f"Remaining funds: ${remaining:.2f}")
    investment_MSCIEF = get_valid_float("Amount to invest in MSCIEF: $", remaining)
    remaining -= investment_MSCIEF

    print(f"Uninvested cash remaining in portfolio: ${remaining:.2f}")

def calculate_expected_value(sp: float, bonds: float, mscief: float, cash: float) -> float:
    expected_sp = sp * (1 + EXPECTED_RATES["SP500"])
    expected_bonds = bonds * (1 + EXPECTED_RATES["Bonds"])
    expected_mscief = mscief * (1 + EXPECTED_RATES["MSCIEF"])
    expected_cash = cash * (1 + EXPECTED_RATES["Cash"])
    return expected_sp + expected_bonds + expected_mscief + expected_cash

def play_out_year() -> tuple[float, float, float]:
    global INITIAL_MONEY, investment_SP, investment_Bonds, investment_MSCIEF
    return_SP = r.choice(historical_returns["SP500"])
    return_Bonds = r.choice(historical_returns["Bonds"])
    return_MSCIEF = r.choice(historical_returns["MSCIEF"])

    investment_SP *= (1 + return_SP / 100)
    investment_Bonds *= (1 + return_Bonds / 100)
    investment_MSCIEF *= (1 + return_MSCIEF / 100)
    
    return return_SP, return_Bonds, return_MSCIEF

if __name__ == "__main__":
    if (input("Do you want to see the intro (y/n): ")).strip().lower() == "y":
        welcome()
    
    allocate_funds()
    reallocate_used = False
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    years = []
    sp_history = []
    bonds_history = []
    mscief_history = []
    cash_history = []
    
    total_simulation_years = 10
    current_year = 1
    
    portfolio_starting_value = INITIAL_MONEY
    
    while current_year <= total_simulation_years:
        print(f"\n--- Running Year {current_year} ---")
        
        current_cash = max(0.0, INITIAL_MONEY - (investment_SP + investment_Bonds + investment_MSCIEF))

        expected_portfolio_val = calculate_expected_value(investment_SP, investment_Bonds, investment_MSCIEF, current_cash)

        pct_SP, pct_Bonds, pct_MSCIEF = play_out_year()
        
        INITIAL_MONEY = investment_SP + investment_Bonds + investment_MSCIEF + current_cash
        
        years.append(current_year)
        sp_history.append(investment_SP)
        bonds_history.append(investment_Bonds)
        mscief_history.append(investment_MSCIEF)
        cash_history.append(current_cash)
        
        ax.clear()
        ax.plot(years, sp_history, color='red', marker='o', linestyle='-', label='S&P 500')
        ax.plot(years, bonds_history, color='green', marker='o', linestyle='-', label='Bonds')
        ax.plot(years, mscief_history, color='blue', marker='o', linestyle='-', label='MSCIEF')
        ax.plot(years, cash_history, color='gray', marker='o', linestyle='--', label='Uninvested Cash')
        
        ax.set_xlabel('Timeline (Years)')
        ax.set_ylabel('Portfolio Value ($)')
        ax.set_title('Asset Allocation Growth Over Time')
        ax.set_xticks(range(1, total_simulation_years + 1))
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        fig.savefig('./Week2/portfolio_growth.png', bbox_inches='tight')

        total_pct_change = ((INITIAL_MONEY - portfolio_starting_value) / portfolio_starting_value) * 100
        
        print(f"Year {current_year} Closing Financial Summary:")
        print(f"Expected Portfolio Value: ${expected_portfolio_val:.2f}")
        print(f"Actual S&P 500 Value:    ${investment_SP:.2f} ({pct_SP:+.0f}%)")
        print(f"Actual Bonds Value:      ${investment_Bonds:.2f} ({pct_Bonds:+.0f}%)")
        print(f"Actual MSCIEF Value:     ${investment_MSCIEF:.2f} ({pct_MSCIEF:+.0f}%)")
        print(f"Uninvested Cash Pool:    ${current_cash:.2f} (+0%)")
        print(f"Actual Portfolio Total:  ${INITIAL_MONEY:.2f} ({total_pct_change:+.0f}% overall)")
        
        if not reallocate_used and current_year < total_simulation_years:
            choice = input("\nWould you like to use your ONE-TIME reallocation allowance right now? (yes/no): ").strip().lower()
            if choice in ["yes", "y"]:
                investment_SP = 0.0
                investment_Bonds = 0.0
                investment_MSCIEF = 0.0
                allocate_funds()
                reallocate_used = True
                
        current_year += 1
        time.sleep(1)
        
    print("\n" + "="*40)
    print("SIMULATION ENDED")
    print(f"Final Account Yield Balance: ${INITIAL_MONEY:.2f}")
    print("="*40)