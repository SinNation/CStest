from typing import Any, Union

import pytest

from cstest.constants import ERRORS
from cstest.content.condition import condition as c


@pytest.mark.parametrize(
    "params, result",
    [
        (["VAR"], {1: c.Condition("VAR", "boolean", "True")}),
        (["NOT", "VAR"], {1: c.Condition("VAR", "boolean", "False")}),
        (["VAR", "=", "20"], {1: c.Condition("VAR", "=", "20")}),
        (["VAR", ">", "30"], {1: c.Condition("VAR", ">", "30")}),
        (["VAR", ">", "=", "40"], {1: c.Condition("VAR", ">=", "40")}),
        (["VAR", "<=", "50"], {1: c.Condition("VAR", "<=", "50")}),
        (["VAR", "=", "A B C"], {1: c.Condition("VAR", "=", "A B C")}),
        ([], {}),
        (["1", "2", "3", "4", "5"], {}),
        ([">", ">", ">"], {}),
        (["VAR", ">", "20", "24"], {}),
    ],
)
def test_create_condition(params: list[str], result: c.condition_dict) -> None:
    cond, _ = c.create_condition(params, 1, {})
    assert cond == result


@pytest.mark.parametrize(
    "list_line, exp_conditions, exp_error",
    [
        (["VAR"], {1: c.Condition("VAR", "boolean", "True")}, ""),
        (["(", "VAR", ")"], {1: c.Condition("VAR", "boolean", "True")}, ""),
        (["NOT", "(", "VAR", ")"], {1: c.Condition("VAR", "boolean", "False")}, ""),
        (["VAR", "=", "20"], {1: c.Condition("VAR", "=", "20")}, ""),
        (["VAR", ">", "30"], {1: c.Condition("VAR", ">", "30")}, ""),
        (["VAR", ">", "=", "40"], {1: c.Condition("VAR", ">=", "40")}, ""),
        (["VAR", "<=", "50"], {1: c.Condition("VAR", "<=", "50")}, ""),
        (["(", "VAR", "<=", "50", ")"], {1: c.Condition("VAR", "<=", "50")}, ""),
        (
            ["(", "(", "VAR", "<=", "50", ")", ")"],
            {1: c.Condition("VAR", "<=", "50")},
            "",
        ),
        (["VAR", "=", "'A", "B", "C'"], {1: c.Condition("VAR", "=", "A B C")}, ""),
        (["20"], {}, ERRORS["if_true"]),
        ([], {}, ERRORS["if_param_count"]),
        (["1", "2", "3", "4", "5"], {}, ERRORS["if_param_count"]),
        (["VAR", "VAR"], {}, ERRORS["if_false"]),
        (["VAR", ">", "'long", "STR'"], {}, ERRORS["if_equality_value_str"]),
        (["VAR", ">", "STR", "20"], {}, ERRORS["if_double_value"]),
        (["VAR", ">", "=", "<"], {}, ERRORS["if_equality_value_opr"]),
        (["VAR", "STR", "=", "20"], {}, ERRORS["if_operator"]),
        (
            ["(", "(", "VAR", "OR", "VAR2", ")", "OR", "NOT", "VAR3", ")"],
            {
                1: c.Condition("VAR", "boolean", "True"),
                2: c.Condition("VAR2", "boolean", "True"),
                3: c.Condition("VAR3", "boolean", "False"),
            },
            "",
        ),
        (
            [
                "(",
                "VAR",
                "<",
                "60",
                ")",
                "AND",
                "(",
                "(",
                "VAR2",
                ")",
                "OR",
                "NOT",
                "(",
                "VAR3",
                ")",
                ")",
            ],
            {
                1: c.Condition("VAR", "<", "60"),
                2: c.Condition("VAR2", "boolean", "True"),
                3: c.Condition("VAR3", "boolean", "False"),
            },
            "",
        ),
        (
            [
                "(",
                "VAR",
                "=",
                "'TWO",
                "STRs'",
                ")",
                "OR",
                "(",
                "VAR2",
                "=",
                "'TWO",
                "MORE",
                "STRs'",
                ")",
            ],
            {
                1: c.Condition("VAR", "=", "TWO STRs"),
                2: c.Condition("VAR2", "=", "TWO MORE STRs"),
            },
            "",
        ),
        (
            [
                "(",
                "(",
                "(",
                "(",
                "VAR",
                "AND",
                "(",
                "VAR2",
                "=",
                "20",
                "OR",
                "NOT",
                "VAR3",
                ")",
                ")",
                "AND",
                "(",
                "(",
                "VAR4",
                "AND",
                "VAR5",
                "=",
                "'A",
                "MULTI",
                "STR'",
                ")",
                "OR",
                "VAR6",
                ")",
                ")",
                "OR",
                "(",
                "VAR7",
                ">",
                "=",
                "100",
                "AND",
                "VAR8",
                ")",
                ")",
                "OR",
                "NOT",
                "VAR9",
                ")",
                "AND",
                "VAR10",
            ],
            {
                1: c.Condition("VAR", "boolean", "True"),
                2: c.Condition("VAR2", "=", "20"),
                3: c.Condition("VAR3", "boolean", "False"),
                4: c.Condition("VAR4", "boolean", "True"),
                5: c.Condition("VAR5", "=", "A MULTI STR"),
                6: c.Condition("VAR6", "boolean", "True"),
                7: c.Condition("VAR7", ">=", "100"),
                8: c.Condition("VAR8", "boolean", "True"),
                9: c.Condition("VAR9", "boolean", "False"),
                10: c.Condition("VAR10", "boolean", "True"),
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


@pytest.mark.parametrize(
    "lst, result",
    [
        ("0", False),
        ("string", False),
        (0, False),
        ([], False),
        ([1, 2], False),
        ([[1, "A"]], False),
        ([[1, 2, 3]], False),
        ([1, "OR", 3], True),
        ([[], "AND", []], True),
        ([1, "OR", [1, 2, 3]], True),
        ([[1, 2, 3], "AND", 3], True),
        ([[1, 2, 3], "OR", [1, 2, 3]], True),
        ([[1, 2, 3], [1, 2, 3], [1, 2, 3]], False),
        ([[1, 2, 3], "AND", [1, 2, 3]], True),
        ([[1, 2, 3], "OR", [1, 2, 3]], True),
        ([[], [1, 2, 3], []], False),
    ],
)
def test_is_sublist(lst: Any, result: bool) -> None:
    assert c.is_sublist(lst) is result


@pytest.mark.parametrize(
    "lst, value, exp_result",
    [
        ([[1, 2]], 3, [[1, 2, 3]]),
        ([[1, 2], [3, 4]], 5, [[1, 2, 5], [3, 4, 5]]),
    ],
)
def test_extend_list(
    lst: list[list[int]], value: int, exp_result: list[list[int]]
) -> None:
    assert c.extend_list(lst, value) == exp_result


@pytest.mark.parametrize(
    "in_list, out_list",
    [
        ([1, "AND", 2], [[1, 2]]),
        ([1, "OR", 2], [[1], [2]]),
        ([[[1, 2]], "AND", 3], [[1, 2, 3]]),
        ([[[1], [2]], "AND", 3], [[1, 3], [2, 3]]),
        ([[[1, 2, 3], [4, 5], [6]], "AND", 7], [[1, 2, 3, 7], [4, 5, 7], [6, 7]]),
        ([[[1, 2]], "OR", 3], [[1, 2], [3]]),
        ([[[1], [2]], "OR", 3], [[1], [2], [3]]),
        ([[[1, 2, 3], [4, 5], [6]], "OR", 7], [[1, 2, 3], [4, 5], [6], [7]]),
        ([3, "AND", [[1, 2]]], [[1, 2, 3]]),
        ([3, "AND", [[1], [2]]], [[1, 3], [2, 3]]),
        ([7, "AND", [[1, 2, 3], [4, 5], [6]]], [[1, 2, 3, 7], [4, 5, 7], [6, 7]]),
        ([3, "OR", [[1, 2]]], [[1, 2], [3]]),
        ([3, "OR", [[1], [2]]], [[1], [2], [3]]),
        ([7, "OR", [[1, 2, 3], [4, 5], [6]]], [[1, 2, 3], [4, 5], [6], [7]]),
        ([[[1, 2]], "AND", [[1, 2]]], [[1, 2, 1, 2]]),
        ([[[1], [2]], "AND", [[1], [2]]], [[1, 1], [1, 2], [2, 1], [2, 2]]),
        (
            [[[1, 2, 3], [4, 5], [6]], "AND", [[1, 2, 3], [4, 5], [6]]],
            [
                [1, 2, 3, 1, 2, 3],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 6],
                [4, 5, 1, 2, 3],
                [4, 5, 4, 5],
                [4, 5, 6],
                [6, 1, 2, 3],
                [6, 4, 5],
                [6, 6],
            ],
        ),
        ([[[1, 2]], "OR", [[1, 2]]], [[1, 2], [1, 2]]),
        ([[[1], [2]], "OR", [[1], [2]]], [[1], [2], [1], [2]]),
        (
            [[[1, 2, 3], [4, 5], [6]], "OR", [[1, 2, 3], [4, 5], [6]]],
            [[1, 2, 3], [4, 5], [6], [1, 2, 3], [4, 5], [6]],
        ),
    ],
)
def test_parse_condition_element(in_list: list[Any], out_list: list[Any]) -> None:
    assert c.parse_condition_element(in_list) == out_list


@pytest.mark.parametrize(
    "lst, exp_alteration, exp_indexer",
    [
        ([1, "AND", 2], [[1, 2]], []),
        ([[1, "OR", 2], "AND", 3], [[1], [2]], [0]),
        ([[[1, "AND", 4], "OR", 2], "AND", 3], [[1, 4]], [0, 0]),
        ([[[[1, "OR", 5], "AND", 4], "OR", 2], "AND", 3], [[1], [5]], [0, 0, 0]),
        ([[1, "OR", [2, "OR", 4]], "AND", 3], [[2], [4]], [0, 2]),
        ([[1, "OR", [[2, "AND", 5], "OR", 4]], "AND", 3], [[2, 5]], [0, 2, 0]),
        ([1, "AND", [2, "OR", 3]], [[2], [3]], [2]),
        ([1, "AND", [[2, "AND", 4], "OR", 3]], [[2, 4]], [2, 0]),
        ([1, "AND", [2, "AND", [[4, "AND", 5], "OR", 3]]], [[4, 5]], [2, 2, 0]),
        (
            [1, "AND", [2, "AND", [[[4, "OR", 6], "AND", 5], "OR", 3]]],
            [[4], [6]],
            [2, 2, 0, 0],
        ),
    ],
)
def test_iterate_list(
    lst: list[Any], exp_alteration: list[list[int]], exp_indexer: list[int]
) -> None:
    alteration, indexer = c.iterate_list(lst, [])
    assert alteration == exp_alteration and indexer == exp_indexer


@pytest.mark.parametrize(
    "lst, exp_output",
    [
        ([1], [[1]]),
        ([1, "AND", 2], [[1, 2]]),
        ([[1, "AND", 2]], [[1, 2]]),
        ([1, "OR", 2], [[1], [2]]),
        ([[1, "AND", 2], "AND", 3], [[1, 2, 3]]),
        ([[1, "AND", 2], "OR", 3], [[1, 2], [3]]),
        ([[1, "OR", 2], "AND", 3], [[1, 3], [2, 3]]),
        ([[1, "OR", 2], "OR", 3], [[1], [2], [3]]),
        ([[1, "OR", 2], "AND", [3, "AND", 4]], [[1, 3, 4], [2, 3, 4]]),
        ([[1, "AND", 2], "AND", [3, "OR", 4]], [[1, 2, 3], [1, 2, 4]]),
        ([[1, "OR", 2], "OR", [3, "OR", 4]], [[1], [2], [3], [4]]),
        (
            [[1, "OR", [2, "AND", 5]], "AND", [3, "AND", [4, "OR", 6]]],
            [[2, 5, 4, 3], [2, 5, 6, 3], [1, 4, 3], [1, 6, 3]],
        ),
        (
            [[[1, "AND", 5], "OR", 2], "AND", [[3, "OR", 6], "AND", 4]],
            [[1, 5, 3, 4], [1, 5, 6, 4], [2, 3, 4], [2, 6, 4]],
        ),
        (
            [[[1, "AND", 5], "OR", [2, "OR", 6]], "AND", [[3, "OR", 7], "AND", 4]],
            [[1, 5, 3, 4], [1, 5, 7, 4], [2, 3, 4], [2, 7, 4], [6, 3, 4], [6, 7, 4]],
        ),
        (
            [
                [[1, "AND", [[2, "OR", 3], "OR", 4]], "AND", [5, "AND", [6, "OR", 7]]],
                "OR",
                8,
            ],
            [
                [2, 1, 6, 5],
                [2, 1, 7, 5],
                [3, 1, 6, 5],
                [3, 1, 7, 5],
                [4, 1, 6, 5],
                [4, 1, 7, 5],
                [8],
            ],
        ),
    ],
)
def test_flatten_list(lst: list[Any], exp_output: list[Any]) -> None:
    assert c.flatten_list(lst) == exp_output


# @pytest.mark.parametrize(
#     "lst, exp_output",
#     [
#         (["(", "var_a", "and", "var_b", "=", "20", ")"], [1, "AND", 2]),
#         (["(", "not", "var_a", "OR", "var_2", ">=", "30", ")"],[1, "OR", 2]),
#         ([[1, "AND", 2], "AND", 3]),
#         ([[1, "AND", 2], "OR", 3]),
#         ([[1, "OR", 2], "AND", 3]),
#         ([[1, "OR", 2], "OR", 3]),
#         ([[1, "OR", 2], "AND", [3, "AND", 4]]),
#         ([[1, "AND", 2], "AND", [3, "OR", 4]]),
#         ([[1, "OR", 2], "OR", [3, "OR", 4]]),
#         (
#             [[1, "OR", [2, "AND", 5]], "AND", [3, "AND", [4, "OR", 6]]]),
#         (
#             [[[1, "AND", 5], "OR", 2], "AND", [[3, "OR", 6], "AND", 4]]),
#         (
#             [[[1, "AND", 5], "OR", [2, "OR", 6]], "AND", [[3, "OR", 7], "AND", 4]]),
#         (
#             [
#                 [[1, "AND", [[2, "OR", 3], "OR", 4]], "AND",
#                 [5, "AND", [6, "OR", 7]]],
#                 "OR",
#                 8,
#             ]),
#     ]
# def test_create_condition_string() -> None:
