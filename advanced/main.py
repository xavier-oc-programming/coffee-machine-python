import sys
from pathlib import Path

# Ensure sibling modules resolve correctly regardless of working directory.
sys.path.insert(0, str(Path(__file__).parent))

from config import CMD_OFF, CMD_REPORT, CMD_REFILL, REFILLABLE
from machine import CoffeeMachine
from drink_menu import DrinkMenu
from coin_processor import CoinProcessor
from display import Display


def main() -> None:
    machine = CoffeeMachine()
    menu    = DrinkMenu()
    coins   = CoinProcessor()
    display = Display()

    display.show_startup()

    while True:
        user_input = display.prompt_drink()

        # ── Commands ──────────────────────────────────────────────────────────
        if user_input == CMD_OFF:
            display.show_shutdown()
            break

        if user_input == CMD_REPORT:
            display.show_report(machine.get_report())
            continue

        # ── Refill ────────────────────────────────────────────────────────────
        if user_input == CMD_REFILL:
            display.show_refill_all(machine.refill_all())
            continue

        if user_input.startswith(CMD_REFILL + " "):
            ingredient = user_input[len(CMD_REFILL) + 1:]
            if ingredient in REFILLABLE:
                display.show_refill_one(ingredient, machine.refill_one(ingredient))
            else:
                display.show_refill_invalid(ingredient)
            continue

        # ── Order validation ──────────────────────────────────────────────────
        if not menu.is_valid(user_input):
            display.show_invalid_input(user_input)
            continue

        display.show_checking(user_input)

        # ── Resource check ────────────────────────────────────────────────────
        missing = machine.check_resources(user_input)
        if missing:
            display.show_insufficient_resources(missing)
            continue

        # ── Payment ───────────────────────────────────────────────────────────
        cost = menu.get_cost(user_input)
        display.show_order_cost(user_input, cost)
        display.show_coin_menu()

        coin_sum: float = 0.0
        while coin_sum < cost:
            key = display.prompt_coin()
            if not coins.is_valid_coin(key):
                display.show_invalid_coin()
                continue
            name  = coins.get_coin_name(key)
            value = coins.get_coin_value(key)
            qty   = display.prompt_coin_amount(name)
            batch = round(value * qty, 2)
            coin_sum = round(coin_sum + batch, 2)
            display.show_coin_added(name, batch, coin_sum)

        # ── Dispense ──────────────────────────────────────────────────────────
        change = coins.calculate_change(coin_sum, cost)
        machine.deduct_resources(user_input)
        machine.add_revenue(cost)
        display.show_change(user_input, change)


if __name__ == "__main__":
    main()
