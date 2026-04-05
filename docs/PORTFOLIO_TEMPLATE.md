# Portfolio Project Template

Copy the prompt below, fill in every `[ ]` placeholder, and paste it to Claude.
Delete whichever variant block (CLI or Tkinter) does not apply.

---

```
Restructure this repo to match my standard portfolio structure.
Follow every instruction exactly — do not invent alternatives.

────────────────────────────────────────
FILL IN BEFORE SENDING
────────────────────────────────────────
Project name (slug)  : [my-project-python]
One-line description : [What the program does in one sentence]
Build type           : [CLI | Tkinter]
Course day           : [Day XX]
GitHub username      : [xavier-oc-programming]

Original files       : [list every file currently in the repo]
Main entry point     : [main.py / game.py / etc.]

Known classes (if any already exist in the course files):
  [ClassName → what it does]
  [ClassName → what it does]

Known constants (speeds, sizes, colours, etc.):
  [CONSTANT_NAME = value  # description]
  [CONSTANT_NAME = value  # description]

Persisted data (if any): [high score / revenue / none]

────────────────────────────────────────
REPO SETUP
────────────────────────────────────────
The repo already exists at github.com/[username]/[my-project-python].
Both `main` and `original` branches already exist as identical
starting snapshots. Build the full structure on main only.
No Co-Authored-By lines in any commit.

────────────────────────────────────────
ROOT LEVEL
────────────────────────────────────────
menu.py
  - Import and print LOGO from art.py
  - Clear console BEFORE printing menu every loop iteration:
      os.system("cls" if os.name == "nt" else "clear")
  - while True loop — menu reappears automatically after
    subprocess.run() returns. No recursion, no re-calling main().
  - Launch with:
      subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
    cwd= is critical — makes sibling imports inside the subprocess
    resolve correctly without installed packages or relative imports.
  - Option 1 → original/[main.py]
  - Option 2 → advanced/[main.py]
  - q → break  (exits the launcher entirely)
  - Any other input → print("Invalid choice. Try again.") and loop

art.py
  - LOGO = r"""..."""  ASCII art logo for this project, printed by menu.py

requirements.txt
  - Standard library only — no pip install required
  - Note Python 3.10+ for X | Y union types and tuple[...] hints
  [ADD any third-party packages here if applicable, e.g. tkinter note]

.gitignore:
  **/__pycache__/
  .DS_Store
  .idea/
  .vscode/
  *.py[cod]

README.md  (see README spec at the bottom)
docs/COURSE_NOTES.md  — original course exercise description

────────────────────────────────────────
original/
────────────────────────────────────────
Copy all course files verbatim. Only permitted change: fix any
hardcoded file paths using Path(__file__).parent where needed.
No logic changes whatsoever.

────────────────────────────────────────
advanced/ — shared architecture rules
────────────────────────────────────────
- All logic modules → zero UI imports, zero print(), zero input()
- display.py → owns ALL rendering and ALL user interaction
- main.py → orchestrator only: input → logic → display
- config.py → every constant; zero magic numbers anywhere else
- Type hints throughout (Python 3.10+: use X | Y, tuple[...])
- Path(__file__).parent for all file paths

advanced/main.py must begin with:
  import sys
  from pathlib import Path
  sys.path.insert(0, str(Path(__file__).parent))
This ensures sibling imports work whether launched via menu.py
(cwd=advanced/) or run directly from the repo root.

────────────────────────────────────────
▼ CLI VARIANT — delete if Tkinter
────────────────────────────────────────
advanced/config.py
  Group constants by category with comments:
  # Screen / Console
  # [Domain-specific group, e.g. Player / Cars / Board]
  # Scoring / levels  (if applicable)
  # Display / formatting
  No magic numbers anywhere else in the codebase.

advanced/[logic_module_1].py — class [ClassName]
  Pure logic. No print(), no input(), no UI imports.
  [List methods and what they do]

advanced/[logic_module_2].py — class [ClassName]
  Pure logic. No print(), no input(), no UI imports.
  [List methods and what they do]

advanced/display.py — class Display
  Owns ALL print() and input() calls.
  On startup, print a command reference before the first prompt:
    print("[Project name] ready.")
    print("  [Prompt lines listing all valid commands]")
  Use a simple >> prompt for all main input.
  No business logic lives here.

  Methods:
    show_startup() → None
    prompt_[action]() → str | int
    show_[state](...) → None
    [list all display methods needed]

advanced/main.py — orchestrator
  Instantiate all logic classes and Display.
  Call display.show_startup() once before the main loop.
  Main loop pattern:
    while True:
        user_input = display.prompt_[action]()
        if user_input == CMD_OFF: ...break
        if user_input == CMD_[X]: ...continue
        [validate → logic → display, no business logic here]

advanced/data.txt  (if persistence needed)
  Start at 0 or 0.00. One value, no trailing whitespace.

────────────────────────────────────────
▼ TKINTER VARIANT — delete if CLI
────────────────────────────────────────
advanced/config.py
  Group constants by category with comments:
  # Screen
  # [Domain-specific group]
  # Colours
  # Fonts
  # Timing / delays
  # Scoring / levels  (if applicable)
  No magic numbers anywhere else in the codebase.

advanced/[logic_module_1].py — class [ClassName]
  Pure logic. No tkinter imports, no print(), no UI.
  [List methods and what they do]

advanced/[logic_module_2].py — class [ClassName]
  Pure logic. No tkinter imports, no print(), no UI.
  [List methods and what they do]

advanced/display.py — class Display
  Owns the Tk root window and every widget.
  No game/app logic lives here.

  ---- Window setup ----
  __init__: create root, set title/size from config, build all widgets.
  Call root.after() for the game loop, NOT root.mainloop() inside __init__.
  root.mainloop() is called once at the end of main().

  ---- Overlay pattern (for pause, game over, welcome screens) ----
  Use a Toplevel or Canvas overlay drawn on top of frozen game state.
  Do NOT destroy the main window on R (return to title) —
  hide/show widgets instead. The window NEVER closes on R.
  close() must call sys.exit(0), NOT root.destroy() alone,
  to avoid tkinter cleanup errors in subprocess context.

  ---- Key binding rules ----
  Use root.bind("<KeyPress-x>") for all held keys (movement).
  Use root.bind("<Key-x>") for single-fire actions (pause, select).
  Always root.focus_set() after building the window.
  Always rebind keys after any overlay exits.

  Methods:
    render_[element](...) → None
    show_welcome() → str | None   ("start" or None for quit)
    show_pause() → bool           (True = resume, False = title)
    show_game_over() → bool       (True = play again, False = title)
    show_level_up(level) → None
    close() → None                (sys.exit(0))

advanced/main.py — orchestrator
  GameState class with reset() method.
  Outer while True loop (title → game → title):
    - reset state, call display.show_welcome()
    - None from show_welcome → display.close()
    - Inner game loop driven by root.after() callbacks
    - Pause: unbind Space before overlay, rebind after
    - R from any overlay → break inner loop → outer → title screen
    - Window NEVER closes on R
  Call root.mainloop() once at the very end of main().

advanced/data.txt  (if persistence needed)
  Start at 0. One integer, no trailing whitespace.

────────────────────────────────────────
README spec
────────────────────────────────────────
Sections:
  1. Quick start
       python menu.py → select 1 or 2, or run builds directly
  2. Builds comparison table (original vs advanced, feature by feature)
  3. Commands / Controls
       CLI: one table listing every valid >> prompt input
       Tkinter: one table per context (title / gameplay / pause / game over)
       Include the startup banner text for CLI builds
  4. [Gameplay rules / Ordering flow / App flow — name it what fits]
       Step-by-step description of what happens during a session
  5. Features
       Both builds first, then advanced-only
       Each feature as its own paragraph with a bold heading
  6. Navigation flow — TWO separate diagrams:
       a) Terminal menu tree: menu.py → 1/2/q paths
       b) In-app flow: each state as a labelled box,
          every key/input and its destination on its own line
       For Tkinter: callout note "R never closes the window"
  7. Architecture — annotated file tree with inline comments
  8. Module reference — every public method on every class,
       formatted as a table: Method | Returns | Description
  9. Configuration reference — table: Constant | Default | Description
  10. [Session flow diagram (CLI) | Display layout (Tkinter)]
       CLI: ASCII art showing the full prompt → outcome flow
       Tkinter: ASCII diagram of the window with coordinate labels
  11. Design decisions — explain WHY for each key architectural choice:
       - display.py owns all I/O (testability, swappability)
       - config.py zero magic numbers (single source of truth)
       - sys.path.insert pattern (works from menu.py AND directly)
       - subprocess.run + cwd= (sibling import resolution)
       - while True in menu.py vs recursion (no stack growth)
       - Console cleared before every menu render (clean UX)
       - [Add project-specific decisions here]
       Tkinter-specific:
       - sys.exit(0) vs root.destroy() (avoids tkinter cleanup errors)
       - Two nested loops vs state machine (title → game → title)
       - Space unregistration before overlays (prevent double-fire)
       - onkeypress vs onkey (press fires on hold; release fires once)
       - Window never closes on R (same Tk instance throughout)
  12. Course context
       Built as Day [XX] of 100 Days of Code by Dr. Angela Yu.
       Concepts covered in the original build: [list them]
       The advanced build extends into: [OOP / tkinter / etc.]
       See docs/COURSE_NOTES.md for full concept breakdown.
  13. Dependencies table — Module | Used in | Purpose

────────────────────────────────────────
COMMIT RULES
────────────────────────────────────────
- No Co-Authored-By lines in any commit message
- Commit after each logical unit of work
- Push main to origin after every commit
- Do not push the original branch (it stays as the starting snapshot)
```

---

## Checklist before sending

- [ ] Filled in all `[ ]` placeholders
- [ ] Deleted the variant block that doesn't apply (CLI or Tkinter)
- [ ] Listed all existing class names from the course files
- [ ] Listed all known constants (speeds, sizes, colours, etc.)
- [ ] Specified whether there is a high score / persistence or not
- [ ] Confirmed the GitHub repo and both branches already exist

## Notes

**Starting a new repo from scratch?** Add this before the REPO SETUP block:

```
Create a GitHub repo called [my-project-python].
Push the current course files to both `main` and `original` branches
as identical starting snapshots. Then build the full structure on main.
```

**Multiple game modes or difficulty levels?** Add them as options 3, 4, etc.
in menu.py and as additional subfolders (e.g. `hard/`, `auto/`).

**No original course files?** Skip the `original/` folder and start directly
with the advanced build. Remove option 1 from menu.py.
