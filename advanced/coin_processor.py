from config import COIN_TYPES


class CoinProcessor:
    """Pure payment logic. No UI, no print()."""

    def is_valid_coin(self, key: str) -> bool:
        """Return True if key corresponds to a valid coin type."""
        return key in COIN_TYPES

    def get_coin_name(self, key: str) -> str:
        """Return the display name of a coin (e.g. 'Quarter')."""
        return COIN_TYPES[key]["name"]

    def get_coin_value(self, key: str) -> float:
        """Return the dollar value of a coin (e.g. 0.25)."""
        return COIN_TYPES[key]["value"]

    def calculate_change(self, inserted: float, cost: float) -> float:
        """Return the change owed, rounded to 2 decimal places."""
        return round(inserted - cost, 2)
