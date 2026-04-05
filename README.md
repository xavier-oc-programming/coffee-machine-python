# Coffee Machine — Command-Line Simulator

A Python command-line application that simulates a fully functional coffee machine. The machine tracks ingredient resources, processes coin-based payments, calculates change, and dispenses drinks — all through a terminal interface.

Built as Day 15 of my 100 Days of Code challenge.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
  - [Ordering a Drink](#ordering-a-drink)
  - [Inserting Coins](#inserting-coins)
  - [Resource Report](#resource-report)
  - [Turning Off](#turning-off)
- [Menu & Pricing](#menu--pricing)
- [Coin Reference](#coin-reference)
- [Starting Resources](#starting-resources)
- [Example Session](#example-session)
- [Concepts Practiced](#concepts-practiced)

---

## Overview

This project simulates the internal logic of a coffee vending machine. When the machine is running, a user can:

- Choose a drink from the menu
- Insert coins one type at a time until the cost is covered
- Receive change if they overpay
- Be denied the order if resources (water, milk, coffee) are insufficient
- Check current resource levels
- Shut the machine down

The project is split into two files: `main.py` handles all program logic, and `coffee_data.py` stores the data (menu, resources, coin values) as a separate module.

---

## Features

- Persistent machine state using a `while` loop — stays on until explicitly turned off
- Real-time resource tracking — each order deducts ingredients from the machine's supply
- Revenue tracking — machine records total money collected
- Coin-by-coin payment loop — user inserts coins until the balance meets the order cost
- Automatic change calculation
- Input validation for both drink orders and coin selections
- Formatted resource report with aligned columns

---

## Project Structure

```
coffee-machine-python/
├── main.py          # Main program logic and control flow
├── coffee_data.py   # Menu, resource levels, and coin data
├── COURSE_NOTES.md  # Concepts and techniques used in this project
└── README.md
```

---

## How to Run

**Requirements:** Python 3.x — no external libraries needed.

```bash
python main.py
```

---

## How to Use

### Ordering a Drink

When prompted, type the name of your drink:

```
What would you like? (espresso/latte/cappuccino): latte
```

### Inserting Coins

A coin menu is displayed. Enter the number of the coin type, then the quantity:

```
Coin Menu:
1: Penny:     $0.01
2: Nickel:    $0.05
3: Dime:      $0.10
4: Quarter:   $0.25

Enter the number corresponding to the coin: 4
How many of this coin would you like to enter? 10
```

Repeat until your total meets or exceeds the drink cost. The machine will then prepare your order and return any change.

### Resource Report

Type `report` to see current machine levels:

```
Water:     250ml
Milk:      150ml
Coffee:    82g
Money:     $2.50
```

### Turning Off

Type `off` to shut the machine down:

```
Coffee machine is now turning off...
Have a nice day!
```

---

## Menu & Pricing

| Drink       | Water  | Milk   | Coffee | Cost   |
|-------------|--------|--------|--------|--------|
| Espresso    | 50 ml  | —      | 18 g   | $1.50  |
| Latte       | 200 ml | 150 ml | 24 g   | $2.50  |
| Cappuccino  | 250 ml | 100 ml | 24 g   | $3.00  |

---

## Coin Reference

| # | Coin    | Value  |
|---|---------|--------|
| 1 | Penny   | $0.01  |
| 2 | Nickel  | $0.05  |
| 3 | Dime    | $0.10  |
| 4 | Quarter | $0.25  |

---

## Starting Resources

| Resource | Amount |
|----------|--------|
| Water    | 300 ml |
| Milk     | 200 ml |
| Coffee   | 100 g  |
| Money    | $0.00  |

---

## Example Session

```
What would you like? (espresso/latte/cappuccino): espresso
Checking coffee order...
Sufficient resources to prepare order.
Your order of espresso will be a total of $1.50

Coin Menu:
1: Penny:      $0.01
2: Nickel:     $0.05
3: Dime:       $0.10
4: Quarter:    $0.25

Enter the number corresponding to the coin: 4
How many of this coin would you like to enter? 6
You have added a total of $1.50
Your sum of coins is 1.50
Thank you! Preparing your espresso. Your change is $0.00.

What would you like? (espresso/latte/cappuccino): report
Water:     250ml
Milk:      200ml
Coffee:    82g
Money:     $1.50

What would you like? (espresso/latte/cappuccino): off

Coffee machine is now turning off...
Have a nice day!
```

---

## Concepts Practiced

See [COURSE_NOTES.md](COURSE_NOTES.md) for a full breakdown of every Python concept applied in this project.
