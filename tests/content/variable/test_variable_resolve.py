from typing import Any

import pytest

from cstest.content.variable import variable_resolve as v
from cstest.content.variable.call_variable import resolver_type
from cstest.content.variable.exceptions import NoVariableNameValue

def_variables = ["var1", "var2", "var3"]


@pytest.mark.parametrize(
    "variable, exp_split",
    [
        (v.ResolveBaseVariable("variablename"), ["variablename"]),
        (v.ResolveBaseVariable("variable[name"), ["variable[name"]),
        (v.ResolveBaseVariable("variable name"), ["variable name"]),
        (v.ResolveBracketVariable("variable[name]"), ["variable", "name]"]),
        (
            v.ResolveBracketVariable("variable[name[next]]"),
            ["variable", "name", "next]]"],
        ),
        (
            v.ResolveBracketVariable("[variable][name]"),
            ["", "variable]", "name]"],
        ),
    ],
)
def test_splitter(variable: resolver_type, exp_split: list[str]) -> None:
    assert variable.splitter() == exp_split


@pytest.mark.parametrize(
    "variable, exp_errors",
    [
        (v.ResolveBaseVariable("var1"), []),
        (
            v.ResolveBaseVariable("1var1"),
            ["Variable name must start with a letter. Variable: 1var1"],
        ),
        (
            v.ResolveBaseVariable("v$ar1"),
            ["Variable contains an invalid symbol. Variable: v$ar1"],
        ),
        (
            v.ResolveBaseVariable("1var 1"),
            [
                "Variable name must start with a letter. Variable: 1var 1",
                "Variable contains an invalid symbol. Variable: 1var 1",
            ],
        ),
        (v.ResolveBracketVariable("var1[var2]"), []),
        (v.ResolveBracketVariable("var1[var2][var3[var4]]"), []),
        (v.ResolveBracketVariable("var1[var2[var3]]"), []),
        (
            v.ResolveBracketVariable("var1[var2][var3"),
            [
                "Variable does not contain equal number of '[' and ']'."
                " Variable: var1[var2][var3"
            ],
        ),
        (
            v.ResolveBracketVariable("var1var2][var3]"),
            [
                "Variable does not contain equal number of '[' and ']'."
                " Variable: var1var2][var3]"
            ],
        ),
        (
            v.ResolveBracketVariable("4var1[var2[var3]]"),
            ["Variable name must start with a letter. Variable: 4var1"],
        ),
        (
            v.ResolveBracketVariable("var1)[var2][var3]"),
            ["Variable contains an invalid symbol. Variable: var1)"],
        ),
        (
            v.ResolveBracketVariable("1var1)[var2][var3]"),
            [
                "Variable name must start with a letter. Variable: 1var1)",
                "Variable contains an invalid symbol. Variable: 1var1)",
            ],
        ),
        (
            v.ResolveBracketVariable("[var1][var2][var3]"),
            ["Variable name must start with a letter. Variable: [var1][var2][var3]"],
        ),
        #     (v.ResolveBracketHashVariable("var1[var2#1]"), True, ""),
        #     (
        #         v.ResolveBracketHashVariable("var10[var2#1#2]"),
        #         False,
        #         "Variable name should only contain a single"
        #         " pair of square brackets and a single #. Variable: var10[var2#1#2]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var10[var2##1]"),
        #         False,
        #         "Variable name should only contain a single"
        #         " pair of square brackets and a single #. Variable: var10[var2##1]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var10[[var2#2]]"),
        #         False,
        #         "Variable name should only contain a single"
        #         " pair of square brackets and a single #. Variable: var10[[var2#2]]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var10#1[var2#1#2]"),
        #         False,
        #         "Variable name should only contain a single"
        #         " pair of square brackets and a single #. Variable:"
        #         " var10#1[var2#1#2]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var10[var2#1]"),
        #         False,
        #         "Variable name is not defined in a *create"
        #         " or *temp command. Variable: var10[var2#1]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var1[var20#1]"),
        #         False,
        #         "Variable name is not defined in a *create or *temp command."
        #         " Variable: var1[var20#1]",
        #     ),
        #     (
        #         v.ResolveBracketHashVariable("var1[var2#a]"),
        #         False,
        #         "Value following a # must be an integer. Variable: var1[var2#a]",
        #     ),
    ],
)
def test_validate_struct(variable: resolver_type, exp_errors: list[str]) -> None:
    assert variable.validate_struct() == exp_errors


@pytest.mark.parametrize(
    "variable",
    [
        (v.ResolveBaseVariable("")),
        (v.ResolveBaseVariable("  ")),
        (v.ResolveBracketVariable("")),
        (v.ResolveBracketVariable(" ")),
    ],
)
def test_validate_struct_exception(variable: resolver_type) -> None:
    with pytest.raises(NoVariableNameValue):
        variable.validate_struct()


def_variables = [
    "var_1_2_3",
    "var_1_2_3_4",
    "var_2_3_4",
    "var_1",
    "var_2",
    "var_3",
    "var_4",
    "var_5",
    "var_6",
    "var_2_3",
    "var_1_2",
    "var_1_2",
    "var_1_6",
    "var_4_5",
]
game_variables: dict[str, Any] = {
    "var_1_2_3": "SUCCESS",
    "var_1_2_3_4": "SUCCESS",
    "var_2_3_4": "SUCCESS",
    "var_1": 1,
    "var_2": 2,
    "var_3": 3,
    "var_4": 4,
    "var_5": 5,
    "var_6": 6,
    "var_2_3": 2,
    "var_1_2": "1_2_3",
    "var_1_6": "1_2",
    "var_4_5": 4,
}


@pytest.mark.parametrize(
    "variable, exp_errors, exp_name, exp_value",
    [
        (v.ResolveBaseVariable("var_1"), [], "var_1", 1),
        (
            v.ResolveBaseVariable("var10"),
            [
                "Variable name is not defined in a *create or *temp command."
                " Variable: var10"
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVariable("var[var_1][var_2][var_3]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVariable("var[var_1[var_2[var_3]]]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVariable("var[var_1][var_2][var[var_3]]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVariable("var[var_1[var_6]][var_3][var_4]"),
            [],
            "var_1_2_3_4",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVariable("var[var[var_2]][var_3][var_4[var_5]]"),
            [],
            "var_2_3_4",
            "SUCCESS",
        ),
    ],
)
def test_resolver_valid_struct(
    variable: resolver_type, exp_errors: list[str], exp_name: str, exp_value: Any
) -> None:
    errors, name, value = variable.resolve(def_variables, game_variables)
    assert errors == exp_errors and name == exp_name and value == exp_value
