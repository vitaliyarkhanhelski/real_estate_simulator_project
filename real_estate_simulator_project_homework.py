#!/usr/bin/env python3
"""
Real estate rent vs buy simulator

You can edit the global parameters at the top of the file.
"""

from dataclasses import dataclass
from typing import List
import math

# Global simulation parameters
PRICE = 500_000.0            # price of property - cena nieruchomości
INITIAL_CAPITAL = 100_000.0  # initial savings/capital - początkowy kapitał, can't be less than DOWN_PAYMENT
DOWN_PAYMENT = PRICE * 0.2   # down payment amount (from initial capital) - wkład własny
MORTGAGE_RATE = 0.07         # annual mortgage rate (7%) - oprocentowanie kredytu w skali roku
MORTGAGE_TERM_YEARS = 30     # mortgage term in years - okres kredytu w latach
RENT_MONTHLY = 2600.0        # initial monthly rent - początkowa miesięczna wynajem
RENT_ANNUAL_INCREASE = 0.05  # 5% annual rent increase - roczny wzrost wynajmu
PROPERTY_ANNUAL_APPRECIATION = 0.05  # 5% property value increase per year - roczny wzrost wartości nieruchomości
MAINTENANCE_ANNUAL_PCT = 0.015  # 1.5% annual maintenance - roczny koszt utrzymania nieruchomości
INVESTMENT_ANNUAL_RETURN = 0.04  # 4% annual return on investments - roczny zwrot z lokaty
ADMIN_MONTHLY_BUY = 1000.0   # monthly admin/condo fees for owner - miesięczne koszty administracyjne dla właściciela
MONTHLY_SALARY = 10_000.0    # monthly salary - miesięczna pensja netto
LIVING_COST = 4_000.0        # monthly living costs (food, utilities, etc.) - miesięczne koszty życia

# Calculated constants (derived from parameters above)
"""mortgage amount - kwota główna pożyczki, pierwotna suma pieniędzy, którą pożyczasz od banku — bez odsetek. 
Od tej kwoty naliczane są odsetki w trakcie spłaty kredytu.
"""
BUYER_PRINCIPAL = max(0.0, PRICE - DOWN_PAYMENT)  

@dataclass
class SimulationResult:
    years: int
    buyer_net_worth: float
    renter_net_worth: float
    buyer_details: dict
    renter_details: dict

def monthly_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate fixed monthly mortgage payment using annuity formula.
    principal - kwota główna pożyczki
    annual_rate - roczne oprocentowanie
    years - okres kredytu w latach"""
    if principal <= 0:
        return 0.0
    if annual_rate == 0:
        return principal / (years * 12)
    r = annual_rate / 12.0
    n = years * 12
    payment = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return payment

def is_new_year(month: int) -> bool:
    """Return True if it's the first month of a new year (excluding month 1)."""
    return (month - 1) % 12 == 0 and month != 1


# Calculate the monthly mortgage payment once at module initialization
MONTHLY_MORTGAGE_PAYMENT = monthly_mortgage_payment(BUYER_PRINCIPAL, MORTGAGE_RATE, MORTGAGE_TERM_YEARS)

