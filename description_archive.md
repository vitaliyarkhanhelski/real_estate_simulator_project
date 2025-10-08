# 🏠 Symulator Nieruchomości: Wynajem vs Zakup

## 📊 Opis programu

Program symuluje i porównuje dwie strategie finansowe na przestrzeni czasu:

| 🏡 **Kupno nieruchomości** | 🔑 **Wynajem mieszkania** |
|---------------------------|--------------------------|
| Kredyt hipoteczny | Inwestowanie oszczędności |
| Własność nieruchomości | Elastyczność finansowa |

Symulator przeprowadza **szczegółową analizę miesięczną**, uwzględniając wszystkie koszty i zyski obu scenariuszy, aby pokazać, która opcja jest bardziej opłacalna finansowo w różnych horyzontach czasowych.

---

## 🎯 Jak działa program?

### 🏡 Scenariusz Kupującego:
- ✅ Wpłaca wkład własny (20% ceny nieruchomości)
- 💰 Zaciąga kredyt hipoteczny na pozostałą kwotę
- 📅 Płaci miesięczne raty kredytu (kapitał + odsetki)
- 🔧 Pokrywa koszty utrzymania nieruchomości (1,5% wartości rocznie)
- 🏢 Płaci opłaty administracyjne/czynsz (1000 zł/miesiąc)
- 📈 Inwestuje pozostałe oszczędności
- 🚀 Wartość nieruchomości rośnie o 5% rocznie

### 🔑 Scenariusz Najemcy:
- 💵 Zachowuje cały kapitał początkowy
- 🏠 Płaci miesięczny czynsz (rosnący o 5% rocznie)
- 📊 Inwestuje wszystkie oszczędności (zwrot 4% rocznie)

---

## ⚙️ Parametry symulacji

| Parametr | Wartość | Opis |
|----------|---------|------|
| 🏠 **Cena nieruchomości** | 500 000 zł | Całkowita cena mieszkania |
| 💰 **Kapitał początkowy** | 100 000 zł | Oszczędności na start |
| 📝 **Wkład własny** | 100 000 zł | 20% ceny nieruchomości |
| 📈 **Oprocentowanie kredytu** | 7% | Roczne oprocentowanie |
| ⏱️ **Okres kredytu** | 30 lat | Czas spłaty kredytu |
| 🔑 **Miesięczny czynsz** | 2 600 zł | Początkowy czynsz |
| 📊 **Wzrost czynszu** | 5% rocznie | Inflacja wynajmu |
| 🚀 **Wzrost wartości nieruchomości** | 5% rocznie | Aprecjacja |
| 🔧 **Koszty utrzymania** | 1,5% rocznie | % wartości nieruchomości |
| 💹 **Zwrot z inwestycji** | 4% rocznie | Lokata/fundusze |
| 🏢 **Opłaty administracyjne** | 1 000 zł/m-c | Dla właściciela |
| 💼 **Miesięczna pensja** | 10 000 zł | Dochód netto |
| 🛒 **Koszty życia** | 4 000 zł/m-c | Jedzenie, rachunki, etc. |

*Wszystkie parametry można edytować w pliku źródłowym!*

---

## 🚀 Jak używać programu?

### Uruchomienie z domyślnymi parametrami:
```bash
python3 real_estate_simulator_project_homework.py
```

### 📅 Funkcja `run_scenarios(start_year, end_year)`

Program pozwala na przeprowadzenie symulacji dla różnych horyzontów czasowych **co rok**.

#### 📌 Przykład 1: Symulacja dla jednego roku
```python
run_scenarios(5)  # Symulacja tylko dla 5 lat
```
**Wynik:** Jedna symulacja dla 5 lat

#### 📌 Przykład 2: Symulacja dla zakresu lat (co rok)
```python
run_scenarios(1, 10)  # Symulacja od 1 do 10 lat
```
**Wynik:** 10 symulacji - dla 1, 2, 3, 4, 5, 6, 7, 8, 9 i 10 lat

#### 📌 Przykład 3: Symulacja dla wybranego zakresu
```python
run_scenarios(5, 10)  # Symulacja od 5 do 10 lat
```
**Wynik:** 6 symulacji - dla 5, 6, 7, 8, 9 i 10 lat

> 💡 **Uwaga:** Program automatycznie generuje symulację dla **każdego roku** w podanym zakresie!

---

## 📈 Wyniki symulacji

Program wyświetla dla każdego roku:

| Metryka | Opis |
|---------|------|
| 🏡 **Wartość netto kupującego** | Wartość nieruchomości - pozostały kredyt + inwestycje |
| 🔑 **Wartość netto najemcy** | Całkowite inwestycje |
| ⚖️ **Różnica** | Która opcja jest bardziej opłacalna i o ile |
| 🎯 **Próg rentowności** | Po ilu latach zakup staje się bardziej opłacalny |

### 📋 Przykładowy wynik:
```
--- After 5 years ---
Wartość netto kupującego (Wartość nieruchomości - Pozostały kredyt + Inwestycje): 245,678.50 zł
Wartość netto najemcy(tylko Inwestycje): 198,432.20 zł
Różnica na korzyść kupującego: 47,246.30 zł

--- After 6 years ---
Wartość netto kupującego (Wartość nieruchomości - Pozostały kredyt + Inwestycje): 268,543.20 zł
Wartość netto najemcy(tylko Inwestycje): 215,876.40 zł
Różnica na korzyść kupującego: 52,666.80 zł

...

Próg rentowności (Breakeven): Zakup staje się bardziej opłacalny po 3 latach.
```

---

## 🔧 Dostosowanie parametrów

Aby zmienić parametry symulacji, edytuj wartości na początku pliku `real_estate_simulator_project_homework.py`:

```python
# Edytowalne parametry globalne
PRICE = 500_000.0            # Cena nieruchomości
INITIAL_CAPITAL = 100_000.0  # Kapitał początkowy
MORTGAGE_RATE = 0.07         # Oprocentowanie kredytu (7%)
MORTGAGE_TERM_YEARS = 30     # Okres kredytu w latach
RENT_MONTHLY = 2600.0        # Miesięczny czynsz
RENT_ANNUAL_INCREASE = 0.05  # Wzrost czynszu (5%)
PROPERTY_ANNUAL_APPRECIATION = 0.05  # Wzrost wartości (5%)
MAINTENANCE_ANNUAL_PCT = 0.015  # Koszty utrzymania (1.5%)
INVESTMENT_ANNUAL_RETURN = 0.04  # Zwrot z inwestycji (4%)
ADMIN_MONTHLY_BUY = 1000.0   # Opłaty administracyjne
MONTHLY_SALARY = 10_000.0    # Miesięczna pensja
LIVING_COST = 4_000.0        # Miesięczne koszty życia
```

---

## 💻 Wymagania techniczne

- **Python 3.6** lub nowszy
- **Biblioteki standardowe:** `dataclasses`, `typing`

---

## 📚 Zastosowanie

✅ Analiza opłacalności zakupu vs wynajmu  
✅ Planowanie finansów osobistych  
✅ Symulacje różnych scenariuszy rynkowych  
✅ Edukacja finansowa  
✅ Podejmowanie świadomych decyzji inwestycyjnych  

---

## 👨‍💻 Autor

Program edukacyjny do analizy decyzji finansowych dotyczących nieruchomości.

---

**Miłej zabawy z symulacjami! 🎉**
