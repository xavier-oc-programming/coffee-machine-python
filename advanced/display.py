from config import COIN_TYPES, MENU, REPORT_LABEL_WIDTH, COIN_NAME_WIDTH


class Display:
    """Owns ALL terminal I/O. No game logic lives here — only print() and input()."""

    # ── Prompts ───────────────────────────────────────────────────────────────

    def show_startup(self) -> None:
        """Print the command reference shown once when the machine starts."""
        drink_names = " / ".join(MENU.keys())
        print("\nCoffee Machine ready.")
        print(f"  Orders  : {drink_names}")
        print("  Commands: report / refill / refill <ingredient> / off\n")

    def prompt_drink(self) -> str:
        """Prompt for a drink order and return the input as lowercase string."""
        return input(">> ").strip().lower()

    def prompt_coin(self) -> str:
        """Prompt for a coin type selection and return the raw input."""
        return input("  Enter coin number: ").strip()

    def prompt_coin_amount(self, coin_name: str) -> int:
        """Prompt for coin quantity. Loops until a valid integer is entered."""
        while True:
            try:
                return int(input(f"  How many {coin_name}s? "))
            except ValueError:
                print("  Please enter a whole number.")

    # ── Output ────────────────────────────────────────────────────────────────

    def show_report(self, report: dict[str, int | float]) -> None:
        """Print current resource levels and revenue."""
        print()
        print(f"  {'Water:':<{REPORT_LABEL_WIDTH}} {report['water']}ml")
        print(f"  {'Milk:':<{REPORT_LABEL_WIDTH}} {report['milk']}ml")
        print(f"  {'Coffee:':<{REPORT_LABEL_WIDTH}} {report['coffee']}g")
        print(f"  {'Revenue:':<{REPORT_LABEL_WIDTH}} ${report['session_revenue']:.2f}  "
              f"(lifetime: ${report['lifetime_revenue']:.2f})")

    def show_coin_menu(self) -> None:
        """Print the coin selection menu."""
        print("\n  Coin Menu:")
        for key, data in COIN_TYPES.items():
            print(f"  {key}: {(data['name'] + ':'):<{COIN_NAME_WIDTH}} ${data['value']:.2f}")

    def show_order_cost(self, drink: str, cost: float) -> None:
        print(f"\n  Your {drink} costs ${cost:.2f}. Please insert coins.")

    def show_coin_added(self, name: str, batch_value: float, total: float) -> None:
        print(f"  Added {name} (${batch_value:.2f}). Running total: ${total:.2f}")

    def show_change(self, drink: str, change: float) -> None:
        print(f"\n  Preparing your {drink}... "
              f"Here is ${change:.2f} in change. Enjoy!")

    def show_checking(self, drink: str) -> None:
        print(f"\n  Checking resources for {drink}...")

    def show_insufficient_resources(self, ingredient: str) -> None:
        print(f"  Sorry, not enough {ingredient} to make that drink.")

    def show_invalid_input(self, text: str) -> None:
        print(f'  Could not process "{text}". Please try again.')

    def show_invalid_coin(self) -> None:
        print("  Invalid coin. Please choose a number from the menu.")

    def show_refill_all(self, amounts: dict[str, int]) -> None:
        print("\n  Refilled all ingredients:")
        units = {"water": "ml", "milk": "ml", "coffee": "g"}
        for ingredient, amount in amounts.items():
            print(f"    {ingredient.capitalize()}: {amount}{units[ingredient]}")

    def show_refill_one(self, ingredient: str, amount: int) -> None:
        units = {"water": "ml", "milk": "ml", "coffee": "g"}
        print(f"\n  Refilled {ingredient}: {amount}{units[ingredient]}")

    def show_refill_invalid(self, ingredient: str) -> None:
        print(f'  "{ingredient}" is not a refillable ingredient. '
              f"Try: water / milk / coffee")

    def show_shutdown(self) -> None:
        print("\n  Coffee machine is turning off...\n  Have a nice day!")
