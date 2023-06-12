import pytest

from cstest.content.variable import validators as v
from cstest.content.variable.exceptions import NoVariableNameValue


@pytest.mark.parametrize(
    "word, exp_outcome",
    [
        ("aaaa", True),
        ("a1111", True),
        ("11111", False),
        ("1aaaa", False),
        (12344, False),
        ("$asd", False),
    ],
)
def test_is_first_alpha(word: str, exp_outcome: bool) -> None:
    assert v.is_first_alpha(word) == exp_outcome


@pytest.mark.parametrize(
    "word",
    [(""), (" ")],
)
def test_is_first_alpha_exception(word: str) -> None:
    with pytest.raises(NoVariableNameValue):
        v.is_first_alpha(word)


@pytest.mark.parametrize(
    "word, exp_outcome",
    [
        ("word", True),
        ("valid_symbol[name]", True),
        ("£", False),
        ("Wo=rd", False),
        ("bla nk", False),
        ("Bl@$h", False),
    ],
)
def test_inv_symbol(word: str, exp_outcome: bool) -> None:
    assert v.inv_symbol(word) == exp_outcome


@pytest.mark.parametrize(
    "word, exp_outcome, exp_error",
    [
        ("word", True, []),
        ("valid_variable[name]", True, []),
        ("1name", False, ["Variable name must start with a letter. Variable: 1name"]),
        ("Wo=rd", False, ["Variable contains an invalid symbol. Variable: Wo=rd"]),
        (
            "1Wo=rd",
            False,
            [
                "Variable name must start with a letter. Variable: 1Wo=rd",
                "Variable contains an invalid symbol. Variable: 1Wo=rd",
            ],
        ),
    ],
)
def test_validate_variable_word(word: str, exp_outcome: bool, exp_error: str) -> None:
    act_outcome, act_error = v.validate_variable_word(word)
    assert act_outcome == exp_outcome and act_error == exp_error


@pytest.mark.parametrize(
    "variables, exp_outcome",
    [
        ("[word]", True),
        ("[word][", False),
        ("[]word][", True),
        ("[]]]", False),
        ("[word]word]", False),
        ("[[word]]", True),
    ],
)
def test_equal_sq_brackets(variables: str, exp_outcome: bool) -> None:
    assert v.equal_sq_brackets(variables) == exp_outcome
