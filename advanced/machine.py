from pathlib import Path
from config import STARTING_WATER, STARTING_MILK, STARTING_COFFEE, MENU

_DATA_FILE = Path(__file__).parent / "data.txt"


class CoffeeMachine:
    """Tracks session resources and persists lifetime revenue to data.txt."""

    def __init__(self) -> None:
        self.water:            int   = STARTING_WATER
        self.milk:             int   = STARTING_MILK
        self.coffee:           int   = STARTING_COFFEE
        self.session_revenue:  float = 0.0
        self.lifetime_revenue: float = self._load_lifetime_revenue()

    # ── Resource checks ───────────────────────────────────────────────────────

    def check_resources(self, drink_name: str) -> str | None:
        """Return the name of the first insufficient ingredient, or None if OK."""
        stock = {"water": self.water, "milk": self.milk, "coffee": self.coffee}
        for ingredient, amount in MENU[drink_name]["ingredients"].items():
            if amount > stock[ingredient]:
                return ingredient
        return None

    def deduct_resources(self, drink_name: str) -> None:
        """Deduct ingredients consumed by the given drink."""
        for ingredient, amount in MENU[drink_name]["ingredients"].items():
            setattr(self, ingredient, getattr(self, ingredient) - amount)

    # ── Revenue ───────────────────────────────────────────────────────────────

    def add_revenue(self, amount: float) -> None:
        """Add a sale amount to both session and lifetime revenue."""
        self.session_revenue  = round(self.session_revenue  + amount, 2)
        self.lifetime_revenue = round(self.lifetime_revenue + amount, 2)
        self._save_lifetime_revenue()

    # ── Report ────────────────────────────────────────────────────────────────

    def get_report(self) -> dict[str, int | float]:
        return {
            "water":            self.water,
            "milk":             self.milk,
            "coffee":           self.coffee,
            "session_revenue":  self.session_revenue,
            "lifetime_revenue": self.lifetime_revenue,
        }

    # ── Persistence ───────────────────────────────────────────────────────────

    def _load_lifetime_revenue(self) -> float:
        try:
            return float(_DATA_FILE.read_text().strip())
        except (FileNotFoundError, ValueError):
            return 0.0

    def _save_lifetime_revenue(self) -> None:
        _DATA_FILE.write_text(f"{self.lifetime_revenue:.2f}")
