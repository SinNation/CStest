from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Tuple

from cstest.constants import CONNECTORS, ERRORS, IF_COMMANDS, OPERATORS


@dataclass
class Condition:
    """Definition of an IF condition."""

    variable: str
    operator: str
    value: Any


def create_condition(params: list[str], length: int) -> Condition:
    """Records parameters into standard form and converts them
    into a Condition object"""
    params = recode_params(params, length)
    return Condition(*params)


condition_dict = dict[int, Condition]
condition_map_type = list[list[Condition]]


def identify_single_condition(list_line: list[str]) -> Tuple[condition_dict, str]:
    params: list[str] = [word for word in list_line if word not in ["(", ")"]]
    length = len(params)
    # Too many, or 0, params identified
    if length not in (1, 2, 3, 4):
        return {}, ERRORS["invalid_if_params"]
    return {1: create_condition(params, length)}, ""


def recode_params(params: list[str], length: int) -> list[str]:
    """Returns a list of strings as a standardised parameter set.
    Length 1 input is a test of truthness (IF {variable})
    Length 2 input is a test of falseness (IF NOT {variable})
    Length 3 and 4 input is a test of equality:
        (IF {variable} = {value}
         IF {variable} >= {value}
         IF {vatiable} > = {value})
    """
    if length == 1:
        return [params[0], "boolean", "True"]
    elif length == 2:
        return [params[1], "boolean", "False"]
    elif length == 4:
        return [params[0], params[1] + params[2], params[3]]
    else:
        return params


def identify_multiple_conditions(
    list_string: list[str],
) -> Tuple[condition_dict, str]:
    """Parse a list of strings that comprise a single *IF statement.
    Identify each variable, operator and value that are in each condition.
    Creates a dictionary of all the conditions within the statement."""
    params: list[str] = []
    string_conditions = {}
    condition_num = 1
    is_string = False
    start_string = False
    end_string = False

    for word in list_string:
        # No need to parse brackets. AND and OR identify each new condition
        if word in ["(", ")"]:
            continue

        # Conditions can contain a full string to compare the value against.
        if word.startswith(("'", '"')):
            start_string = True
            is_string = True
        if word.endswith(("'", '"')):
            end_string = True

        word = word.replace("'", "").replace('"', "")

        # End of a condition, so process it
        if word in CONNECTORS and not is_string:
            length = len(params)
            # Too many, or 0, params identified
            if length not in (1, 2, 3, 4):
                return {}, ERRORS["invalid_if_params"]
            else:
                string_conditions[condition_num] = create_condition(params, length)
                condition_num += 1
                params = []  # Reset for next condition
        # Mid-condition, keep appending the word as the next parameter
        else:
            # Word is mid-string, append to last param value to compile full string
            if is_string and not start_string:
                params[len(params) - 1] = params[len(params) - 1] + " " + word
                # If is last word in string, then close the string
                if end_string:
                    is_string = False
                    end_string = False
                continue
            # Immediately close the string if it is only one word long
            if end_string:
                is_string = False
                end_string = False

            # Append any other word, or is the starting word of the string
            params.append(word)
            start_string = False  # Can always be safely turned off

    # The last condition won't reach another AND or OR, so process it here
    length = len(params)
    # Too many, or 0, params identified
    if length not in (1, 2, 3, 4):
        return {}, ERRORS["invalid_if_params"]
    string_conditions[condition_num] = create_condition(params, length)

    return string_conditions, ""


def has_sublist(lst: list) -> bool:
    return True if isinstance(lst, list) and len(lst) == 3 else False


def extend_list(base_list: list[list[int]], new_value: int) -> list[list[int]]:
    for item in base_list:
        item.extend([new_value])
    return base_list


def parse_condition_element(lst: list[Any]) -> list[list[int]]:
    print(lst)
    if not isinstance(lst[0], list) and not isinstance(lst[2], list):
        return [[lst[0], lst[2]]] if lst[1] == "AND" else [[lst[0]], [lst[2]]]

    elif isinstance(lst[0], list) and not isinstance(lst[2], list):
        if lst[1] == "AND":
            return extend_list(lst[0], lst[2])

    elif isinstance(lst[0], list) and isinstance(lst[2], list):
        if lst[1] == "AND":
            for new_list in lst[0]:
                for lst_2 in lst[2]:
                    new_list.extend(lst_2)
        return lst[0]

    elif not isinstance(lst[0], list) and isinstance(lst[2], list):
        if lst[1] == "AND":
            return extend_list(lst[2], lst[0])

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
    while has_sublist(lst[0]) or has_sublist(lst[2]):
        alteration, indexer = iterate_list(lst, [])

        statement = "lst"
        for x in indexer:
            statement += f"[{x}]"
        statement += f" = {alteration}"

        exec(statement)

        print(f"{alteration = }")
        print(f"new list: {lst}")

    return parse_condition_element(lst)


