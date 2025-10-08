#!/usr/bin/env python3
"""
Przeanalizowanie korzyści płynących z zakupu mieszkania/domu względem wynajmu 
i inwestowania posiadanego kapitału.

Parametry symulacji:
- N_YEARS: długość rozpatrywanego okresu (lata)
- INITIAL_CAPITAL: kapitał jakim dysponujemy na początku
- SAVINGS: roczny dochód po odjęciu kosztów życia (bez wynajmu/kredytu/kosztów posiadania)
- DEPOSIT_INTEREST_RATE: oprocentowanie na lokacie
- PROPERTY_PRICE: cena nieruchomości
- LENDING_RATE: oprocentowanie kredytu hipotecznego
- OWNING_COST: roczny koszt posiadania/utrzymania nieruchomości (% wartości)
- RENTING_COST: roczny koszt wynajmu wraz z opłatami
- REAL_ESTATE_PRICE_CHANGE: roczna zmiana cen nieruchomości i czynszu (%)

Cel: policzyć majątek końcowy po N_YEARS latach w zależności od roku zakupu:
- rok 0: kupujemy od razu
- rok 1 do N_YEARS: kupujemy w tym roku (wcześniej wynajmujemy)
- rok N_YEARS+1: nigdy nie kupujemy (tylko wynajem)

Założenia:
- Wkład własny w roku 0: INITIAL_CAPITAL
- Wkład własny w roku późniejszym: cały zgromadzony kapitał
- Okres kredytu: MORTGAGE_TERM_YEARS (niezależnie od roku zakupu)
- Raty kredytu: równe (annuity), płatne rocznie
"""

from dataclasses import dataclass
from typing import List

# Parametry globalne symulacji
N_YEARS = 10 # długość rozpatrywanego okresu (lata)
INITIAL_CAPITAL = 200_000.0 # kapitał jakim dysponujemy na początku
SAVINGS = 60_000.0 # roczny dochód po odjęciu kosztów życia (bez wynajmu/kredytu/kosztów posiadania)
DEPOSIT_INTEREST_RATE = 0.08  # 8% oprocentowanie na lokacie
PROPERTY_PRICE = 600_000.0 # cena nieruchomości
LENDING_RATE = 0.06  # 6% oprocentowanie kredytu hipotecznego
MORTGAGE_TERM_YEARS = 30  # okres kredytu w latach
OWNING_COST = 0.01  # 1% wartości nieruchomości rocznie, roczny koszt posiadania nieruchomości (% wartości)
RENTING_COST = 36_000.0 # roczny koszt wynajmu wraz z opłatami
REAL_ESTATE_PRICE_CHANGE = 0.04  # 4% roczna zmiana cen nieruchomości i czynszu (%)


@dataclass
class SimulationResult:
    """Wynik symulacji dla danego roku zakupu"""
    purchase_year: int  # 0 = od razu, N_YEARS+1 = nigdy
    net_worth: float  # końcowy majątek
    property_value: float  # wartość nieruchomości (0 jeśli nie kupiono)
    investment: float  # kapitał na lokacie
    remaining_mortgage: float  # pozostały kredyt
    total_paid_rent: float  # łączna suma zapłaconego czynszu w okresie 10 lat
    total_paid_mortgage: float  # łączna suma spłaconych rat kredytu w okresie 10 lat
    total_paid_owning_costs: float  # łączna suma kosztów posiadania w okresie 10 lat
    monthly_mortgage_payment: float  # miesięczna rata kredytu
    loan_amount: float  # początkowa kwota kredytu


