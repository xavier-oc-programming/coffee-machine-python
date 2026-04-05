import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

ROOT = Path(__file__).parent


def main() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(LOGO)
        print("  Select a version to run:")
        print("  ─────────────────────────")
        print("  1   Original  (procedural, course build)")
        print("  2   Advanced  (OOP refactor)")
        print("  q   Quit")
        print()
        choice = input("  Enter your choice: ").strip().lower()

        if choice == "1":
            path = ROOT / "original" / "main.py"
            subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
        elif choice == "2":
            path = ROOT / "advanced" / "main.py"
            subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
        elif choice == "q":
            break
        else:
            print("\n  Invalid choice. Try again.")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    main()
