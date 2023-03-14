from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from cstest.constants import CONDITION_SYMBOLS

condition_type = dict[str, Any]


@dataclass
class Condition:
    variable: str
    operator: str
    value: Any


@dataclass
class ConditionGroup:
    conditions: list[Condition]
    comparator: str


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
    # "*if (bailey_available or tommy_available) or lopez_available or (cheese_avail
    # #or bread_avail)",
    "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5))",
    # "(bailey_available or tommy_available)",
]


def recode_params(params: list[str]) -> list[str]:
    length = len(params)

    if length == 1:
        return [params[0], "boolean", "True"]
    if length == 2:
        return [params[1], "boolean", "False"]
    if length == 4:
        return [params[0], params[1] + params[2], params[3]]
    else:
        return params


def create_condition(params: list[str]) -> Condition:
    params = recode_params(params)
    return Condition(*params)


def parse_conditions(list_string: list[str]) -> dict[int, Condition]:
    params: list[str] = []
    string_conditions = {}
    condition_num = 1

    for word in list_string:
        if word in ["(", ")"]:
            continue
        if word in ["OR", "AND"]:
            string_conditions[condition_num] = create_condition(params)
            condition_num += 1
            params = []
            continue
        params.append(word)
    string_conditions[condition_num] = create_condition(params)

    return string_conditions


def create_condition_map(
    string_conditions: dict[int, Condition], list_string: list[str], single_cond: bool
) -> dict[int, list[Condition]]:
    if single_cond:
        return {1: [string_conditions[1]]}

    condition_map: dict[int, list[Condition]] = {1: []}

    condition_number = 1
    map_number = 2

    bracket_count = 0
    condition_store: list[Condition] = []
    condition_found = False
    condition_type = ""
    # condition_group_type = ""

    for counter, word in enumerate(list_string):
        if word == "(":
            bracket_count += 1
        elif word == ")":
            if condition_type == "AND":
                for _, map in condition_map.items():
                    map.extend(condition_store)

            if condition_type == "OR":
                for key, map in condition_map.items():
                    temp_condition_map = {}
                    temp_condition_map[map_number] = deepcopy(map)
                    temp_condition_map[map_number].append(condition_store[1])
                    map_number += 1

                    condition_map[key].append(condition_store[0])

                for key, map in temp_condition_map.items():
                    condition_map[key] = map

            condition_store = []
            condition_found = False
            bracket_count -= 1

        elif word not in ("AND", "OR") and not condition_found:
            condition_store.append(string_conditions[condition_number])
            condition_number += 1
            condition_found = True
        elif word in ["AND", "OR"] and bracket_count != 0:
            condition_type = word
            condition_found = False
        elif word in ["AND", "OR"] and bracket_count == 0:
            # condition_group_type = word
            pass
        else:
            continue

    return condition_map


# "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5))"


def single_var_handler(list_string: list[str]) -> list[str]:
    return [word for word in list_string if word not in ["(", ")"]]


for string in strings:
    string = string.replace("*if", "").lstrip().upper()

    for symbol in CONDITION_SYMBOLS:
        string = string.replace(symbol, f" {symbol} ")

    list_string = string.split()

    string_conditions = {}

    if not any([x in list_string for x in ["AND", "OR"]]):
        string_conditions[1] = create_condition(single_var_handler(list_string))
        condition_map = create_condition_map(string_conditions, list_string, True)
    else:
        string_conditions = parse_conditions(list_string)
        condition_map = create_condition_map(string_conditions, list_string, False)

    print(condition_map)
