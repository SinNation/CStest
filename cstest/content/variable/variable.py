from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from cstest.processor.game import GameStatus


@dataclass
class DefinedVariable:
    name: str
    var_type: str


@dataclass  # type: ignore
class CalledVariable(ABC):
    constructed_name: str
    name: DefinedVariable = field(init=False)

    @abstractmethod
    def splitter(self) -> list[str]:
        pass

    @abstractmethod
    def validator(self, game_status: GameStatus) -> bool:
        pass

    @abstractmethod
    def resolver(self, game_status: GameStatus) -> None:
        pass


@dataclass
class CalledBaseVariable(CalledVariable):
    constructed_name: str
    name: DefinedVariable = field(init=False)

    def splitter(self) -> list[str]:
        return [self.constructed_name]

    def validator(self, game_status: GameStatus) -> bool:
        return self.constructed_name in game_status.defined_variables.keys()

    def resolver(self, game_status: GameStatus) -> None:
        self.name = game_status.defined_variables[self.constructed_name]


@dataclass
class CalledBracketVariable(CalledVariable):
    constructed_name: str
    name: DefinedVariable = field(init=False)

    def splitter(self) -> list[str]:
        return self.constructed_name.split("[")

    def validator(self, game_status: GameStatus) -> bool:
        try:
            split_variable = self.splitter()

            if len(split_variable) == 2:
                if split_variable[0] in game_status.defined_variables.keys():
                    if (
                        split_variable[1].replace("]", "")
                        in game_status.defined_variables.keys()
                    ):
                        return True
            return False
        except Exception:
            return False

    def resolver(self, game_status: GameStatus) -> None:
        split_variable = self.splitter()
        suffix_lkp = split_variable[1].replace("]", "")
        suffix = game_status.variable_values[suffix_lkp]
        self.name = game_status.defined_variables[f"{split_variable[0]}_{suffix}"]


@dataclass
class CalledBracketHashVariable(CalledVariable):
    constructed_name: str
    name: DefinedVariable = field(init=False)

    def splitter(self) -> list[str]:
        split_variable = self.constructed_name.split("[")
        split_suffix = split_variable[1].split("#")
        return [split_variable[0], split_suffix[0], split_suffix[1].replace("]", "")]

    def validator(self, game_status: GameStatus) -> bool:
        try:
            split_variable = self.splitter()

            if len(split_variable) == 3:
                if split_variable[0] in game_status.defined_variables.keys():
                    if split_variable[1] in game_status.defined_variables.keys():
                        if isinstance(split_variable[2], int):
                            return True
            return False
        except Exception:
            return False

    def resolver(self, game_status: GameStatus) -> None:
        split_variable = self.splitter()
        suffix_val = game_status.variable_values[split_variable[1]]
        suffix = suffix_val[split_variable[2]]
        self.name = game_status.defined_variables[f"{split_variable[0]}_{suffix}"]