def annual_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Oblicza stałą roczną ratę kredytu (annuity).
    
    Args:
        principal: kwota kredytu
        annual_rate: roczne oprocentowanie (np. 0.08 dla 8%)
        years: okres kredytu w latach
    
    Returns:
        roczna rata kredytu
    """
    if principal <= 0:
        return 0.0
    if annual_rate == 0:
        return principal / years
    
    # Wzór na ratę annuity: R = P * [r(1+r)^n] / [(1+r)^n - 1]
    r = annual_rate
    n = years
    payment = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return payment


def simulate_purchase_year(purchase_year: int) -> SimulationResult:
    """
    Symuluje scenariusz zakupu nieruchomości w danym roku.
    
    Args:
        purchase_year: rok zakupu 
                      0 = od razu (na początku)
                      1 do N_YEARS = zakup w tym roku
                      N_YEARS+1 = nigdy nie kupujemy
    
    Returns:
        SimulationResult z wynikami symulacji
    """
    # Inicjalizacja zmiennych
    investment = INITIAL_CAPITAL  # kapitał na lokacie
    property_value = 0.0  # wartość posiadanej nieruchomości
    remaining_mortgage = 0.0  # pozostały kredyt do spłaty
    current_rent = RENTING_COST  # aktualny czynsz
    
    # Zmienne do śledzenia sum
    total_paid_rent = 0.0 # łączna suma zapłaconego czynszu
    total_paid_mortgage = 0.0 # łączna suma spłaconych rat kredytu
    total_paid_owning_costs = 0.0 # łączna suma kosztów posiadania nieruchomości

    # Informacje o kredycie (będą ustawione w momencie zakupu)
    annual_mortgage_payment = 0.0 # roczna rata kredytu
    monthly_mortgage_payment = 0.0 # miesięczna rata kredytu
    mortgage_years_remaining = 0 # pozostałe lata kredytu
    loan_amount = 0.0 # początkowa kwota kredytu
    
    # Symulacja rok po roku (od roku 0 do roku N_YEARS włącznie)
    for year in range(N_YEARS + 1):
        purchased_this_year = False  # Flaga: czy kupiliśmy w tym roku
        
        # Sprawdzamy czy to rok zakupu (i czy jeszcze nie kupiliśmy)
        if year == purchase_year and property_value == 0:
            # ZAKUP NIERUCHOMOŚCI
            # Cena nieruchomości rośnie wraz z rynkiem - w roku Y kosztuje więcej, im później kupujemy tym drosza
            current_property_price = PROPERTY_PRICE * (1 + REAL_ESTATE_PRICE_CHANGE) ** year
            
            # Jeśli mamy więcej kapitału niż cena nieruchomości, płacimy tylko cenę, reszta zostaje na lokacie
            down_payment = min(investment, current_property_price)  # wkład własny = min(kapitał, cena)
            loan_amount = max(0.0, current_property_price - down_payment) # kwota kredytu, 0 jeśli wkład własny >= cena mieszkania
            
            # Ustawiamy parametry kredytu
            remaining_mortgage = loan_amount # pozostały kredyt
            mortgage_years_remaining = MORTGAGE_TERM_YEARS # pozostałe lata kredytu
            annual_mortgage_payment = annual_payment(loan_amount, LENDING_RATE, MORTGAGE_TERM_YEARS) # roczna rata kredytu
            monthly_mortgage_payment = annual_mortgage_payment / 12.0 # miesięczna rata kredytu, uwzględnia ZARÓWNO odsetki JAK I kapitał
            
            # Kupujemy nieruchomość
            property_value = current_property_price # cena nieruchomości w roku zakupu
            investment = investment - down_payment  # nadwyżka kapitału zostaje na lokacie (może być 0), przypadek brzegowy gdy kupujemy od razu bez kredytu
            purchased_this_year = True  # Oznaczamy że kupiliśmy w tym roku
        
        # Aprecjacja/wzrost wartości nieruchomości i czynszu na początku roku
        # NIE aplikujemy aprecjacji w roku zakupu (już uwzględniona w cenie rynkowej)
        if year > 0:
            # jeśli posiadamy nieruchomość (została nabyta) i NIE kupiliśmy jej w tym roku
            if property_value > 0 and not purchased_this_year:
                property_value *= (1 + REAL_ESTATE_PRICE_CHANGE) # Nieruchomość rośnie 4% rocznie
            current_rent *= (1 + REAL_ESTATE_PRICE_CHANGE) # Czynsz rośnie 4% rocznie
        
        # Obliczanie wydatków w tym roku
        yearly_expenses = 0.0
        
        # Jeśli posiadamy nieruchomość, płacimy koszty posiadania i ratę kredytu
        if property_value > 0:
            # WŁAŚCICIEL - płacimy kredyt i koszty posiadania
            owning_cost_this_year = property_value * OWNING_COST # Koszt utrzymania nieruchomości
            
            # Spłata kredytu
            if remaining_mortgage > 0 and mortgage_years_remaining > 0:
                # Odsetki za ten rok
                yearly_interest = remaining_mortgage * LENDING_RATE 

                # Rzeczywista płatność do banku w tym roku (nie więcej niż dług/kapitał + odsetki)
                actual_payment = min(annual_mortgage_payment, remaining_mortgage + yearly_interest)
                
                # Kapitał spłacony w tym roku
                principal_paid = actual_payment - yearly_interest
                remaining_mortgage = max(0.0, remaining_mortgage - principal_paid) # aktualizacja pozostałego kredytu
                # Zmniejszamy liczbę pozostałych lat kredytu
                mortgage_years_remaining -= 1
                
                total_paid_mortgage += actual_payment # suma spłaconych rat kredytu
                yearly_expenses = actual_payment + owning_cost_this_year # Rata + utrzymanie nieruchomości
            else:
                # Kredyt spłacony, płacimy tylko koszty posiadania
                yearly_expenses = owning_cost_this_year
            
            total_paid_owning_costs += owning_cost_this_year
        else:
            # NAJEMCA - płacimy czynsz
            yearly_expenses = current_rent # Roczny czynsz najmu
            total_paid_rent += current_rent # łączna suma zapłaconego czynszu
        
        # Kapitalizacja lokaty
        investment *= (1 + DEPOSIT_INTEREST_RATE) # Lokata rośnie 8% rocznie

        # ile na plusie rocznie, Dodajemy oszczędności minus wydatki
        yearly_surplus = SAVINGS - yearly_expenses # Oszczędności roczne (dochód) - wydatki
        investment += yearly_surplus # aktualizacja kapitału na lokacie
    
    # Końcowy majątek = wartość nieruchomości + kapitał - pozostały kredyt
    net_worth = property_value + investment - remaining_mortgage

    # Zwracamy wyniki symulacji
    return SimulationResult(
        purchase_year=purchase_year,
        net_worth=net_worth,
        property_value=property_value,
        investment=investment,
        remaining_mortgage=remaining_mortgage,
        total_paid_rent=total_paid_rent,
        total_paid_mortgage=total_paid_mortgage,
        total_paid_owning_costs=total_paid_owning_costs,
        monthly_mortgage_payment=monthly_mortgage_payment,
        loan_amount=loan_amount
    )


def get_scenario_name(purchase_year: int) -> str:
    """
    Zwraca nazwę scenariusza w zależności od roku zakupu.
    
    Args:
        purchase_year: rok zakupu (0 = od razu, N_YEARS+1 = nigdy)
    
    Returns:
        nazwa scenariusza
    """
    if purchase_year > N_YEARS:
        return "TYLKO WYNAJEM (nigdy nie kupujemy)"
    elif purchase_year == 0:
        return "Zakup mieszkania OD RAZU (rok 0)"
    else:
        return f"Zakup mieszkania w roku {purchase_year}"


def print_simulation_header():
    """Wyświetla nagłówek i parametry symulacji"""
    print("=" * 80)
    print("SYMULACJA ZAKUPU VS WYNAJMU NIERUCHOMOŚCI")
    print("=" * 80)
    print(f"\nParametry symulacji:")
    print(f"  Okres symulacji: {N_YEARS} lat")
    print(f"  Kapitał początkowy: {INITIAL_CAPITAL:,.0f} zł")
    print(f"  Roczne oszczędności: {SAVINGS:,.0f} zł")
    print(f"  Oprocentowanie lokaty: {DEPOSIT_INTEREST_RATE:.1%}")
    print(f"  Cena nieruchomości: {PROPERTY_PRICE:,.0f} zł")
    print(f"  Oprocentowanie kredytu: {LENDING_RATE:.1%}")
    print(f"  Koszt utrzymania posiadanej nieruchomości: {OWNING_COST:.1%} wartości rocznie")
    print(f"  Roczny czynsz wynajmu: {RENTING_COST:,.0f} zł")
    print(f"  Wzrost cen/czynszu: {REAL_ESTATE_PRICE_CHANGE:.1%} rocznie")
    print()
    print(f"  Okres kredytu: {MORTGAGE_TERM_YEARS} lat")
    print("\n" + "=" * 80)


def print_scenario_details(result: SimulationResult):
    """
    Wyświetla szczegóły wyników symulacji dla danego scenariusza.
    
    Args:
        result: wynik symulacji do wyświetlenia
    """
    scenario_name = get_scenario_name(result.purchase_year)
    
    print(f"\n{scenario_name}:")
    
    print(f"  Majątek końcowy: {result.net_worth:,.2f} zł")
    print(f"    - Wartość nieruchomości: {result.property_value:,.2f} zł")
    print(f"    - Kapitał na lokacie: {result.investment:,.2f} zł")
    print(f"    - Pozostały kredyt: {result.remaining_mortgage:,.2f} zł")
    if result.total_paid_rent > 0:
        print(f"  Suma zapłaconego czynszu za wynajem: {result.total_paid_rent:,.2f} zł")
    # Informacja o kredycie (jeśli kupiono)
    if result.purchase_year <= N_YEARS and result.monthly_mortgage_payment > 0:
        print(f"  Miesięczna rata kredytu: {result.monthly_mortgage_payment:,.2f} zł")
        print(f"  Kwota kredytu: {result.loan_amount:,.2f} zł")
    if result.total_paid_mortgage > 0:
        print(f"  Suma spłaconych rat kredytu: {result.total_paid_mortgage:,.2f} zł")
    if result.total_paid_owning_costs > 0:
        print(f"  Suma kosztów utrzymania posiadanej nieruchomości: {result.total_paid_owning_costs:,.2f} zł")


def print_summary(best_result: SimulationResult):
    """
    Wyświetla podsumowanie z najlepszą strategią.
    
    Args:
        best_result: wynik symulacji z najwyższym majątkiem końcowym
    """
    print("\n" + "=" * 80)
    print("PODSUMOWANIE:")
    print("=" * 80)
    
    if best_result.purchase_year > N_YEARS:
        print(f"Najlepsza strategia: TYLKO WYNAJEM")
    elif best_result.purchase_year == 0:
        print(f"Najlepsza strategia: Zakup OD RAZU (rok 0)")
    else:
        print(f"Najlepsza strategia: Zakup mieszkania w roku {best_result.purchase_year}")
    
    print(f"Maksymalny majątek końcowy: {best_result.net_worth:,.2f} zł")
    
    print()


def run_all_scenarios():
    """Uruchamia symulacje dla wszystkich możliwych lat zakupu"""
    # Nagłówek
    print_simulation_header()
    
    results: List[SimulationResult] = []
    
    # Symulujemy wszystkie możliwe lata zakupu
    # 0 do N_YEARS: zakup w tych latach (N_YEARS+1 opcji)
    # N_YEARS+1: nigdy nie kupujemy (tylko wynajem)
    for year in range(N_YEARS + 2):
        result = simulate_purchase_year(year)
        results.append(result)
    
    # Wyświetlamy wyniki
    print(f"\nWYNIKI SYMULACJI dla okresu {N_YEARS} lat:") 
    print("-" * 80)
    
    for r in results:
        # Szczegóły każdego scenariusza
        print_scenario_details(r)
    
    # Znajdź optymalny rok zakupu
    best_result = max(results, key=lambda r: r.net_worth)
    
    # Podsumowanie
    print_summary(best_result)
    
    return results


if __name__ == '__main__':
    run_all_scenarios()