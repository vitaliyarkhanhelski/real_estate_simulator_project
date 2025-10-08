# 🏠 Symulator Zakupu vs Wynajmu Nieruchomości

<div align="center">

### **Kupić teraz czy poczekać? A może tylko wynajmować?**  
Ten program pomoże Ci znaleźć odpowiedź! 💰

---

## 🎯 Główny Wniosek

```
┌─────────────────────────────────────────────────────────┐
│  💡 KUP OD RAZU = NAJLEPSZA STRATEGIA                   │
│                                                          │
│  Majątek po 10 latach:                                  │
│  🏆 Kup teraz:        960,087 zł                         │
│  ⏳ Kup za 5 lat:     819,535 zł  (-141k zł!)            │
│  🔑 Tylko wynajem:    752,091 zł  (-208k zł!)            │
│                                                          │
│  Paradoks: Większy kredyt + wyższa rata = więcej $$$    │
│  Sekret: Kupujesz najtaniej!                            │
└─────────────────────────────────────────────────────────┘
```

</div>

---

## 📊 Co robi ten program?

Symuluje Twoją sytuację finansową przez **10 lat** i pokazuje, która strategia jest najlepsza:

- 🏡 **Kupić OD RAZU** - bierzesz kredyt i kupujesz mieszkanie już w roku 0
- ⏳ **Poczekać z zakupem** - wynajmujesz i zbierasz na większy wkład własny (lata 1-10)
- 🔑 **Tylko wynajmować** - inwestujesz wszystko na lokacie

Na koniec program pokazuje Twój majątek w każdym scenariuszu!

## ⚙️ Jak to działa?

### 📈 Rosnąca cena nieruchomości
**Mieszkania drożeją!** Cena rośnie 4% rocznie. 

```
Rok 0:  600,000 zł 🏷️
Rok 5:  729,992 zł 🏷️ (+21.7%)
Rok 10: 888,147 zł 🏷️ (+48%)
```

Im dłużej czekasz, tym droższa nieruchomość!

### 💳 Kredyt hipoteczny
- ⏰ **Okres:** 30 lat
- 💰 **Raty:** równe (annuity) - każdego miesiąca płacisz to samo
- 💵 **Wkład własny:** wszystkie zgromadzone oszczędności

### 🎯 Matematyczny trick
Niezależnie kiedy kupisz, **wartość końcowa mieszkania jest taka sama!**

```
Kupujesz w roku 0:  600k → +10 lat → 888k
Kupujesz w roku 5:  730k → +5 lat  → 888k  ✨ magia procentu składanego
```

## 🎮 Parametry Symulacji

Domyślne wartości (możesz je zmienić w kodzie):

| 📌 Parametr | 💵 Wartość | 📝 Co to znaczy? |
|-------------|-----------|------------------|
| **Czas** | 10 lat | Jak długo trwa symulacja |
| **Twój kapitał startowy** | 200,000 zł | Ile masz na początku |
| **Roczne oszczędności** | 60,000 zł | Ile odkładasz rocznie (po kosztach życia) |
| **Lokata** | 8% | Ile zarabiasz na lokacie |
| **Cena mieszkania** | 600,000 zł | Ile kosztuje mieszkanie w roku 0 |
| **Kredyt** | 6% | Ile płacisz odsetek |
| **Okres kredytu** | 30 lat | Jak długo spłacasz kredyt |
| **Koszty utrzymania** | 1% | Ile rocznie wydajesz na mieszkanie (% wartości) |
| **Wynajem** | 36,000 zł/rok | Ile płacisz za wynajem |
| **Wzrost cen** | 4%/rok | Jak szybko drożeją mieszkania i czynsz |

## 🚀 Jak Uruchomić

Wystarczy jeden command:

```bash
python real_estate_simulator_project_homework.py
```

I gotowe! Program sam przeanalizuje wszystkie scenariusze i pokaże wyniki. ✨

## 📈 Przykładowe Wyniki

<details>
<summary>👉 Kliknij, żeby zobaczyć pełne wyniki symulacji</summary>

