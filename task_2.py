import time
import math
from datetime import datetime, timedelta

class BankDepositCalculator:
    def __init__(self, initial_deposit, annual_interest_rate):
        """
        Initialize the deposit calculator
        
        Args:
            initial_deposit: Initial amount of money
            annual_interest_rate: Annual interest rate as percentage (e.g., 7 for 7%)
        """
        self.initial_deposit = initial_deposit
        self.annual_rate = annual_interest_rate / 100.0
        
        # Calculate daily interest rate (assuming 365 days per year)
        self.daily_rate = self.annual_rate / 365.0
        
        # For exponential formula
        self.C = -math.log(1 + self.daily_rate)  # Constant for exponential formula
        
        # For the Knight's unstable method
        # A = 1 + daily_rate (compounded every 2 seconds)
        # But actually Knight was compounding too frequently!
        seconds_per_day = 24 * 3600
        self.A_2sec = 1 + self.daily_rate / (seconds_per_day / 2)
    
    def unstable_knight_method(self, duration_days):
        """
        The Knight's computationally unstable method - compounding every 2 seconds
        This accumulates floating-point errors
        
        Args:
            duration_days: Number of days to simulate
        
        Returns:
            Final amount and list of accumulated values
        """
        value = self.initial_deposit
        values = [value]
        
        seconds = int(duration_days * 24 * 3600)
        iterations = seconds // 2  # Every 2 seconds
        
        print(f"\nKnight's Unstable Method (compounding every 2 seconds for {duration_days} days)")
        print(f"Total iterations: {iterations:,}")
        
        for i in range(iterations):
            value = self.A_2sec * value
            if i % (iterations // min(10, iterations)) == 0 and i > 0:
                values.append(value)
        
        return value, values
    
    def stable_bank_method(self, duration_days):
        """
        Stable method: Calculate directly using compound interest formula
        Banks typically compound interest daily
        
        Args:
            duration_days: Number of days to simulate
        
        Returns:
            Final amount
        """
        # Standard compound interest formula: A = P(1 + r/n)^(nt)
        # For daily compounding: n = 365
        rate_per_day = self.annual_rate / 365.0
        final_amount = self.initial_deposit * ((1 + rate_per_day) ** duration_days)
        
        return final_amount
    
    def exponential_method(self, duration_days):
        """
        Alternative stable method using exponential formula
        y = B * exp(-C * t), where t is in days
        
        Args:
            duration_days: Number of days to simulate
        
        Returns:
            Final amount
        """
        # Actually, for growth we need: y = B * exp(C * t)
        # where C = ln(1 + daily_rate)
        C = math.log(1 + self.daily_rate)
        final_amount = self.initial_deposit * math.exp(C * duration_days)
        
        return final_amount
    
    def simulate_realistic_bank(self, start_date, end_date):
        """
        Simulate how a real bank would calculate interest
        - Interest typically compounds daily or monthly
        - Only at compounding periods does the interest get added
        
        Args:
            start_date: Start date as string 'YYYY-MM-DD'
            end_date: End date as string 'YYYY-MM-DD'
        
        Returns:
            Final amount and transaction log
        """
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        balance = self.initial_deposit
        daily_rate = self.annual_rate / 365.0
        transactions = []
        
        # Add initial transaction
        transactions.append((current_date.strftime('%Y-%m-%d'), 'Initial deposit', balance, balance))
        
        # Simulate daily compounding
        while current_date < end_date_obj:
            # Calculate daily interest
            daily_interest = balance * daily_rate
            
            # Add interest to balance (banks typically round to cents)
            balance += daily_interest
            balance = round(balance, 2)  # Round to nearest cent
            
            # Move to next day
            current_date += timedelta(days=1)
            
            # Record monthly statement (every 30 days for display)
            if current_date.day == 1 or (current_date - datetime.strptime(start_date, '%Y-%m-%d')).days % 30 == 0:
                transactions.append((current_date.strftime('%Y-%m-%d'), 'Daily interest', daily_interest, balance))
        
        return balance, transactions

def main():
    # Parameters
    initial_deposit = 1000.0  # $1000 initial deposit
    annual_rate = 7.0  # 7% annual interest
    
    calculator = BankDepositCalculator(initial_deposit, annual_rate)
    
    print("=" * 70)
    print("THE MISERLY KNIGHT'S DILEMMA")
    print("=" * 70)
    print(f"Initial deposit: ${initial_deposit:,.2f}")
    print(f"Annual interest rate: {annual_rate}%")
    print(f"Daily interest rate: {calculator.daily_rate * 100:.6f}%")
    
    # Test for different durations
    test_durations = [1, 7, 30, 365, 365*5]  # 1 day, 1 week, 1 month, 1 year, 5 years
    
    for days in test_durations:
        print(f"\n{'='*70}")
        print(f"RESULTS AFTER {days} DAYS ({days/365:.1f} years)")
        print(f"{'='*70}")
        
        # Knight's unstable method (only for shorter periods due to computational cost)
        if days <= 30:  # Only show for short periods
            knight_result, _ = calculator.unstable_knight_method(days)
            print(f"Knight's unstable method:       ${knight_result:,.6f}")
        
        # Stable bank method (daily compounding)
        stable_result = calculator.stable_bank_method(days)
        print(f"Stable bank method (daily):     ${stable_result:,.6f}")
        
        # Exponential method
        exp_result = calculator.exponential_method(days)
        print(f"Exponential method:             ${exp_result:,.6f}")
        
        # Compare differences
        if days <= 30:
            error = abs(knight_result - stable_result)
            error_pct = (error / stable_result) * 100
            print(f"Error in Knight's method:       ${error:.6f} ({error_pct:.6f}%)")
    
    # Show realistic bank simulation for 1 year
    print(f"\n{'='*70}")
    print("REALISTIC BANK SIMULATION (1 year with daily compounding)")
    print(f"{'='*70}")
    
    final_balance, transactions = calculator.simulate_realistic_bank('2024-01-01', '2025-01-01')
    
    print(f"\nInitial deposit: ${initial_deposit:,.2f}")
    print(f"Final balance after 1 year: ${final_balance:,.2f}")
    print(f"Total interest earned: ${final_balance - initial_deposit:,.2f}")
    
    # Show sample transactions (first few and last)
    print(f"\nSample transaction log:")
    print("-" * 60)
    print(f"{'Date':<12} {'Description':<20} {'Interest':<12} {'Balance':<12}")
    print("-" * 60)
    
    for i, (date, desc, interest, balance) in enumerate(transactions):
        if i < 3 or i >= len(transactions) - 3:  # Show first 3 and last 3
            interest_str = f"${interest:,.2f}" if desc != 'Initial deposit' else ""
            print(f"{date:<12} {desc:<20} {interest_str:<12} ${balance:,.2f}")
        elif i == 3:
            print("...")

if __name__ == "__main__":
    main()