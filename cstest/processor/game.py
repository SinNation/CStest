from dataclasses import dataclass
from typing import Any

from cstest.content.variable.variable import DefinedVariable


@dataclass
class GameStatus:
    defined_variables: dict[str, DefinedVariable]
    variable_values: dict[str, Any]
