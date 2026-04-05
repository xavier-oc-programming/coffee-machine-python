# Coffee Machine — Command-Line Simulator

A Python command-line application that simulates a fully functional coffee vending machine. The machine tracks ingredient resources, processes coin-based payments, calculates change, and dispenses drinks — all through the terminal.

Two builds are included: the original procedural course exercise and a full OOP refactor with separated concerns, type hints, and persisted lifetime revenue.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Builds Comparison](#2-builds-comparison)
3. [Commands](#3-commands)
4. [Ordering Flow](#4-ordering-flow)
5. [Features](#5-features)
6. [Navigation Flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module Reference](#8-module-reference)
9. [Configuration Reference](#9-configuration-reference)
10. [Session Flow Diagram](#10-session-flow-diagram)
11. [Design Decisions](#11-design-decisions)
12. [Course Context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 1. Quick Start

**Requirements:** Python 3.10+  — no external packages.

```bash
python menu.py
```

Select `1` for the original build, `2` for the advanced OOP build, or `q` to quit.

To run either build directly:

```bash
python original/main.py
python advanced/main.py
```

---

## 2. Builds Comparison

| Feature                        | Original | Advanced |
|-------------------------------|----------|----------|
| Architecture                  | Procedural | OOP |
| File count                    | 2        | 6        |
| Type hints                    | No       | Yes      |
| Separation of concerns        | Partial  | Full     |
| All I/O in one place          | No       | Yes (`display.py`) |
| Zero magic numbers            | No       | Yes (`config.py`) |
| Persisted lifetime revenue    | No       | Yes (`data.txt`) |
| Input validation (coins)      | Basic    | Full (loops on invalid) |
| Floating-point safety         | No       | Yes (`round()` throughout) |
| Terminal launcher (`menu.py`) | —        | ✓ |

---

## 3. Commands

On startup, both builds print a command reference before the first prompt:

```
Coffee Machine ready.
  Orders  : espresso / latte / cappuccino
  Commands: report / refill / refill <ingredient> / off
```

Commands are then entered at the `>>` prompt:

| Input                   | Context            | Result                                          |
|-------------------------|--------------------|-------------------------------------------------|
| `espresso`              | `>>` prompt        | Begin ordering an espresso ($1.50)              |
| `latte`                 | `>>` prompt        | Begin ordering a latte ($2.50)                  |
| `cappuccino`            | `>>` prompt        | Begin ordering a cappuccino ($3.00)             |
| `report`                | `>>` prompt        | Print current resource and revenue levels       |
| `refill`                | `>>` prompt        | Reset all ingredients to starting levels        |
| `refill water`          | `>>` prompt        | Reset water to 300 ml                           |
| `refill milk`           | `>>` prompt        | Reset milk to 200 ml                            |
| `refill coffee`         | `>>` prompt        | Reset coffee to 100 g                           |
| `off`                   | `>>` prompt        | Shut down the machine and exit                  |
| `1` `2` `3` `4`         | Coin prompt        | Select penny / nickel / dime / quarter          |
| *(any integer)*         | Coin amount prompt | Number of that coin to insert                   |

---

## 4. Ordering Flow

Every order follows the same sequence:

1. **Drink selection** — user types a drink name at the prompt
2. **Resource check** — machine verifies it has enough water, milk, and coffee
3. **Cost display** — machine prints the price
4. **Coin menu** — coin types and values are displayed
5. **Coin insertion loop** — user selects a coin type and quantity; loop repeats until the running total meets the cost
6. **Change** — any overpayment is returned
7. **Dispense** — ingredients are deducted, revenue recorded, drink confirmed
8. **Back to prompt** — machine immediately accepts the next command

If resources are insufficient at step 2, the order is cancelled and the machine returns to the main prompt.

---

## 5. Features

### Both Builds

**Persistent machine loop** — the machine stays on until `off` is typed. Every order returns to the main prompt automatically.

**Real-time resource tracking** — each drink deducts its exact ingredient amounts from the machine's supply. Resources are finite and shared across the session.

**Coin-by-coin payment** — the coin insertion loop accepts one coin denomination at a time, in any quantity. The loop continues until the running total meets or exceeds the cost.

**Change calculation** — any overpayment is computed and returned to the user at dispense time.

**Resource report** — typing `report` prints current water, milk, coffee, and revenue levels with aligned columns.

**Input validation** — unknown commands print an error without crashing or restarting the machine.

### Advanced Build Only

**Separated concerns** — logic classes (`CoffeeMachine`, `DrinkMenu`, `CoinProcessor`) contain zero `print()` or `input()` calls. All terminal I/O lives exclusively in `display.py`.

**Type hints throughout** — every function signature carries parameter and return type annotations.

**Zero magic numbers** — every constant (resource amounts, prices, coin values, column widths) is defined once in `config.py` and imported everywhere else.

**Persisted lifetime revenue** — `data.txt` records total money earned across all sessions. The report shows both session revenue and the running lifetime total.

**Floating-point safety** — every monetary calculation is wrapped in `round(..., 2)` to prevent binary floating-point drift (e.g. `0.1 + 0.2 = 0.30000000000000004`).

**Terminal launcher** — `menu.py` provides a looping menu that launches either build as a subprocess and returns to the menu when the build exits.

---

## 6. Navigation Flow

### Terminal Menu (menu.py)

```
python menu.py
│
├── 1 ──► subprocess: original/main.py
│         (returns to menu when "off" is typed)
│
├── 2 ──► subprocess: advanced/main.py
│         (returns to menu when "off" is typed)
│
└── q ──► exit launcher
```

### In-App Command Flow

```
┌────────────────────────────────┐
│          MACHINE ON            │
│   waiting for command...       │
└──────────────┬─────────────────┘
               │
    ┌──────────┼──────────────┬──────────────┐
    ▼          ▼              ▼              ▼
  "off"     "report"    drink name      anything else
    │          │              │              │
  shutdown   print          valid?         print
  & exit     report     ┌────┴────┐       "invalid"
                         ▼        ▼
                        yes        no
                         │        │
                    resource    print "not
                     check       in menu"
                         │
                    sufficient?
                   ┌─────┴─────┐
                   ▼           ▼
                  yes           no
                   │            │
             show cost      print "not
             coin menu      enough X"
                   │
              coin loop
           (repeat until paid)
                   │
             calculate change
             deduct resources
             add revenue
             print confirmation
                   │
                   ▼
         ┌────────────────────┐
         │   back to prompt   │
         └────────────────────┘
```

---

## 7. Architecture

```
coffee-machine-python/
│
├── menu.py              # Terminal launcher — looping menu, subprocess.run()
├── art.py               # LOGO constant — ASCII art printed by menu.py
├── requirements.txt     # Standard library only; Python 3.10+ note
├── .gitignore
│
├── docs/
│   └── COURSE_NOTES.md  # Breakdown of every Python concept used in original/
│
├── original/            # Course build — verbatim, procedural
│   ├── main.py          # All logic in one file; module-level state
│   └── coffee_data.py   # MENU, resources, coin_value dictionaries
│
└── advanced/            # OOP refactor — separated concerns, type hints
    ├── config.py        # Every constant; zero magic numbers elsewhere
    ├── machine.py       # class CoffeeMachine — resources, revenue, persistence
    ├── drink_menu.py    # class DrinkMenu — menu data access
    ├── coin_processor.py# class CoinProcessor — payment calculations
    ├── display.py       # class Display — ALL print() and input() calls
    ├── main.py          # Orchestrator — input → logic → display, no business logic
    └── data.txt         # Persisted lifetime revenue (float, updated each sale)
```

---

## 8. Module Reference

### `DrinkMenu` — `advanced/drink_menu.py`

| Method | Returns | Description |
|--------|---------|-------------|
| `get_names()` | `list[str]` | All available drink names |
| `is_valid(name)` | `bool` | True if the name matches a menu item |
| `get_cost(drink_name)` | `float` | Price of the drink in dollars |
| `get_ingredients(drink_name)` | `dict[str, int]` | Ingredient requirements |

---

### `CoffeeMachine` — `advanced/machine.py`

| Method | Returns | Description |
|--------|---------|-------------|
| `check_resources(drink_name)` | `str \| None` | First insufficient ingredient name, or `None` if OK |
| `deduct_resources(drink_name)` | `None` | Deduct ingredients used by a drink |
| `refill_all()` | `dict[str, int]` | Reset all ingredients to starting levels, return new amounts |
| `refill_one(ingredient)` | `int` | Reset one ingredient to its starting level, return new amount |
| `add_revenue(amount)` | `None` | Add a sale to session + lifetime revenue, save to disk |
| `get_report()` | `dict[str, int \| float]` | Current resource levels and revenue figures |

---

### `CoinProcessor` — `advanced/coin_processor.py`

| Method | Returns | Description |
|--------|---------|-------------|
| `is_valid_coin(key)` | `bool` | True if key is a valid coin menu number |
| `get_coin_name(key)` | `str` | Display name (e.g. `"Quarter"`) |
| `get_coin_value(key)` | `float` | Dollar value (e.g. `0.25`) |
| `calculate_change(inserted, cost)` | `float` | Change owed, rounded to 2 decimal places |

---

### `Display` — `advanced/display.py`

| Method | Returns | Description |
|--------|---------|-------------|
| `show_startup()` | `None` | Prints the command reference once on machine start |
| `prompt_drink()` | `str` | Prompts for and returns drink name input at `>>` |
| `prompt_coin()` | `str` | Prompts for coin type selection |
| `prompt_coin_amount(coin_name)` | `int` | Prompts for quantity; loops until valid integer |
| `show_report(report)` | `None` | Prints resource levels and revenue |
| `show_coin_menu()` | `None` | Prints all coin types with values |
| `show_order_cost(drink, cost)` | `None` | Prints drink price before payment |
| `show_coin_added(name, batch_value, total)` | `None` | Prints running coin total |
| `show_change(drink, change)` | `None` | Confirms order and prints change |
| `show_checking(drink)` | `None` | Prints resource check message |
| `show_insufficient_resources(ingredient)` | `None` | Prints shortage error |
| `show_invalid_input(text)` | `None` | Prints unrecognised command error |
| `show_refill_all(amounts)` | `None` | Prints confirmation after all ingredients refilled |
| `show_refill_one(ingredient, amount)` | `None` | Prints confirmation after single ingredient refilled |
| `show_refill_invalid(ingredient)` | `None` | Prints error for unrecognised ingredient name |
| `show_invalid_coin()` | `None` | Prints invalid coin selection error |
| `show_shutdown()` | `None` | Prints goodbye message |

---

## 9. Configuration Reference

All constants live in `advanced/config.py`. No other file uses a magic number.

| Constant | Default | Description |
|----------|---------|-------------|
| `STARTING_WATER` | `300` | Initial water supply in ml |
| `STARTING_MILK` | `200` | Initial milk supply in ml |
| `STARTING_COFFEE` | `100` | Initial coffee supply in g |
| `MENU` | *(dict)* | Drink names → ingredients + cost |
| `COIN_TYPES` | *(dict)* | Coin keys `"1"`–`"4"` → name + value |
| `CMD_OFF` | `"off"` | Shutdown command string |
| `CMD_REPORT` | `"report"` | Report command string |
| `REPORT_LABEL_WIDTH` | `10` | Left-column width for report rows |
| `COIN_NAME_WIDTH` | `10` | Left-column width for coin menu rows |

### Menu Prices

| Drink | Water | Milk | Coffee | Cost |
|-------|-------|------|--------|------|
| Espresso | 50 ml | — | 18 g | $1.50 |
| Latte | 200 ml | 150 ml | 24 g | $2.50 |
| Cappuccino | 250 ml | 100 ml | 24 g | $3.00 |

### Coin Values

| Key | Name | Value |
|-----|------|-------|
| `1` | Penny | $0.01 |
| `2` | Nickel | $0.05 |
| `3` | Dime | $0.10 |
| `4` | Quarter | $0.25 |

---

## 10. Session Flow Diagram

The terminal session follows a strict linear flow with one re-entry point:

```
  START
    │
    ▼
┌──────────────────────────────────────────┐
│ prompt: espresso / latte / cappuccino /  │◄──────────────┐
│         report / off                     │               │
└──────────────┬───────────────────────────┘               │
               │                                           │
        ┌──────┴──────┐                                    │
        │             │                                    │
       off          report         invalid         drink name
        │             │               │                    │
    shutdown       ┌──┴───────────┐  error                 │
      exit         │   Resource   │   msg          ┌───────┴──────┐
                   │   Report     │                │              │
                   │  water: Xml  │         not enough X     resources OK
                   │  milk:  Xml  │                │              │
                   │  coffee: Xg  │               msg          show cost
                   │  revenue: $X │                │              │
                   └──────────────┘          back to prompt   ┌──┴──────────────────┐
                         │                                    │    COIN LOOP         │
                   back to prompt                             │  show coin menu      │
                                                             │  prompt coin type    │
                                                             │  prompt quantity     │
                                                             │  add to running total│
                                                             │  repeat if total<cost│
                                                             └──────────┬───────────┘
                                                                        │
                                                                  total >= cost
                                                                        │
                                                               calculate change
                                                               deduct ingredients
                                                               add revenue to disk
                                                               print confirmation
                                                                        │
                                                                back to prompt ──►
```

---

## 11. Design Decisions

### `display.py` owns all I/O

Every `print()` and `input()` call in the advanced build lives in `display.py`. Logic classes (`CoffeeMachine`, `DrinkMenu`, `CoinProcessor`) have zero terminal interaction.

**Why:** Logic that doesn't touch I/O can be tested without capturing stdout or mocking input. It can also be swapped to a different interface (GUI, web API) by replacing only `display.py`. The original build mixes output and logic throughout `main.py`, which makes both harder to change independently.

---

### `check_resources` returns `str | None` instead of `bool`

```python
missing = machine.check_resources(user_input)
if missing:
    display.show_insufficient_resources(missing)  # knows which ingredient
```

**Why:** A boolean only tells you whether the order can be made. Returning the ingredient name lets the error message tell the user *which* resource ran out, without needing a second lookup or a separate method call.

---

### `round()` on every monetary calculation

```python
coin_sum = round(coin_sum + batch, 2)
change   = round(inserted - cost, 2)
```

**Why:** Python floats use binary representation. `0.1 + 0.2` evaluates to `0.30000000000000004`. In the original build, coin sums could drift slightly, causing the `while coin_sum < order_cost` condition to behave unexpectedly. Rounding to 2 decimal places after every operation keeps money values exact.

---

### `subprocess.run()` with `cwd=str(path.parent)` in `menu.py`

```python
subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
```

**Why:** Each build lives in its own subdirectory (`original/`, `advanced/`). When Python runs a script, it adds the script's own directory to `sys.path` automatically — but only if the working directory matches. Setting `cwd` to the script's parent ensures that sibling imports (`import config`, `import machine`) resolve correctly inside the subprocess, without needing relative import syntax or installed packages.

---

### `while True` loop in `menu.py` instead of recursion

```python
while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)
    choice = input("  Enter your choice: ").strip().lower()
    if choice == "q":
        break
    ...
```

**Why:** A recursive `main()` call would grow the call stack by one frame every time a build exits and the menu re-appears. For a long-running launcher this would eventually hit Python's recursion limit. The `while True` loop is flat and correct — it simply re-runs on every iteration.

---

### Console cleared before every menu render

```python
os.system("cls" if os.name == "nt" else "clear")
```

**Why:** When a build exits after typing `off`, its output is still visible in the terminal. Clearing the console before re-drawing the menu gives a clean, intentional UI rather than the launcher appearing mid-stream after a wall of coffee machine output.

---

### `sys.path.insert(0, ...)` in `advanced/main.py`

```python
sys.path.insert(0, str(Path(__file__).parent))
```

**Why:** When `menu.py` launches `advanced/main.py` with `cwd=advanced/`, Python adds `advanced/` to `sys.path`. But if `advanced/main.py` is run directly (`python advanced/main.py` from the repo root), the working directory is the repo root, and sibling imports like `from config import ...` would fail. The `sys.path.insert` line makes imports work correctly in both launch contexts.

---

## 12. Course Context

Built as **Day 15** of the [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

The course exercise is a procedural coffee machine that covers:
- Nested dictionaries
- While loops with boolean flags
- Module separation (`coffee_data.py`)
- f-string formatting with alignment
- Type casting (`int()`, `float()`)

The advanced build extends those fundamentals into OOP territory (classes, methods, encapsulation, type hints) as a self-directed refactor.

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for a full breakdown of every concept applied in the original build.

---

## 13. Dependencies

| Module | Used in | Purpose |
|--------|---------|---------|
| `os` | `menu.py` | `os.system()` to clear the terminal |
| `sys` | `menu.py`, `advanced/main.py` | Subprocess executable path; `sys.path` manipulation |
| `subprocess` | `menu.py` | Launch `original/` and `advanced/` as child processes |
| `pathlib.Path` | `menu.py`, `advanced/machine.py`, `advanced/main.py` | Portable file path construction |