def process_conditions(
    conditions: condition_dict, list_string: list[str]
) -> condition_map_type:
    """Processes the structure of the IF statement. They are comprised of
    Condition pairs (e.g., condition_1 AND condition_2 - where both conditions
    must be true, or condition_1 OR condiion_2 - where either condition can be
    true. This pair can be represented in a python object (list) thus:
    [[condition_1, condition_2]] == AND
    [[condition_1], [condition_2]] == OR

    This function converts the IF statement string into nested lists of
    Condition pairs. Each Condition pair comprises 3 elements (two Conditions
    plus a connector (AND or OR).

    That nested list can then be recursively iterated over to find the lowest
    level Condition pair, which is reformatted to the above structure based on
    its connector.

    In this way, the list is progressively flattened from the lowest level up,
    by iteratively taking the lowest level pair and collapsing it into a list
    of lists. Ultimately the entire statement will be a single list containing
    one or more nested lists.

    Each Condition is treated as an integer for simplicity, with each subsequently
    encountered Condition being given the next number off the stack. These are
    then mapped to the dictionary of conditions previously identified - allowing
    them to be inserted in place of the integers when the list is returned
    """

    cond_num = 1  # First Condition to be encountered is number 1
    in_condition = False

    # Recodes the command into a string representation of a python list
    condition_string = "["
    for word in list_string:
        if word in IF_COMMANDS.keys():
            # Recodes the structure to make it a list
            condition_string += IF_COMMANDS[word]
            in_condition = False
        elif not in_condition:
            # Every new condition is wholesale replaced by the next integer
            condition_string += f"{str(cond_num)},"
            in_condition = True
            cond_num += 1
    condition_string += "]"

    # Converts the generated string into a python list
    lst = ast.literal_eval(condition_string)

    if not has_sublist(lst):
        [lst] = lst

    print(f"Initial list: {lst}")

    # return unpack_list(lst)
    return []


def pre_process_line(line: str) -> list[str]:
    """Remove IF command, implant spaces around operators (so they can be
    distinguished into individual words) and split all words into a list
    of strings"""
    line = line.replace("*if", "").lstrip().upper()

    for symbol in OPERATORS:
        line = line.replace(symbol, f" {symbol} ")

    return line.split()


def create_condition_map(line: str) -> Tuple[condition_map_type, str]:
    """Processes an IF command line to create the full map of all possible
    paths of conditions to be assessed. Returns a list of lists, each sub-list
    contains a set of conditions, all of which must be true. Any of the sub-lists
    can evaluate to true for the entire IF command to evaluate to true."""
    list_line = pre_process_line(line)

    # If not AND or OR are present, there is only a single condition in the command
    if not any([x in list_line for x in ["AND", "OR"]]):
        conditions, error = identify_single_condition(list_line)
    else:
        conditions, error = identify_multiple_conditions(list_line)

    condition_map = process_conditions(conditions, list_line)

    print(condition_map)
    return condition_map, error


strings = [
    # "(bailey_available or tommy_available) or lopez_available",
    # "lopez_available or (bailey_available or tommy_available)",
    # "bailey_available",
    # "m_medicine >= 50",
    # "not(gilbert_painkillers)",
    # "(wil <60) and ((m_survival <50) and not(ptsd))",
    # "*if with_bailey and (bailey_faction >= 40)",
    # "*if (group_food < 300) and (group_food > 100)",
    "*if (curr_weapon = 'compound bow') or (curr_weapon = 'recurve bow')",
    # "*if (bailey_available or tommy_available) or lopez_available or (cheese_avail or
    #  bread_avail)",
    # "*if ((var_1 or var_2 = 20) and var_3 >= 12) or (var_4 = 'lala' and not(var_5))",
    # "(bailey_available or tommy_available)",
    # "*if ((((a and (b or c)) and ((d and e) or f)) or (g and h)) or i) and j"
    # "*if ((((a and (b and c)) and ((d and e) and f)) and (g and h)) and i) and j"
    # "*if (a and (b and (c and d)))"
]

for s in strings:
    create_condition_map(s)
