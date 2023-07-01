from typing import Any
from unittest.mock import patch

import pytest

from cstest.content.condition import condition as c
from cstest.project.constants import ERRORS


@pytest.mark.parametrize(
    "params, exp_cond, exp_error",
    [
        (["VAR"], {1: c.Condition("VAR", "boolean", "True")}, ""),
        (["NOT", "VAR"], {1: c.Condition("VAR", "boolean", "False")}, ""),
        (["VAR", "=", "20"], {1: c.Condition("VAR", "=", "20")}, ""),
        (["VAR", ">", "30"], {1: c.Condition("VAR", ">", "30")}, ""),
        (["VAR", ">", "=", "40"], {1: c.Condition("VAR", ">=", "40")}, ""),
        (["VAR", "!=", "30"], {1: c.Condition("VAR", "!=", "30")}, ""),
        (["VAR", "!", "=", "40"], {1: c.Condition("VAR", "!=", "40")}, ""),
        (["VAR", "<=", "50"], {1: c.Condition("VAR", "<=", "50")}, ""),
        (["VAR", "=", "A B C"], {1: c.Condition("VAR", "=", "A B C")}, ""),
        ([], {}),
        (["1", "2", "3", "4", "5"], {}),
        ([">", ">", ">"], {}),
        (["VAR", ">", "20", "24"], {}),
    ],
)
def test_create_condition(
    params: list[str], exp_cond: c.condition_dict, exp_error: str
) -> None:
    cond = c.create_condition(params, 1)
    assert cond == exp_cond


@pytest.mark.parametrize(
    "list_line, exp_conditions, exp_error",
    [
        (["VAR"], {1: c.Condition("VAR", "boolean", "True")}, ""),
        (["(", "VAR", ")"], {1: c.Condition("VAR", "boolean", "True")}, ""),
        (["NOT", "(", "VAR", ")"], {1: c.Condition("VAR", "boolean", "False")}, ""),
        (["VAR", "=", "20"], {1: c.Condition("VAR", "=", "20")}, ""),
        (["VAR", ">", "30"], {1: c.Condition("VAR", ">", "30")}, ""),
        (["VAR", ">", "=", "40"], {1: c.Condition("VAR", ">=", "40")}, ""),
        (["VAR", "!=", "30"], {1: c.Condition("VAR", "!=", "30")}, ""),
        (["VAR", "!", "=", "40"], {1: c.Condition("VAR", "!=", "40")}, ""),
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
    "lst, result",
    [
        ("", False),
        (2, False),
        (True, False),
        ([1, "AND", 2], False),
        ([2, "OR", [3, "AND", 4]], False),
        ([[1, 2]], False),
        ([[1], [2]], False),
        ([[1, 2, 3], [4, 5]], False),
        ([1], True),
        ([[1]], True),
        ([[3, "OR", 4]], True),
        ([[[[1]]]], True),
        ([[[[[3, "OR", 4]]]]], True),
    ],
)
def test_is_empty_list(lst: list[Any], result: bool) -> None:
    assert c.is_empty_list(lst) == result


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
        (
            [[1, "OR", [[[2, "AND", 5]], "OR", 4]], "AND", 3],
            [2, "AND", 5],
            [0, 2, 0],
        ),
        (
            [[[[[[1]], "OR", 5], "AND", 4], "OR", 2], "AND", [3, "OR", 4]],
            [1],
            [0, 0, 0, 0],
        ),
        (
            [
                [[[[[1, "AND", 10]], "OR", 5], "AND", 4], "OR", 2],
                "AND",
                [3, "OR", [[4, "OR", 10]]],
            ],
            [1, "AND", 10],
            [0, 0, 0, 0],
        ),
        (
            [[1, "OR", [[[2, "AND", [[5, "OR", 7]]]], "OR", 4]], "AND", 3],
            [2, "AND", [[5, "OR", 7]]],
            [0, 2, 0],
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
        ([1, "AND", 2], [[1, 2]]),
        ([[1, "AND", 2]], [[1, 2]]),  # Redundant bracket around top level
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
        (  # Two redundant brackets around single Condition
            [[1, "OR", [2, "AND", [[50]]]], "AND", [3, "AND", [4, "OR", 6]]],
            [[2, 50, 4, 3], [2, 50, 6, 3], [1, 4, 3], [1, 6, 3]],
        ),
        (  # Redundant brackets around two nested conditions
            [[1, "OR", [[2, "AND", 55]]], "AND", [3, "AND", [[4, "OR", 65]]]],
            [[2, 55, 4, 3], [2, 55, 65, 3], [1, 4, 3], [1, 65, 3]],
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
        (  # Redundant brackets around nested condition with nested condition
            [
                [
                    [1, "AND", [[[2, "OR", 3], "OR", 4]]],
                    "AND",
                    [5, "AND", [6, "OR", 7]],
                ],
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


@pytest.mark.parametrize(
    "lst, exp_output",
    [
        (["VAR_A"], "[1,]"),
        (["NOT", "VAR_A"], "[1,]"),
        (["VAR_A", "=", "20"], "[1,]"),
        (["VAR_A", ">", "=", "50"], "[1,]"),
        (["VAR_B", "=", "A LONG STRING"], "[1,]"),
        (["(", "VAR_A", "=", "20", ")"], "[[1,],]"),
        (["(", "(", "VAR_A", "=", "20", ")", ")"], "[[[1,],],]"),
        (["(", "VAR_A", "AND", "VAR_B", "=", "20", ")"], "[[1,'AND',2,],]"),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "20", ")", ")"],
            "[[[1,'AND',2,],],]",
        ),
        (
            ["(", "(", "(", "VAR_A", ")", ")", "AND", "VAR_B", "=", "20", ")"],
            "[[[[1,],],'AND',2,],]",
        ),
        (["(", "not", "VAR_A", "OR", "VAR_2", ">=", "30", ")"], "[[1,'OR',2,],]"),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "12", ")", "AND", "VAR_C", ")"],
            "[[[1,'AND',2,],'AND',3,],]",
        ),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "12", ")", "OR", "VAR_C", ")"],
            "[[[1,'AND',2,],'OR',3,],]",
        ),
        (
            ["(", "(", "VAR_A", "OR", "VAR_B", "=", "12", ")", "AND", "VAR_C", ")"],
            "[[[1,'OR',2,],'AND',3,],]",
        ),
        (
            [
                "(",
                "(",
                "VAR_A",
                "AND",
                "(",
                "(",
                "VAR_B",
                ">=",
                "45",
                "OR",
                "NOT",
                "VAR_C",
                ")",
                "OR",
                "VAR_D",
                "=",
                "A STRING",
                ")",
                ")",
                "AND",
                "(",
                "VAR_E",
                "AND",
                "(",
                "VAR_F",
                "OR",
                "VAR_G",
                "!",
                "=",
                "STRING",
                ")",
                ")",
                ")",
                "OR",
                "VAR_H",
                ")",
            ],
            "[[[1,'AND',[[2,'OR',3,],'OR',4,],],'AND',"
            "[5,'AND',[6,'OR',7,],],],'OR',8,],]",
        ),
    ],
)
def test_create_condition_string(lst: list[Any], exp_output: str) -> None:
    assert c.create_condition_string(lst) == exp_output