```
========================================================================
SYMULACJA ZAKUPU VS WYNAJMU NIERUCHOMOŚCI
========================================================================

Parametry symulacji:
  Okres symulacji: 10 lat
  Kapitał początkowy: 200,000 zł
  Roczne oszczędności: 60,000 zł
  Oprocentowanie lokaty: 8.0%
  Cena nieruchomości: 600,000 zł
  Oprocentowanie kredytu: 6.0%
  Okres kredytu: 30 lat

========================================================================

WYNIKI SYMULACJI dla okresu 10 lat:
--------------------------------------------------------------------------------

Zakup mieszkania OD RAZU (rok 0):
  Majątek końcowy: 960,087.45 zł
    - Wartość nieruchomości: 888,146.57 zł
    - Kapitał na lokacie: 396,190.89 zł
    - Pozostały kredyt: 324,250.01 zł
  Miesięczna rata kredytu: 2,421.63 zł
  Kwota kredytu: 400,000.00 zł

Zakup mieszkania w roku 5:
  Majątek końcowy: 819,535.26 zł
    - Wartość nieruchomości: 888,146.57 zł
    - Kapitał na lokacie: 215,439.39 zł
    - Pozostały kredyt: 284,050.69 zł
  Miesięczna rata kredytu: 1,886.07 zł
  Kwota kredytu: 311,537.73 zł

TYLKO WYNAJEM (nigdy nie kupujemy):
  Majątek końcowy: 752,090.60 zł
    - Kapitał na lokacie: 752,090.60 zł

========================================================================
PODSUMOWANIE:
========================================================================
Najlepsza strategia: Zakup OD RAZU (rok 0)
Maksymalny majątek końcowy: 960,087.45 zł
```

</details>

## 🎯 Analiza Wyników

### 🥇 Ranking Strategii

| 🏆 | Rok zakupu | 💰 Majątek końcowy | 💳 Kredyt | 💵 Rata/mies |
|----|------------|-------------------|----------|--------------|
| 🥇 | **0 (OD RAZU)** | **960,087 zł** | 400,000 zł | 2,422 zł |
| 🥈 | 1 | 927,353 zł | 384,000 zł | 2,325 zł |
| 🥉 | 5 | 819,535 zł | 311,538 zł | 1,886 zł |
| 📊 | 10 | 729,406 zł | 197,980 zł | 1,199 zł |
| 🔑 | Tylko wynajem | 752,091 zł | - | - |

### 💡 Kluczowe Wnioski

#### ✅ **ZWYCIĘZCA: Kup od razu!**

Paradoks: Mimo że:
- 💸 Bierzesz największy kredyt (400k)
- 📈 Płacisz najwyższą ratę (2,422 zł/mies)

TO NADAL WYGRYWASZ! Dlaczego? 

```
Kupujesz najtaniej (600k) → Mieszkanie rośnie przez 10 lat → Maksymalny zysk!
```

#### ⚖️ **Kompromis czekania**

| Czekasz dłużej = | Plusy | Minusy |
|------------------|-------|--------|
| | ✅ Mniejszy kredyt | ❌ Droższa nieruchomość |
| | ✅ Niższa rata | ❌ Mniejszy majątek końcowy |

#### 🔑 **Tylko wynajem?**

```
752k zł majątek końcowy
= lepsze niż zakup w latach 7-10
= gorsze niż zakup w latach 0-6
```

Wniosek: Wynajem nie jest zły, ale kupno wcześniej = lepsze! 📊

## 🔧 Struktura Kodu

<details>
<summary>👨‍💻 Dla programistów: jak zbudowany jest kod</summary>

```python
📦 Główne funkcje:

🧮 annual_payment()          → Oblicza roczną ratę kredytu (annuity)
🏗️ simulate_purchase_year()  → Symuluje jeden scenariusz (zakup w danym roku)
📋 print_simulation_header() → Wyświetla parametry symulacji
📊 print_scenario_details()  → Wyświetla wyniki dla scenariusza
🎯 print_summary()           → Wyświetla najlepszą strategię
🚀 run_all_scenarios()       → Uruchamia wszystkie 12 scenariuszy (rok 0-10 + tylko wynajem)

💾 SimulationResult dataclass → Przechowuje wyniki symulacji
```

**Flow programu:**
```
Start → Ustawienie parametrów → Dla każdego roku (0-10 + wynajem):
    ├─ Symuluj rok po roku (10 lat)
    ├─ Oblicz kapitał, kredyt, wydatki
    └─ Zapisz wynik końcowy
→ Porównaj wszystkie → Znajdź najlepszy → Wyświetl ranking
```

</details>

## 💻 Wymagania

- 🐍 Python 3.7 lub nowszy
- 📚 Biblioteki standardowe: `dataclasses`, `typing`
- ⚡ Działa od razu - zero instalacji!

## 🎓 Zastosowania Edukacyjne

Ten program to świetny przykład:
- ✅ Symulacji finansowej
- ✅ Analizy scenariuszy
- ✅ Matematyki finansowej (procent składany, annuity)
- ✅ Optymalizacji decyzji
- ✅ Clean code w Python

Idealny do nauki programowania + finansów! 🚀

## 📝 Licencja

MIT - użyj swobodnie! 🎉

---

<div align="center">

**🏠 Kupić czy wynajmować? Teraz już wiesz! 💡**

Stworzony z ❤️ jako projekt edukacyjny

</div>

