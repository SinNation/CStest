import os
from typing import Any


def highlight(text: Any, bold: bool = False) -> str:
    return ("\033[1m" if bold else "") + f"\033[96m{text}\033[0m"


def banner(text: str) -> None:
    size = os.get_terminal_size()
    print(highlight(f"{ text :~^{size.columns}}", bold=True))


def welcome() -> None:
    banner("welcome to cstest")
    print(
        """NOTE: The cstest folder must be in the same folder as your Choicescript projects.
    Otherwise the tool will not be able to find your project."""
    )
