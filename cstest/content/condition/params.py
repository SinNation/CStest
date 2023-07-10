# from typing import Any, Tuple

# from cstest.constants import ERRORS, OPERATORS


# def is_num(param: Any) -> bool:
#     if param is True or param is False:
#         return False
#     try:
#         int(param)
#         return True
#     except Exception:
#         try:
#             float(param)
#             return True
#         except Exception:
#             return False


# def validate_params(params: list[str], length: int) -> Tuple[int, str]:
#     if length not in (1, 2, 3, 4):
#         error = ERRORS["if_param_count"]
#     elif length == 1:
# error = ERRORS["if_true"] if params[0] in OPERATORS or is_num(params[0]) else ""
#     elif length == 2:
#         error = (
#             ERRORS["if_false"]
#             if params[0] != "NOT" or params[1] in OPERATORS or is_num(params[1])
#             else ""
#         )
#     elif length == 3:
#         if params[0] in OPERATORS or is_num(params[0]):
#             error = ERRORS["if_equality_variable"]
#         elif params[1] not in OPERATORS:
#             error = ERRORS["if_operator"]
#         elif params[1] in (">", "<", ">=", "<=") and " " in params[2]:
#             error = ERRORS["if_equality_value_str"]
#         elif params[2] in OPERATORS:
#             error = ERRORS["if_equality_value_opr"]
#         else:
#             error = ""
#     else:
#         if params[0] in OPERATORS or is_num(params[0]):
#             error = ERRORS["if_equality_variable"]
#         elif params[1] not in OPERATORS:
#             error = ERRORS["if_operator"]
#         elif params[2] != "=":
#             error = ERRORS["if_double_value"]
#         elif params[1] in (">", "<") and " " in params[3]:
#             error = ERRORS["if_equality_value_str"]
#         elif params[3] in OPERATORS:
#             error = ERRORS["if_equality_value_opr"]
#         else:
#             error = ""

#     return length, error


# def recode_params(params: list[str], length: int) -> list[str]:
#     """Returns a list of strings as a standardised parameter set.
#     Length 1 input is a test of truthness (IF {variable})
#     Length 2 input is a test of falseness (IF NOT {variable})
#     Length 3 and 4 input is a test of equality:
#         (IF {variable} = {value}
#          IF {variable} >= {value}
#          IF {variable} > = {value})
#     """
#     if length == 1:
#         return [params[0], "boolean", "True"]
#     elif length == 2:
#         return [params[1], "boolean", "False"]
#     elif length == 4:
#         return [params[0], params[1] + params[2], params[3]]
#     else:
#         return params
