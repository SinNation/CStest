# from typing import Any

# import pytest

# from cstest.content.condition.params import is_num, recode_params, validate_params
# from cstest.content.errors.error import ERR


# @pytest.mark.parametrize(
#     "val, exp",
#     [
#         ("string", False),
#         ("20", True),
#         ("20.1", True),
#         (True, False),
#         (20, True),
#         (20.1, True),
#     ],
# )
# def test_is_num(val: Any, exp: bool) -> None:
#     assert is_num(val) == exp


# @pytest.mark.parametrize(
#     "params, length, error",
#     [
#         ([], 0, ERR["if_param_count"]),
#         ([1, 2, 3, 4, 5], 5, ERR["if_param_count"]),
#         ([1, 2, 3, 4, 5, 6, 7, 8], 8, ERR["if_param_count"]),
#         (["variable"], 1, ""),
#         (["20"], 1, ERR["if_true"]),
#         ([">"], 1, ERR["if_true"]),
#         (["NOT", "variable"], 2, ""),
#         (["NOT", "20"], 2, ERR["if_false"]),
#         (["NOT", "<"], 2, ERR["if_false"]),
#         (["variable", "variable"], 2, ERR["if_false"]),
#         (["20", "variable"], 2, ERR["if_false"]),
#         (["=", "variable"], 2, ERR["if_false"]),
#         (["variable", "=", "string"], 3, ""),
#         (["variable", "=", "long string"], 3, ""),
#         (["variable", "!=", "string"], 3, ""),
#         (["variable", ">=", "20"], 3, ""),
#         (["variable", "<=", "string"], 3, ""),
#         (["variable", ">", "long string"], 3, ERR["if_equality_value_str"]),
#         (["20", ">", "20"], 3, ERR["if_equality_variable"]),
#         (["<=", ">", "20"], 3, ERR["if_equality_variable"]),
#         (["variable", "string", "20"], 3, ERR["if_operator"]),
#         (["variable", "20", "20"], 3, ERR["if_operator"]),
#         (["variable", ">", "<"], 3, ERR["if_equality_value_opr"]),
#         (["variable", ">", "=", "string"], 4, ""),
#         (["variable", "<", "=", "20"], 4, ""),
#         (["variable", "<", "=", "long string"], 4, ERR["if_equality_value_str"]),
#         (["20", ">", "=", "20"], 4, ERR["if_equality_variable"]),
#         (["<=", ">", "=", "20"], 4, ERR["if_equality_variable"]),
#         (["variable", "string", "=", "20"], 4, ERR["if_operator"]),
#         (["variable", ">", "20", "20"], 4, ERR["if_double_value"]),
#         (["variable", ">", "20", "20"], 4, ERR["if_double_value"]),
#         (["variable", ">", "=", "<"], 4, ERR["if_equality_value_opr"]),
#     ],
# )
# def test_validate_params(params: list[str], length: int, error: str) -> None:
#     act_length, act_error = validate_params(params)
#     assert act_length == length and act_error == error


# @pytest.mark.parametrize(
#     "params, length, exp_params",
#     [
#         (["variable"], 1, ["variable", "boolean", "True"]),
#         (["NOT", "variable"], 2, ["variable", "boolean", "False"]),
#         (["variable", "=", "20"], 3, ["variable", "=", "20"]),
#         (["variable", ">", "=", "40"], 4, ["variable", ">=", "40"]),
#         (["variable", "=", "A long string"], 3, ["variable", "=", "A long string"]),
#     ],
# )
# def test_recode_params(
#     params: list[str],
#     length: int,
#     exp_params: list[str],
# ) -> None:
#     act_params = recode_params(params, length)
#     assert act_params == exp_params
