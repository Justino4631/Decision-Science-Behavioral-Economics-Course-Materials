"""
Shared strategy compile + file-persistence logic.

Both the tkinter UI (ui.py) and the PySide6 UI (ui_qt.py) import this
module so that:
  - "does this code compile and behave like a valid strategy" is checked
    exactly the same way in both apps, and
  - a strategy saved from either app lands in the same custom_strategies/
    folder and is immediately usable from the other app too.
"""
import os
import re

from strategies import STRATEGIES

CUSTOM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_strategies")

_SAFE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def strategy_template(func_name: str = "my_strategy") -> str:
    """Starter source for a brand-new strategy, shared by both UIs so a
    'New strategy' always begins from the same example."""
    return (
        f'def {func_name}(moves: list, strat_idx: int) -> int:\n'
        f'    """Write your own strategy.\n'
        f'    Return 0 for COOPERATE or 1 for DEFECT.\n'
        f'    """\n'
        f'    if not moves:\n'
        f'        return COOPERATE\n\n'
        f'    opp_idx = 1 - strat_idx\n'
        f'    last_opp_move = moves[-1][opp_idx]\n\n'
        f'    # Example logic: copy the opponent\'s last move\n'
        f'    return last_opp_move\n'
    )


def _exec_env():
    return {
        "COOPERATE": 0,
        "DEFECT": 1,
        "random": __import__("random"),
        "math": __import__("math"),
    }


def compile_strategy(code_str: str, func_name: str):
    """Compile + smoke-test a strategy's source.

    Returns the callable, with the exact source text attached as
    ``func.__source__`` (exec'd functions can't be read back with
    inspect.getsource, since they have no real file behind them — this
    is what lets the UI show a saved/loaded strategy's code faithfully).

    Raises ValueError with a human-readable message on any failure;
    both UIs display this message directly.
    """
    func_name = (func_name or "").strip()
    if not func_name:
        raise ValueError("Please provide a function name.")
    if not _SAFE_NAME_RE.match(func_name):
        raise ValueError(
            f"'{func_name}' isn't a valid function name "
            "(letters, numbers, underscores only; can't start with a digit)."
        )

    env = _exec_env()
    try:
        exec(code_str, env)
    except Exception as e:
        raise ValueError(f"Code failed to compile:\n\n{e}")

    if func_name not in env or not callable(env[func_name]):
        raise ValueError(f"Function '{func_name}' was not defined in the code.")

    func = env[func_name]
    try:
        test_res = func([(0, 0), (1, 0)], 0)
    except Exception as e:
        raise ValueError(f"Error while test-running the strategy:\n\n{e}")

    if test_res not in (0, 1):
        raise ValueError("Strategy must return 0 (COOPERATE) or 1 (DEFECT).")

    try:
        func.__source__ = code_str
    except (AttributeError, TypeError):
        pass

    return func


def ensure_custom_dir():
    os.makedirs(CUSTOM_DIR, exist_ok=True)


def write_strategy_file(func_name: str, code_str: str) -> str:
    """Write already-validated source to custom_strategies/<func_name>.py.
    Does not compile or validate — call compile_strategy() first so a
    broken strategy never lands on disk. Returns the file path.
    """
    if not _SAFE_NAME_RE.match(func_name or ""):
        raise ValueError(f"'{func_name}' isn't a valid function/file name.")
    ensure_custom_dir()
    path = os.path.join(CUSTOM_DIR, f"{func_name}.py")
    text = code_str if code_str.endswith("\n") else code_str + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def save_strategy(func_name: str, code_str: str) -> str:
    """Convenience one-shot: compile+test, then persist. Raises
    ValueError if the code doesn't compile/test cleanly — never writes
    a broken file. Returns the saved file's path."""
    compile_strategy(code_str, func_name)
    return write_strategy_file(func_name, code_str)


def load_custom_strategies() -> dict:
    """Load every .py file under custom_strategies/. Each file's own
    name (minus .py) is the function name we look for inside it. Files
    that fail to compile/validate are skipped rather than crashing
    startup — a hand-edited or half-written file just won't show up."""
    ensure_custom_dir()
    found = {}
    for fname in sorted(os.listdir(CUSTOM_DIR)):
        if not fname.endswith(".py"):
            continue
        name = fname[:-3]
        path = os.path.join(CUSTOM_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                code_str = f.read()
            func = compile_strategy(code_str, name)
        except (ValueError, OSError):
            continue
        found[name] = func
    return found


def all_strategies() -> dict:
    """Built-ins plus anything saved to disk. A saved file with the same
    name as a built-in overrides it — the person explicitly re-saved it."""
    catalog = {s.__name__: s for s in STRATEGIES}
    catalog.update(load_custom_strategies())
    return catalog