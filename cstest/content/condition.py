from dataclasses import dataclass
from typing import Any

# from cstest.constants import CONDITION_SYMBOLS

condition_type = dict[str, Any]


@dataclass
class Condition:
    variable: str
    operator: str
    value: Any


# @dataclass
# class ConditionGroup:
#     conditions: list[Condition]
#     comparator: str


# strings = [
#     # "(bailey_available or tommy_available) or lopez_available",
#     # "lopez_available or (bailey_available or tommy_available)",
#     "bailey_available",
#     "m_medicine >= 50",
#     "not(gilbert_painkillers)",
#     # "(wil <60) and ((m_survival <50) and not(ptsd))",
#     # "*if with_bailey and (bailey_faction >= 40)",
#     # "*if (group_food < 300) and (group_food > 100)",
#     # "*if (curr_weapon = 'compound bow') or (curr_weapon = 'recurve bow')",
#     # "*if (bailey_available or tommy_available) or lopez_available or (cheese_avail
# or bread_avail)",
#     # "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5)",
#     # "(bailey_available or tommy_available)",
# ]


# def recode_params(params: list[str]) -> list[str]:
#     length = len(params)
#     if length == 1:
#         return [params[0], "boolean", "True"]
#     elif length == 2:
#         return [params[1], "boolean", "False"]
#     elif length == 4:
#         return [params[0], params[1] + params[2], params[3]]
#     else:
#         return params


# def create_condition(params: list[str]) -> Condition:
#     params = recode_params(params)
#     return Condition(*params)


# def single_var_handler(list_str: list[str]) -> list[str]:
#     return [word for word in list_string if word not in ["(", ")"]]


# for string in strings:
#     string = string.replace("*if", "").lstrip().upper()

#     for symbol in CONDITION_SYMBOLS:
#         string = string.replace(symbol, f" {symbol} ")

#     list_string = string.split()

#     params: list[str] = []
#     string_conditions = {}
#     condition_num = 1

#     if not any([x in list_string for x in ["AND", "OR"]]):
#         string_conditions[1] = create_condition(single_var_handler(list_string))
#     else:
#         for word in list_string:
#             if word in ["(", ")"]:
#                 continue
#             if word in ["OR", "AND"]:
#                 string_conditions[condition_num] = create_condition(params)
#                 condition_num += 1
#                 params = []
#                 continue
#             params.append(word)
#         string_conditions[condition_num] = create_condition(params)

#     rel_depth = 0
#     rel_conditions = []
#     condition_num = 1

#     for word in list_string:
#         if word == "(":
#             rel_depth += 1

#         if word == ")":
#             pass

#         if word == "AND":
#             pass

#         if word == "OR":
#             pass

#         else:
#             rel_conditions.append(string_conditions[condition_num])

#     print(rel_conditions)

# #     [( ( cond_1 OR cond_2 ) AND cond_3 ) OR ( Cond_4 AND cond_5)]


# #     params: list[str] = []
# #     operator = ""
# #     rel_conditions: list[Condition] = []
# #     condition_depth = 1
# #     all_conditions: list[ConditionGroup] = []

# #     all_conditions.append(create_condition(params))

# #     print(all_conditions)

# #     for word in list_string:
# #         if word == "(":
# #             condition_depth += 1
# #             continue
# #         if word == ")":
# #             condition_depth -= 1
# #             rel_conditions.append(create_condition(params))
# #             all_conditions.append(ConditionGroup(rel_conditions, operator))
# #             params = []
# #             continue
# #         if word in ["OR", "AND"]:
# #             operator = word
# #             rel_conditions.append(create_condition(params))
# #             params = []
# #             continue
# #         params.append(word)

# #     print(all_conditions)


# # "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5)",


# # [
# #     [
# #         Condition("var_1", "boolean", True),
# #         Condition("var_2", "=", 20),
# #     ],
# #     [Condition("var_3", ">=", 12)],
# # ],
# # [[Condition("var_4", "=", "lala")], [Condition("var_5", "boolean", False)]]