@pytest.mark.parametrize(
    "cond_dict, lst, output",
    [
        (
            {
                1: c.Condition("A", "=", "20"),
                2: c.Condition("A", "=", "30"),
                3: c.Condition("A", "=", "40"),
            },
            [[1, 2, 3]],
            [
                [
                    c.Condition("A", "=", "20"),
                    c.Condition("A", "=", "30"),
                    c.Condition("A", "=", "40"),
                ]
            ],
        ),
        (
            {
                1: c.Condition("A", "=", "20"),
                2: c.Condition("A", "=", "30"),
                3: c.Condition("A", "=", "40"),
            },
            [[1], [2, 3]],
            [
                [
                    c.Condition("A", "=", "20"),
                ],
                [
                    c.Condition("A", "=", "30"),
                    c.Condition("A", "=", "40"),
                ],
            ],
        ),
        (
            {
                1: c.Condition("A", "=", "20"),
                2: c.Condition("A", "=", "30"),
                3: c.Condition("A", "=", "40"),
            },
            [[1], [2], [3]],
            [
                [
                    c.Condition("A", "=", "20"),
                ],
                [
                    c.Condition("A", "=", "30"),
                ],
                [
                    c.Condition("A", "=", "40"),
                ],
            ],
        ),
    ],
)
def test_map_conditions(
    cond_dict: c.condition_dict, lst: list[list[int]], output: list[list[c.Condition]]
) -> None:
    assert c.map_conditions(cond_dict, lst) == output


