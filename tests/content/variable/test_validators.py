import pytest

from cstest.content.variable import validators as v
from cstest.content.variable.exceptions import NoVariableNameValue


@pytest.mark.parametrize(
    "name",
    [(""), (" ")],
)
def test_empty_variable_nname(name: str) -> None:
    with pytest.raises(NoVariableNameValue):
        v.empty_variable_name(name)


@pytest.mark.parametrize(
    "name, exp_outcome",
    [
        ("aaaa", True),
        ("a1111", True),
        ("11111", False),
        ("1aaaa", False),
        (12344, False),
        ("$asd", False),
    ],
)
def test_is_first_alpha(name: str, exp_outcome: bool) -> None:
    assert v.is_first_alpha(name) == exp_outcome


@pytest.mark.parametrize(
    "name, exp_outcome",
    [
        ("name", True),
        ("valid_symbol[name]", True),
        ("£", False),
        ("Wo=rd", False),
        ("bla nk", False),
        ("Bl@$h", False),
    ],
)
def test_inv_symbol(name: str, exp_outcome: bool) -> None:
    assert v.inv_symbol(name) == exp_outcome


@pytest.mark.parametrize(
    "name, exp_error",
    [
        ("name", []),
        ("valid_variable[name]", []),
        ("1name", ["Variable name must start with a letter. Variable: 1name"]),
        ("Wo=rd", ["Variable contains an invalid symbol. Variable: Wo=rd"]),
        (
            "1Wo=rd",
            [
                "Variable name must start with a letter. Variable: 1Wo=rd",
                "Variable contains an invalid symbol. Variable: 1Wo=rd",
            ],
        ),
    ],
)
def test_validate_variable_name(name: str, exp_error: str) -> None:
    assert v.validate_variable_name(name) == exp_error


@pytest.mark.parametrize("name, exp_outcome", [("name", False), ("[name", True)])
def test_first_char_sq_bracket(name: str, exp_outcome: bool) -> None:
    assert v.first_char_sq_bracket(name) == exp_outcome


@pytest.mark.parametrize(
    "variables, exp_outcome",
    [
        ("[name]", True),
        ("[name][", False),
        ("[]name][", True),
        ("[]]]", False),
        ("[name]name]", False),
        ("[[name]]", True),
    ],
)
def test_equal_sq_brackets(variables: str, exp_outcome: bool) -> None:
    assert v.equal_sq_brackets(variables) == exp_outcome