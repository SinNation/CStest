from typing import Any

import pytest

from cstest.content.variable import variable_resolve as v
from cstest.content.variable.call_variable import resolver_type
from cstest.content.variable.exceptions import NoVariableNameValue

def_variables = ["var1", "var2", "var3"]


@pytest.mark.parametrize(
    "variable, exp_split",
    [
        (v.ResolveBaseVar("variablename"), ["variablename"]),
        (v.ResolveBaseVar("variable[name"), ["variable[name"]),
        (v.ResolveBaseVar("variable name"), ["variable name"]),
        (v.ResolveHashVar("variable[name]#1"), ["variable[name]", "1"]),
        (v.ResolveHashVar("var#12"), ["var", "12"]),
        (v.ResolveHashVar("var#1 2"), ["var", "1 2"]),
        (v.ResolveBracketVar("variable[name]"), ["variable", "name]"]),
        (v.ResolveBracketVar("variable[nam#e]"), ["variable", "nam#e]"]),
        (
            v.ResolveBracketVar("variable[name[next]]"),
            ["variable", "name", "next]]"],
        ),
        (
            v.ResolveBracketVar("[variable][name]"),
            ["", "variable]", "name]"],
        ),
    ],
)
def test_splitter(variable: resolver_type, exp_split: list[str]) -> None:
    assert variable.splitter() == exp_split


@pytest.mark.parametrize(
    "variable, exp_errors",
    [
        (v.ResolveBaseVar("var1"), []),
        (
            v.ResolveBaseVar("1var1"),
            ["Variable name must start with a letter. Variable: 1var1"],
        ),
        (
            v.ResolveBaseVar("v$ar1"),
            ["Variable contains an invalid symbol. Variable: v$ar1"],
        ),
        (
            v.ResolveBaseVar("1var 1"),
            [
                "Variable name must start with a letter. Variable: 1var 1",
                "Variable contains an invalid symbol. Variable: 1var 1",
            ],
        ),
        (v.ResolveHashVar("var#1"), []),
        (
            v.ResolveHashVar("var#1#2"),
            ["Variable name can not contain more than one #. Variable: var#1#2"],
        ),
        (
            v.ResolveHashVar("1var#1#2"),
            ["Variable name can not contain more than one #. Variable: 1var#1#2"],
        ),
        (
            v.ResolveHashVar("1-var#a"),
            [
                "Variable name must start with a letter. Variable: 1-var",
                "Variable contains an invalid symbol. Variable: 1-var",
                "Value following a # must be a number. Variable: 1-var#a",
            ],
        ),
        (v.ResolveBracketVar("var1[var2]"), []),
        (v.ResolveBracketVar("var1[var2][var3[var4]]"), []),
        (v.ResolveBracketVar("var1[var2[var3]]"), []),
        (v.ResolveBracketVar("var1[var2#1]"), []),
        (v.ResolveBracketVar("var1[var2#2][var3[var4#1]]"), []),
        (
            v.ResolveBracketVar("var1[var2][var3"),
            [
                "Variable does not contain equal number of '[' and ']'."
                " Variable: var1[var2][var3"
            ],
        ),
        (
            v.ResolveBracketVar("var1var2][var3]"),
            [
                "Variable does not contain equal number of '[' and ']'."
                " Variable: var1var2][var3]"
            ],
        ),
        (
            v.ResolveBracketVar("4var1[var2[var3]]"),
            ["Variable name must start with a letter. Variable: 4var1"],
        ),
        (
            v.ResolveBracketVar("var1)[var2][var3]"),
            ["Variable contains an invalid symbol. Variable: var1)"],
        ),
        (
            v.ResolveBracketVar("1var1)[var2][var3]"),
            [
                "Variable name must start with a letter. Variable: 1var1)",
                "Variable contains an invalid symbol. Variable: 1var1)",
            ],
        ),
        (
            v.ResolveBracketVar("[var1][var2][var3]"),
            ["Variable name must start with a letter. Variable: [var1][var2][var3]"],
        ),
        (
            v.ResolveBracketVar("var10[var2#1#2]"),
            ["Variable name can not contain more than one #. Variable: var2#1#2"],
        ),
        (
            v.ResolveBracketVar("var10#1[var2#2]"),
            [
                "Use of # must always occur within a single set of []. You can not"
                " slice a variable value that is being used to construct a full"
                " variable name. Variable: var10#1[var2#2]"
            ],
        ),
        (
            v.ResolveBracketVar("var[var2#2[var3]]"),
            [
                "Use of # must always occur within a single set of []. You can not"
                " slice a variable value that is being used to construct a full"
                " variable name. Variable: var[var2#2[var3]]"
            ],
        ),
        (
            v.ResolveBracketVar("var10[var2#a]"),
            ["Value following a # must be a number. Variable: var2#a"],
        ),
        (
            v.ResolveBracketVar("[var10#1[[-var2##a]"),
            [
                "Variable name must start with a letter. Variable: [var10#1[[-var2##a]",
                "Variable does not contain equal number of '[' and ']'. Variable:"
                " [var10#1[[-var2##a]",
            ],
        ),
        (
            v.ResolveBracketVar("1var10#a[-var2##2]"),
            [
                "Variable name must start with a letter. Variable: 1var10a",
                "Use of # must always occur within a single set of []. You can not"
                " slice a variable value that is being used to construct a full"
                " variable name. Variable: 1var10#a[-var2##2]",
                "Variable name must start with a letter. Variable: 1var10",
                "Value following a # must be a number. Variable: 1var10#a",
                "Variable name must start with a letter. Variable: -var22]",
                "Variable contains an invalid symbol. Variable: -var22]",
                "Variable name can not contain more than one #. Variable: -var2##2",
            ],
        ),
    ],
)
def test_validate_struct(variable: resolver_type, exp_errors: list[str]) -> None:
    assert variable.validate_struct() == exp_errors