@pytest.mark.parametrize(
    "list_line, exp_cond_map",
    [
        (["VAR_A"], [[c.Condition("VAR_A", "boolean", "True")]]),
        (["NOT", "VAR_A"], [[c.Condition("VAR_A", "boolean", "False")]]),
        (["VAR_A", "=", "20"], [[c.Condition("VAR_A", "=", "20")]]),
        (["VAR_A", ">", "=", "50"], [[c.Condition("VAR_A", ">=", "50")]]),
        (
            ["VAR_B", "=", "A LONG STRING"],
            [[c.Condition("VAR_B", "=", "A LONG STRING")]],
        ),
        (["(", "VAR_A", "=", "20", ")"], [[c.Condition("VAR_A", "=", "20")]]),
        (["(", "(", "VAR_A", "=", "20", ")", ")"], [[c.Condition("VAR_A", "=", "20")]]),
        (
            ["(", "VAR_A", "AND", "VAR_B", "=", "20", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", "=", "20"),
                ]
            ],
        ),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "20", ")", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", "=", "20"),
                ]
            ],
        ),
        (
            ["(", "(", "(", "VAR_A", ")", ")", "AND", "VAR_B", "=", "20", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", "=", "20"),
                ]
            ],
        ),
        (
            ["(", "not", "VAR_A", "OR", "VAR_2", ">=", "30", ")"],
            [
                [c.Condition("VAR_A", "boolean", "False")],
                [c.Condition("VAR_2", ">=", "30")],
            ],
        ),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "12", ")", "AND", "VAR_C", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", "=", "12"),
                    c.Condition("VAR_C", "boolean", "True"),
                ]
            ],
        ),
        (
            ["(", "(", "VAR_A", "AND", "VAR_B", "=", "12", ")", "OR", "VAR_C", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", "=", "12"),
                ],
                [c.Condition("VAR_C", "boolean", "True")],
            ],
        ),
        (
            ["(", "(", "VAR_A", "OR", "VAR_B", "=", "12", ")", "AND", "VAR_C", ")"],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_C", "boolean", "True"),
                ],
                [
                    c.Condition("VAR_B", "=", "12"),
                    c.Condition("VAR_C", "boolean", "True"),
                ],
            ],
        ),
        (
            [
                "(",
                "(",
                "VAR_A",
                "AND",
                "(",
                "(",
                "VAR_B",
                ">=",
                "45",
                "OR",
                "NOT",
                "VAR_C",
                ")",
                "OR",
                "VAR_D",
                "=",
                "A STRING",
                ")",
                ")",
                "AND",
                "(",
                "VAR_E",
                "AND",
                "(",
                "VAR_F",
                "OR",
                "VAR_G",
                "!",
                "=",
                "STRING",
                ")",
                ")",
                ")",
                "OR",
                "VAR_H",
                ")",
            ],
            [
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", ">=", "45"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_F", "boolean", "True"),
                ],
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_C", "boolean", "False"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_F", "boolean", "True"),
                ],
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_D", "=", "A STRING"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_F", "boolean", "True"),
                ],
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_B", ">=", "45"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_G", "!=", "STRING"),
                ],
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_C", "boolean", "False"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_G", "!=", "STRING"),
                ],
                [
                    c.Condition("VAR_A", "boolean", "True"),
                    c.Condition("VAR_D", "=", "A STRING"),
                    c.Condition("VAR_E", "boolean", "True"),
                    c.Condition("VAR_G", "!=", "STRING"),
                ],
                [c.Condition("VAR_H", "boolean", "True")],
            ],
        ),
    ],
)
def test_process_conditions(
    list_line: list[str], exp_cond_map: c.condition_map_type
) -> None:
    pass
    # assert c.process_conditions(list_line) == exp_cond_map


@pytest.mark.parametrize(
    "line, exp_output",
    [
        ("", []),
        ("word", ["WORD"]),
        ("WORD", ["WORD"]),
        ("*if", []),
        (" word ", ["WORD"]),
        ("  wo rd  ", ["WO", "RD"]),
        ("if word = 2", ["IF", "WORD", "=", "2"]),
        ("*if word>=2 and not word", ["WORD", ">", "=", "2", "AND", "NOT", "WORD"]),
        (
            "()><!not=>=<=!=",
            ["(", ")", ">", "<", "!", "NOT", "=", ">", "=", "<", "=", "!", "="],
        ),
        ("*if ((word =2))", ["(", "(", "WORD", "=", "2", ")", ")"]),
    ],
)
def test_pre_process_line(line: str, exp_output: list[str]) -> None:
    assert c.pre_process_line(line) == exp_output


def test_create_condition_map() -> None:
    string = """*if (( VAR_A AND ( ( VAR_B >= 45 OR NOT VAR_C ) OR VAR_D = A STRING ) )
      AND ( VAR_E AND ( VAR_F OR VAR_G!= STRING ) )) OR VAR_H )"""

    exp_map = [
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_B", ">=", "45"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_F", "boolean", "True"),
        ],
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_C", "boolean", "False"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_F", "boolean", "True"),
        ],
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_D", "=", "A STRING"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_F", "boolean", "True"),
        ],
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_B", ">=", "45"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_G", "!=", "STRING"),
        ],
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_C", "boolean", "False"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_G", "!=", "STRING"),
        ],
        [
            c.Condition("VAR_A", "boolean", "True"),
            c.Condition("VAR_D", "=", "A STRING"),
            c.Condition("VAR_E", "boolean", "True"),
            c.Condition("VAR_G", "!=", "STRING"),
        ],
        [c.Condition("VAR_H", "boolean", "True")],
    ]

    act_map, error = c.create_condition_map(string)

    assert act_map == exp_map and error == ""
