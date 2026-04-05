# ── Starting Resources ────────────────────────────────────────────────────────
STARTING_WATER:  int = 300      # ml
STARTING_MILK:   int = 200      # ml
STARTING_COFFEE: int = 100      # g

# ── Menu ──────────────────────────────────────────────────────────────────────
MENU: dict[str, dict] = {
    "espresso": {
        "ingredients": {"water": 50, "coffee": 18},
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 3.0,
    },
}

# ── Coins ─────────────────────────────────────────────────────────────────────
COIN_TYPES: dict[str, dict] = {
    "1": {"name": "Penny",   "value": 0.01},
    "2": {"name": "Nickel",  "value": 0.05},
    "3": {"name": "Dime",    "value": 0.10},
    "4": {"name": "Quarter", "value": 0.25},
}

# ── Commands ──────────────────────────────────────────────────────────────────
CMD_OFF:    str = "off"
CMD_REPORT: str = "report"

# ── Formatting ────────────────────────────────────────────────────────────────
REPORT_LABEL_WIDTH: int = 10    # left-column width for resource report rows
COIN_NAME_WIDTH:    int = 10    # left-column width for coin menu rows
