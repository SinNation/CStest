from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Tuple, Union

from cstest.constants import CONDITION_SYMBOLS

condition_type = dict[str, Any]


@dataclass
class Condition:
    variable: str
    operator: str
    value: Any


def recode_params(params: list[Any]) -> list[Any]:
    length = len(params)

    if length == 1:
        return [params[0], "boolean", "True"]
    if length == 2:
        return [params[1], "boolean", "False"]
    if length == 4:
        return [params[0], params[1] + params[2], params[3]]
    else:
        return params


def create_condition(params: list[Any]) -> Condition:
    params = recode_params(params)
    return Condition(*params)


def parse_conditions(list_string: list[Any]) -> dict[int, Condition]:
    params: list[Any] = []
    string_conditions = {}
    condition_num = 1
    is_string = False
    start_string = False
    end_string = False

    for word in list_string:
        word = str(word)
        if word.startswith("'") or word.startswith('"'):
            start_string = True
            is_string = True
        if word.endswith("'") or word.endswith('"'):
            end_string = True
        word = word.replace("'", "").replace('"', "")

        if word in ["(", ")"]:
            continue
        elif word in ["OR", "AND"] and not is_string:
            string_conditions[condition_num] = create_condition(params)
            condition_num += 1
            params = []
        else:
            if is_string and not start_string:
                params[len(params) - 1] = params[len(params) - 1] + " " + word
                if end_string:
                    is_string = False
                    end_string = False
                continue
            if end_string:
                is_string = False
                end_string = False

            params.append(word)
            start_string = False

    string_conditions[condition_num] = create_condition(params)

    return string_conditions


def single_var_handler(list_string: list[str]) -> list[Any]:
    params: list[Any] = [word for word in list_string if word not in ["(", ")"]]
    return params


commands = {
    "(": "[",
    ")": "],",
    "AND": "'AND',",
    "OR": "'OR',",
}


def has_sublist(lst: list) -> bool:
    return True if isinstance(lst, list) and len(lst) == 3 else False


def split_list(lst: list) -> Tuple[list[Any]]:
    return lst[0], lst[1], lst[2]  # type: ignore


def parse_condition_element(lst: list[Any]) -> list[list[int]]:
    if not isinstance(lst[0], list) and not isinstance(lst[2], list):
        return [[lst[0], lst[2]]] if lst[1] == "AND" else [[lst[0]], [lst[2]]]
    elif isinstance(lst[0], list) and not isinstance(lst[2], list):
        if lst[1] == "AND":
            for new_list in lst[0]:
                new_list.extend([lst[2]])

    elif isinstance(lst[0], list) and isinstance(lst[2], list):
        if lst[1] == "AND":
            for new_list in lst[0]:
                if len(lst[2]) == 1:
                    new_list.extend(lst[2])
                else:
                    for iter, list_2 in enumerate(lst[2]):
                        if iter == 1:
                            new_list.extend(lst[2][0])
                        else:
                            lst[0].extend(new_list.extend(lst[2][iter - 1]))
    elif not isinstance(lst[0], list) and isinstance(lst[2], list):
        if lst[1] == "AND":
            for new_list in lst[2]:
                new_list.extend([lst[0]])
        return [new_list]

    return lst


def iterate_list(lst: list[Any], indexer: list[int]) -> Tuple[list[Any], list[int]]:
    if has_sublist(lst[0]):
        indexer.append(0)
        return iterate_list(lst[0], indexer)
    elif has_sublist(lst[2]):
        indexer.append(2)
        return iterate_list(lst[2], indexer)
    else:
        return parse_condition_element(lst), indexer


def unpack_list(lst: list[Any]) -> list[list[int]]:
    for x in range(5):  # while has_sublist(lst[0]) or has_sublist(lst[2]):
        alteration, indexer = iterate_list(lst, [])

        statement = "lst"
        for x in indexer:
            statement += f"[{x}]"
        statement += f" = {alteration}"

        exec(statement)

    return parse_condition_element(lst)


def create_condition_map(
    string_conditions: dict[int, Condition], list_string: list[str]
) -> list[list[int]]:
    condition_string = "["
    cond_num = 1

    for word in list_string:
        if word in commands.keys():
            condition_string += commands[word]
        else:
            condition_string += f"{str(cond_num)},"
            cond_num += 1

    condition_string += "]"

    lst = ast.literal_eval(condition_string)

    if not has_sublist(lst):
        [lst] = lst

    return unpack_list(lst)


strings = [
    # "(bailey_available or tommy_available) or lopez_available",
    # "lopez_available or (bailey_available or tommy_available)",
    # "bailey_available",
    # "m_medicine >= 50",
    # "not(gilbert_painkillers)",
    # "(wil <60) and ((m_survival <50) and not(ptsd))",
    # "*if with_bailey and (bailey_faction >= 40)",
    # "*if (group_food < 300) and (group_food > 100)",
    # "*if (curr_weapon = 'compound bow') or (curr_weapon = 'recurve bow')",
    # "*if (bailey_available or tommy_available) or lopez_available or (cheese_avail or
    #  bread_avail)",
    # "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5))",
    # "(bailey_available or tommy_available)",
    # "*if ((((a and (b or c)) and ((d and e) or f)) or (g and h)) or i) and j"
    "*if ((((a and (b and c)) and ((d and e) and f)) and (g and h)) and i) and j"
    # "*if (a and (b and (c and d)))"
]


for string in strings:
    string = string.replace("*if", "").lstrip().upper()

    for symbol in CONDITION_SYMBOLS:
        string = string.replace(symbol, f" {symbol} ")

    list_string = string.split()

    string_conditions = {}

    if not any([x in list_string for x in ["AND", "OR"]]):
        string_conditions[1] = create_condition(single_var_handler(list_string))
        # condition_map = create_condition_map(string_conditions, list_string, True)
    else:
        string_conditions = parse_conditions(list_string)
        condition_map = create_condition_map(string_conditions, list_string)

    print(string_conditions)
    print(condition_map)