def simulate(years: int) -> SimulationResult:
    """Run month-by-month simulation for buyer and renter using global parameters."""
    months = years * 12
    
    # setup kupującego
    buyer_investment = max(0.0, INITIAL_CAPITAL - DOWN_PAYMENT) # ile pieniędzy kupujący inwestuje po wpłaceniu wkładu własnego
    remaining_mortgage = BUYER_PRINCIPAL # pozostała kwota kredytu
    property_value = PRICE # wartość nieruchomości
    current_monthly_payment = MONTHLY_MORTGAGE_PAYMENT  # miesięczna rata kredytu - wartość stała

    # setup najemcy
    renter_investment = INITIAL_CAPITAL # ile pieniędzy najemca inwestuje
    current_rent = RENT_MONTHLY # miesięczny wynajem

    monthly_return = (1 + INVESTMENT_ANNUAL_RETURN) ** (1/12) - 1 # miesięczna stopa zwrotu przeliczona z rocznej (z uwzględnieniem kapitalizacji)

    buyer_paid_interest = 0.0 # suma płaconych odsetek
    buyer_paid_principal = 0.0 # suma płaconych kapitałów
    renter_total_paid_rent = 0.0 # suma płaconych wynajmów
    buyer_total_paid = 0.0 # suma płaconych rat kredytu

    for month in range(1, months + 1):
        # Apply yearly changes at the start of each year (month 1,13,25,...)
        if is_new_year(month):
            property_value *= (1 + PROPERTY_ANNUAL_APPRECIATION) # roczna aprecjacja nieruchomości
            current_rent *= (1 + RENT_ANNUAL_INCREASE) # roczny wzrost wynajmu

        # BUYER monthly maintenance = annual maintenance pct of current property value / 12
        monthly_maintenance = property_value * MAINTENANCE_ANNUAL_PCT / 12.0 # miesięczny koszt utrzymania nieruchomości

        # Mortgage interest for this month
        monthly_interest = remaining_mortgage * (MORTGAGE_RATE / 12.0) # odsetkowa część miesięcznej raty kredytu
        principal_component = 0.0 # część miesięcznej raty przeznaczona na spłatę kapitału
        payment = 0.0 # miesięczna rata kredytu

        """Spłata kredytu w systemie amortyzacji polega na tym, że w pierwszych latach kredytu płaci się więcej odsetek, 
        a w kolejnych latach płaci się coraz mniej odsetek i coraz więcej kapitału.
        """
        if remaining_mortgage > 0:
            payment = min(current_monthly_payment, remaining_mortgage + monthly_interest) # rzeczywista miesięczna płatność (nie większa niż pozostały dług + odsetki)
            principal_component = payment - monthly_interest # część miesięcznej raty przeznaczona na spłatę kapitału
            remaining_mortgage = max(0.0, remaining_mortgage - principal_component) # aktualizacja pozostałego kapitału kredytu po spłacie
            buyer_paid_interest += monthly_interest  # dodanie miesięcznych odsetek do całkowitej kwoty zapłaconych odsetek przez kupującego - suma spłaconych odsetek
            buyer_paid_principal += principal_component # dodanie spłaconego kapitału do całkowitej kwoty spłaconego kapitału przez kupującego - suma spłaconego kapitału
            buyer_total_paid += payment + monthly_maintenance + ADMIN_MONTHLY_BUY # suma całkowitych miesięcznych kosztów kupującego (rata + utrzymanie nieruchomości + opłaty administracyjne)

        # RENTER monthly outflow = current_rent
        renter_total_paid_rent += current_rent # dodanie miesięcznego czynszu do całkowitych kosztów poniesionych przez wynajmującego

        # Calculate monthly surplus (what's left after all expenses)
        # RENTER: salary - living costs - rent
        monthly_surplus_renter = MONTHLY_SALARY - LIVING_COST - current_rent  # kwota, która zostaje wynajmującemu po pokryciu kosztów życia i czynszu
        
        # BUYER: salary - living costs - mortgage payment - maintenance - admin fees
        monthly_surplus_buyer = MONTHLY_SALARY - LIVING_COST - payment - monthly_maintenance - ADMIN_MONTHLY_BUY # kwota, która zostaje kupującemu po pokryciu kosztów życia, rata kredytu, utrzymania nieruchomości i opłat administracyjnych

        # Update investments by compounding monthly
        buyer_investment *= (1 + monthly_return) # aktualizacja inwestycji kupującego z uwzględnieniem kapitalizacji
        renter_investment *= (1 + monthly_return) # aktualizacja inwestycji wynajmującego z uwzględnieniem kapitalizacji

        # Add monthly surplus to investments (or subtract if negative - going into debt)
        renter_investment += monthly_surplus_renter # dodanie miesięcznego nadwyżki do inwestycji wynajmującego
        buyer_investment += monthly_surplus_buyer # dodanie miesięcznego nadwyżki do inwestycji kupującego

        # If mortgage paid off, set monthly payment to zero for remaining months
        if remaining_mortgage <= 1e-8:
            remaining_mortgage = 0.0 # jeśli kredyt jest spłacany, pozostała kwota kredytu jest ustawiona na 0
            current_monthly_payment = 0.0 # miesięczna rata kredytu jest ustawiona na 0

    # Final property appreciation: apply at the end of last year if needed
    # (property_value already updated at start of each year; for simplicity we'll apply appreciation if simulation ended mid-year not needed)

    buyer_net_worth = property_value - remaining_mortgage + buyer_investment # majątek netto kupującego: wartość nieruchomości - pozostały kredyt + inwestycje
    renter_net_worth = renter_investment # majątek netto wynajmującego: inwestycje

    buyer_details = {
        "property_value": property_value, # wartość nieruchomości dla bieżącego roku
        "remaining_mortgage": remaining_mortgage, # pozostała kwota kredytu do spłaty
        "buyer_investment": buyer_investment, # inwestycje kupującego
        "total_paid_interest": buyer_paid_interest, # suma spłaconych odsetek
        "total_paid_principal": buyer_paid_principal, # suma spłaconego kapitału
        "total_paid": buyer_total_paid, # suma całkowitych miesięcznych kosztów kupującego (rata + utrzymanie nieruchomości + opłaty administracyjne)
    }
    renter_details = {
        "renter_investment": renter_investment, # inwestycje wynajmującego
        "total_paid_rent": renter_total_paid_rent, # suma całkowitych miesięcznych kosztów wynajmującego (czynsz)
    }

    return SimulationResult(years, buyer_net_worth, renter_net_worth, buyer_details, renter_details)

def run_scenarios(start_year: int, end_year: int = None):
    """Run simulations for different time horizons using global parameters."""

    if start_year < 1:
        raise ValueError("Start year must be greater than 0")

    if end_year is None:
        end_year = start_year

    if start_year > end_year:
        raise ValueError("Start year must be less than end year")

    print("Running simulations with global parameters (edit top of file to change values)\n")
    results: List[SimulationResult] = []
    for h in range(start_year, end_year + 1):
        res = simulate(years=h)
        results.append(res)

    for r in results:
        print(f"--- After {r.years} years ---")
        print(f"Wartość netto kupującego (Wartość nieruchomości - Pozostały kredyt + Inwestycje): {r.buyer_net_worth:,.2f} zł")
        print(f"Wartość netto najemcy(tylko Inwestycje): {r.renter_net_worth:,.2f} zł")
        
        diff = r.buyer_net_worth - r.renter_net_worth
        if diff > 0:
            print(f"Różnica na korzyść kupującego: {diff:,.2f} zł")
        else:
            print(f"Różnica na korzyść najemcy: {-diff:,.2f} zł")
        print()

    # Find breakeven within 30 years
    breakeven = None
    for year in range(1, 31):
        res = simulate(years=year)
        if res.buyer_net_worth > res.renter_net_worth:
            breakeven = year
            break

    if breakeven:
        print(f"Próg rentowności (Breakeven): Zakup staje się bardziej opłacalny po {breakeven} latach.")
    else:
        print("Próg Rentowności (Breakeven): Zakup nie staje się bardziej opłacalny w ciągu 30 lat przy obecnych założeniach.")


if __name__ == '__main__':
    run_scenarios(1, 10)
