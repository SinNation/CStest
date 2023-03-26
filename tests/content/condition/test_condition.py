from typing import Union

import pytest

from cstest.constants import ERRORS
from cstest.content.condition import condition as c


@pytest.mark.parametrize(
    "params, result",
    [
        (["variable"], {1: c.Condition("variable", "boolean", "True")}),
        (["NOT", "variable"], {1: c.Condition("variable", "boolean", "False")}),
        (["variable", "=", "20"], {1: c.Condition("variable", "=", "20")}),
        (["variable", ">", "30"], {1: c.Condition("variable", ">", "30")}),
        (["variable", ">", "=", "40"], {1: c.Condition("variable", ">=", "40")}),
        (["variable", "<=", "50"], {1: c.Condition("variable", "<=", "50")}),
        (
            ["variable", "=", "A long string"],
            {1: c.Condition("variable", "=", "A long string")},
        ),
        ([], {}),
        (["1", "2", "3", "4", "5"], {}),
        ([">", ">", ">"], {}),
        (["variable", ">", "20", "24"], {}),
    ],
)
def test_create_condition(params: list[str], result: c.condition_dict) -> None:
    cond, _ = c.create_condition(params, 1, {})
    assert cond == result


@pytest.mark.parametrize(
    "list_line, exp_conditions, exp_error",
    [
        (["variable"], {1: c.Condition("variable", "boolean", "True")}, ""),
        (
            ["NOT", "(", "variable", ")"],
            {1: c.Condition("variable", "boolean", "False")},
            "",
        ),
        (["variable", "=", "20"], {1: c.Condition("variable", "=", "20")}, ""),
        (["variable", ">", "30"], {1: c.Condition("variable", ">", "30")}, ""),
        (["variable", ">", "=", "40"], {1: c.Condition("variable", ">=", "40")}, ""),
        (["variable", "<=", "50"], {1: c.Condition("variable", "<=", "50")}, ""),
        (
            ["variable", "=", "'A", "long", "string'"],
            {1: c.Condition("variable", "=", "A long string")},
            "",
        ),
        (["20"], {}, ERRORS["if_true"]),
        ([], {}, ERRORS["if_param_count"]),
        (["1", "2", "3", "4", "5"], {}, ERRORS["if_param_count"]),
        (["variable", "variable"], {}, ERRORS["if_false"]),
        (["variable", ">", "'long", "string'"], {}, ERRORS["if_equality_value_str"]),
        (["variable", ">", "string", "20"], {}, ERRORS["if_double_value"]),
        (["variable", ">", "=", "<"], {}, ERRORS["if_equality_value_opr"]),
        (["variable", "string", "=", "20"], {}, ERRORS["if_operator"]),
        (
            [
                "(",
                "(",
                "variable",
                "or",
                "variable2",
                ")",
                "or",
                "not",
                "variable3",
                ")",
            ],
            {
                1: c.Condition("variable", "boolean", "True"),
                2: c.Condition("variable2", "boolean", "True"),
                3: c.Condition("variable3", "boolean", "False"),
            },
            "",
        ),
        (
            [
                "(",
                "variable",
                "<60",
                ")",
                "and",
                "(",
                "(",
                "variable2",
                ")",
                "or",
                "not",
                "(",
                "variable3",
                ")",
                ")",
            ],
            {
                1: c.Condition("variable", "<", "60"),
                2: c.Condition("variable2", "boolean", "True"),
                3: c.Condition("variable3", "boolean", "False"),
            },
            "",
        ),
        (
            [
                "(",
                "variable",
                "=",
                "'two",
                "strings'",
                ")",
                "or",
                "(",
                "variable2",
                "=",
                "'two",
                "more",
                "strings'",
                ")",
            ],
            {
                1: c.Condition("variable", "=", "two strings"),
                2: c.Condition("variable2", "=", "two more strings"),
            },
            "",
        ),
        (
            [
                "(",
                "(",
                "(",
                "(",
                "variable",
                "and",
                "(",
                "variable2",
                "=",
                "20",
                "or",
                "not",
                "variable3",
                ")",
                ")",
                "and",
                "(",
                "(",
                "variable4",
                "and",
                "variable 5",
                "=",
                "a",
                "multi",
                "string",
                ")",
                "or",
                "variable6",
                ")",
                ")",
                "or",
                "(",
                "variable7",
                "and",
                "variable8",
                ")",
                ")",
                "or",
                "not",
                "variable9",
                ")",
                "and",
                "variable10",
            ],
            {
                1: c.Condition("variable", "boolean", "True"),
                2: c.Condition("variable2", "=", "20"),
                3: c.Condition("variable3", "boolean", "False"),
                4: c.Condition("variable4", "boolean", "True"),
                5: c.Condition("variable5", "=", "a multi string"),
                6: c.Condition("variable6", "boolean", "True"),
                7: c.Condition("variable7", "boolean", "True"),
                8: c.Condition("variable8", "boolean", "True"),
                9: c.Condition("variable9", "boolean", "False"),
                10: c.Condition("variable10", "boolean", "True"),
            },
            "",
        ),
    ],
)
def test_identify_conditions(
    list_line: list[str], exp_conditions: c.condition_dict, exp_error: str
) -> None:
    conditions, error = c.identify_conditions(list_line)

    assert conditions == exp_conditions and error == exp_error
