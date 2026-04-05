# Course Notes — Coffee Machine Project

A breakdown of every Python concept applied in this project, with explanations and examples pulled directly from the code.

---

## Table of Contents

- [Modules & Imports](#modules--imports)
- [Dictionaries](#dictionaries)
  - [Nested Dictionaries](#nested-dictionaries)
  - [Accessing Values](#accessing-values)
  - [Iterating with .items()](#iterating-with-items)
  - [Accessing Keys with .keys()](#accessing-keys-with-keys)
- [Functions](#functions)
  - [Defining & Calling Functions](#defining--calling-functions)
  - [Parameters & Return Values](#parameters--return-values)
- [While Loops](#while-loops)
  - [Infinite Loop with Boolean Flag](#infinite-loop-with-boolean-flag)
  - [Condition-Based Loop](#condition-based-loop)
  - [break Statement](#break-statement)
- [For Loops](#for-loops)
  - [Iterating Over a Dictionary](#iterating-over-a-dictionary)
- [Conditional Statements](#conditional-statements)
  - [if / elif / else](#if--elif--else)
  - [Membership Testing with in](#membership-testing-with-in)
- [f-Strings & String Formatting](#f-strings--string-formatting)
  - [Basic f-String](#basic-f-string)
  - [Alignment & Padding](#alignment--padding)
  - [Floating-Point Formatting](#floating-point-formatting)
- [Type Casting](#type-casting)
- [Variables & Reassignment](#variables--reassignment)
- [Arithmetic & Compound Assignment](#arithmetic--compound-assignment)
- [list() Conversion](#list-conversion)
- [Boolean Logic](#boolean-logic)

---

## Modules & Imports

Python allows you to split code across multiple files. A **module** is just a `.py` file. You import it using the `import` keyword and then access its contents with dot notation.

```python
import coffee_data

coffee_data.MENU       # access the MENU dictionary
coffee_data.resources  # access the resources dictionary
```

**Why use a module here?**
Separating data (`coffee_data.py`) from logic (`main.py`) keeps the code organized and easier to maintain. This mirrors the concept of separation of concerns.

---

## Dictionaries

### Nested Dictionaries

A dictionary where values are themselves dictionaries. This project uses nested dicts to represent menu items:

```python
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
}
```

To access a nested value, chain the keys:

```python
MENU["espresso"]["cost"]                     # → 1.5
MENU["latte"]["ingredients"]["water"]        # → 200
```

### Accessing Values

```python
order_cost = float(coffee_data.MENU[user_input]['cost'])
```

`user_input` is a variable used as the key — Python dictionaries accept any hashable value as a key, including variable contents.

### Iterating with .items()

`.items()` returns each key-value pair as a tuple, allowing you to unpack both at once:

```python
for index, coin_data in coffee_data.coin_value.items():
    coin_face_name, coin_value = list(coin_data.items())[0]
```

Here, `coin_value` is itself a dict `{"Quarter": 0.25}`, so `.items()` is called again to unpack the inner pair.

### Accessing Keys with .keys()

`.keys()` returns a view of all keys in a dictionary:

```python
list(coffee_data.MENU.keys())  # → ['espresso', 'latte', 'cappuccino']
```

Wrapping in `list()` converts the view into a list for use in membership checks and indexing.

---

## Functions

### Defining & Calling Functions

Functions are reusable blocks of code defined with `def`:

```python
def resource_check(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        if coffee_data.MENU[order]["ingredients"][ingredient] > coffee_data.resources[ingredient]:
            return False
    return True
```

Called later as:

```python
enough_resources = resource_check(user_input)
```

### Parameters & Return Values

- **Parameter**: `order` — the value passed in when calling the function
- **Return value**: `True` or `False` — the function evaluates all ingredients and returns a boolean

The same pattern is used for `resource_update(order)`, which modifies the `resources` dictionary in-place:

```python
def resource_update(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        coffee_data.resources[ingredient] -= coffee_data.MENU[order]['ingredients'][ingredient]
```

No return value is needed here since the function directly mutates the module-level dictionary.

---

## While Loops

### Infinite Loop with Boolean Flag

The machine runs continuously until the user explicitly shuts it down. A boolean variable acts as the on/off switch:

```python
machine_on = True

while machine_on:
    user_input = input("What would you like? ...")
    if user_input == "off":
        break
```

Using `break` exits the loop immediately without evaluating any further code in that iteration.

### Condition-Based Loop

The coin collection loop continues until the user has inserted enough money:

```python
coin_sum = 0
while coin_sum < order_cost:
    # accept coins, add to coin_sum
```

This loop only exits when the condition becomes False — i.e., when `coin_sum` reaches or exceeds `order_cost`.

### break Statement

`break` immediately exits the nearest enclosing loop:

```python
if not enough_resources:
    print("Insufficient resources to prepare order.")
    ordering_coffee = False
    break
```

Setting `ordering_coffee = False` before `break` ensures the outer loop doesn't re-enter the inner ordering block on the next iteration.

---

## For Loops

### Iterating Over a Dictionary

You can loop over dictionary keys directly:

```python
for ingredient in coffee_data.MENU[order]['ingredients']:
    coffee_data.resources[ingredient] -= coffee_data.MENU[order]['ingredients'][ingredient]
```

Each `ingredient` is a key string (e.g., `"water"`, `"milk"`, `"coffee"`), which is then used to index both dictionaries simultaneously.

---

## Conditional Statements

### if / elif / else

Used to branch program flow based on user input:

```python
if user_input == "off":
    break
elif user_input == 'report':
    # print resource report
elif user_input in list(coffee_data.MENU.keys()):
    ordering_coffee = True
else:
    print(f'Could not fulfill your command of "{user_input}".')
```

Only one branch runs per iteration. Python evaluates them top-to-bottom and stops at the first `True` condition.

### Membership Testing with in

The `in` operator checks whether a value exists in a collection:

```python
if user_input in list(coffee_data.MENU.keys()):
    ...

if coin_choice in list(coffee_data.coin_value.keys()):
    ...
```

This is used here as input validation — ensuring the user's input matches a valid key before trying to access it.

---

## f-Strings & String Formatting

### Basic f-String

An f-string (formatted string literal) lets you embed expressions directly inside a string:

```python
print(f"Thank you! Preparing your {user_input}. Your change is ${change:.2f}.")
```

Anything inside `{}` is evaluated as a Python expression.

### Alignment & Padding

The `:<10` format specifier left-aligns text and pads it to a width of 10 characters:

```python
print(f"{'Water:':<10} {coffee_data.resources['water']}ml")
print(f"{'Milk:':<10} {coffee_data.resources['milk']}ml")
```

This produces a neatly aligned report:
```
Water:     300ml
Milk:      200ml
Coffee:    100g
```

The format mini-language is: `{value:<width}` for left-align, `{value:>width}` for right-align.

### Floating-Point Formatting

`:.2f` formats a float to exactly 2 decimal places:

```python
print(f"${order_cost:.2f}")   # → $2.50
print(f"${change:.2f}")       # → $0.25
```

Without this, floating-point arithmetic can produce values like `2.4999999999` due to binary representation limits.

---

## Type Casting

Converting between types is done with `int()`, `float()`, and `str()`:

```python
order_cost = float(coffee_data.MENU[user_input]['cost'])
coin_choice_amount = int(input("How many of this coin would you like to enter?"))
```

- `input()` always returns a **string** — if you need a number, you must cast it
- `float()` is used for money values to preserve decimal precision
- `int()` is used for coin count since you can't insert half a coin

---

## Variables & Reassignment

Variables in Python are just labels pointing to values. They can be reassigned at any time:

```python
machine_on = True      # boolean
ordering_coffee = None # starts as None (no active order)
ordering_coffee = True # reassigned when an order is placed
ordering_coffee = False # reset after order is fulfilled
```

Using `None` as an initial value is a common Python pattern to indicate "not yet set."

---

## Arithmetic & Compound Assignment

Standard arithmetic used throughout the program:

```python
total_value = coin_choice_amount * selected_coin_value   # multiplication
coin_sum += total_value                                  # compound add-assign
change = coin_sum - order_cost                           # subtraction
```

The `+=` operator is shorthand for `coin_sum = coin_sum + total_value`. Similarly, `-=` is used when deducting resources:

```python
coffee_data.resources[ingredient] -= coffee_data.MENU[order]['ingredients'][ingredient]
```

---

## list() Conversion

Dictionary views (`.keys()`, `.values()`, `.items()`) are not lists — they're dynamic views. Wrapping them in `list()` creates a snapshot:

```python
list(coffee_data.MENU.keys())        # ['espresso', 'latte', 'cappuccino']
list(coffee_data.coin_value.keys())  # ['1', '2', '3', '4']
```

This is needed when you want to index by position (e.g., `[0]`) or when a function requires a concrete list rather than a view object.

```python
selected_coin_data = list(coin_data.items())[0]
coin_face_name, coin_value = selected_coin_data
```

Here, `.items()` is converted to a list so `[0]` can grab the first (and only) key-value pair from the inner dictionary.

---

## Boolean Logic

Boolean values (`True` / `False`) are used as control flags throughout:

```python
machine_on = True       # keeps the main loop alive
ordering_coffee = False # gate for the ordering sub-loop
enough_resources = resource_check(user_input)  # return value of a function
```

These flags let you control program flow without deeply nesting if statements. The pattern of "set a flag, then check it in a while loop" is a common and clean way to manage state in sequential programs.