@pytest.mark.parametrize(
    "variable",
    [
        (v.ResolveBaseVar("")),
        (v.ResolveBaseVar("  ")),
        (v.ResolveHashVar("")),
        (v.ResolveHashVar(" ")),
        (v.ResolveBracketVar("")),
        (v.ResolveBracketVar(" ")),
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
    "var_33",
    "var_4",
    "var_44",
    "var_5",
    "var_6",
    "var_2_3",
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
    "var_33": 13,
    "var_4": 4,
    "var_44": 35474,
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
        (v.ResolveBaseVar("var_1"), [], "var_1", 1),
        (
            v.ResolveBaseVar("var10"),
            [
                "Variable name is not defined in a *create or *temp command."
                " Variable: var10"
            ],
            "",
            "",
        ),
        (v.ResolveHashVar("var_1_2_3#1"), [], "var_1_2_3#1", "S"),
        (v.ResolveHashVar("var_1_2_3#5"), [], "var_1_2_3#5", "E"),
        (
            v.ResolveHashVar("var_99#5"),
            [
                "Variable name is not defined in a *create or *temp command."
                " Variable: var_99"
            ],
            "",
            "",
        ),
        (
            v.ResolveHashVar("var_3#2"),
            [
                "Value given with # is higher than the length of the variable value."
                " Variable: var_3#2"
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVar("var[var_1][var_2][var_3]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var_1[var_2[var_3]]]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var_1][var_2][var[var_3]]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var_1[var_6]][var_3][var_4]"),
            [],
            "var_1_2_3_4",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var[var_2]][var_3][var_4[var_5]]"),
            [],
            "var_2_3_4",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var_2][var[var_4]]"),
            [
                "Variable name is not defined in a *create or *temp command."
                " Variable: var_2_4"
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVar("var[var_1][var_2][var_33#2]"),
            [],
            "var_1_2_3",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var_1[var_6]][var_33#2][var_44#5]"),
            [],
            "var_1_2_3_4",
            "SUCCESS",
        ),
        (
            v.ResolveBracketVar("var[var#1[var_2]]"),
            [
                "Value following a # must be a number. Variable: var#1_2",
                "Variable name is not defined in a *create or *temp command."
                " Variable: var_",
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVar("var[var_1][var_2][var_33#20]"),
            [
                "Value given with # is higher than the length of the variable value."
                " Variable: var_33#20"
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVar("var[var_1[var_2[var_33#1]]]"),
            [
                "Variable name is not defined in a *create or *temp command. Variable:"
                " var_2_1"
            ],
            "",
            "",
        ),
        (
            v.ResolveBracketVar("var[var_1][var_2##1][var[var_3]]"),
            ["Variable name can not contain more than one #. Variable: var_2##1"],
            "",
            "",
        ),
    ],
)
def test_resolver_valid_struct(
    variable: resolver_type, exp_errors: list[str], exp_name: str, exp_value: Any
) -> None:
    errors, name, value = variable.resolve(game_variables)
    assert errors == exp_errors and name == exp_name and value == exp_value
