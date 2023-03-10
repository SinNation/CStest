from typing import Any
import os


def highlight(text: Any, bold: bool = False) -> str:
    return ("\033[1m" if bold else "") + f"\033[96m{text}\033[0m"


def banner(text: str) -> None:
    size = os.get_terminal_size()
    print(highlight(f"{ text :~^{size.columns}}", bold=True))


def welcome() -> None:
    banner("cstest")
    print(
        """Welcome to CStest. An automated testing tool for Choicescript.
    NOTE: The cstest folder must be in the same folder as your Choicescript projects.
    Otherwise the tool will not be able to find your project."""
    )
