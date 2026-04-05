from config import MENU


class DrinkMenu:
    """Read-only access to the drink menu. No UI, no print()."""

    def get_names(self) -> list[str]:
        """Return all available drink names."""
        return list(MENU.keys())

    def is_valid(self, name: str) -> bool:
        """Return True if name matches a menu item."""
        return name in MENU

    def get_cost(self, drink_name: str) -> float:
        """Return the price of a drink in dollars."""
        return float(MENU[drink_name]["cost"])

    def get_ingredients(self, drink_name: str) -> dict[str, int]:
        """Return the ingredient requirements for a drink."""
        return MENU[drink_name]["ingredients"]
