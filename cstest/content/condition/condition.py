# #   BRACKET VARIABLES
# #   # to denote number
# #   Invalid statements

# from __future__ import annotations

# import ast
# from dataclasses import dataclass
# from typing import Any, Optional, Tuple

# from cstest.constants import CONNECTORS, IF_COMMANDS, OPERATORS
# from cstest.content.condition.params import recode_params, validate_params

# # if var = 1
# # if var = "str"
# # if var = var
# # if var = var[var2]
# # if var = var[var2#1]
# # if var = var[var2]#1
# # if var = var[var2#1]#1


# @dataclass
# class Condition:
#     full_variable: str
#     operator: str
#     value: str

#     def __post_init__(self) -> None:
#         self.base_variable: str
#         self.base_hash: int
#         self.bracket_variable: str
#         self.bracket_hash: int

#     def resolve_variable(Self) -> None:
#         pass

#     def evaluate_condition(self) -> None:
#         """Return variable value == self.value"""
#         pass


# condition_dict = dict[int, Condition]
# condition_map_type = list[list[Condition]]


# def create_condition(params: list[str], length: int) -> Condition:
#     """Standardises parameters and uses them to create Condition object"""
#     return Condition(*recode_params(params, length))


# def identify_conditions(
#     list_string: list[str],
# ) -> Tuple[condition_dict, str]:
#     """Parse a list of strings that comprise a single *IF statement.
#     Identify each variable, operator and value that are in each condition.
#     Creates a dictionary of all the conditions within the statement."""
#     params: list[str] = []
#     string_conditions: condition_dict = {}
#     condition_num = 1
#     is_string = False
#     start_string = False
#     end_string = False
#     error = ""

#     for word in list_string:
#         if word in ["(", ")"]:  # Ignore brackets. AND and OR identify new conditions
#             continue

#         if word.startswith(("'", '"')):  # Manages multi-word string values
#             start_string = True
#             is_string = True
#         if word.endswith(("'", '"')):
#             end_string = True
#         word = word.replace("'", "").replace('"', "")

#         if word in CONNECTORS and not is_string:  # End of condition found
#             length, error = validate_params(params, len(params))
#             if error == "":
#                 string_conditions[condition_num] = create_condition(params, length)
#                 condition_num += 1
#                 params = []  # Reset for next condition
#             else:
#                 return {}, error
#         else:  # Mid-condition, keep appending the word as the next parameter
#             if is_string and not start_string:  # Word is mid multi word string
#                 params[len(params) - 1] = params[len(params) - 1] + " " + word
#                 if end_string:  # If is last word in string, then close the string
#                     is_string = False
#                     end_string = False
#                 continue
#             if end_string:  # Immediately close the string if only one word long
#                 is_string = False
#                 end_string = False

#    params.append(word)  # Append any other word, or starting word of the string
#             start_string = False  # Can always be safely turned off

#     # The last condition won't reach another AND or OR, so process it here
#     length, error = validate_params(params, len(params))
#     if error == "":
#         string_conditions[condition_num] = create_condition(params, length)
#     else:
#         return {}, error
#     return string_conditions, ""


# def is_sublist(lst: Any) -> bool:
#     """Identifies if an object is a list containing 3 elements.
#     This identifies a case where a list contains an unresolved Condition
#     pair, which needs resolving first"""
#     if isinstance(lst, list):
#         if len(lst) == 3:
#             if lst[1] in CONNECTORS:
#                 return True
#     return False


# def is_empty_list(lst: Any) -> bool:
#     """Identifies if an object is a lst containing nothing but
#     another list"""
#     if isinstance(lst, list):  # Is a list
#         if len(lst) == 1:  # Has one element - not a Condition pair or list of ints
#             if isinstance(lst[0], list):  # That element is a list
#                 if len(lst[0]) == 1:  # Contains single Condition
#                     return True
#                 elif lst[0][1] in CONNECTORS:  # Conrains a Condition pair
#                     return True
#                 else:  # Will then be a list of ints, i.e., processed Conditions
#                     return False
#             else:  # If not a list, must be a list wrapping a single Condition
#                 return True
#     return False


# def extend_list(base_list: list[list[int]], new_value: int) -> list[list[int]]:
#     for item in base_list:
#         item.extend([new_value])
#     return base_list


# def parse_condition_element(lst: list[Any]) -> list[list[int]]:
#     """Receives a list containing 3 elements: 2 conditions and a connector.
#     Neither condition has a sublist, but it could be a list of lists, containing
#     previously resolved Condition pairs from lower in the nested list stack.

#     Depending on which Conditions are lists and which are just integers (Conditions)
#     it creates a unified list[list[int]] from both conditions and returns that.

#     How the unified list is generated depends on whether the connector is AND or OR"""

#     # First Condition pair for entire statement will just be 2 ints - make a list
#     if not isinstance(lst[0], list) and not isinstance(lst[2], list):
#         return [[lst[0], lst[2]]] if lst[1] == "AND" else [[lst[0]], [lst[2]]]

#     # These two are the same, just the list is either on the left or right
#     # Takes the existing list[list[int]] and adds the integer from the other
#     # condition into it and returns it
#     elif isinstance(lst[0], list) and not isinstance(lst[2], list):
#         if lst[1] == "AND":
#             return extend_list(lst[0], lst[2])
#         if lst[1] == "OR":
#             lst[0].append([lst[2]])
#             return lst[0]

#     elif not isinstance(lst[0], list) and isinstance(lst[2], list):
#         if lst[1] == "AND":
#             return extend_list(lst[2], lst[0])
#         if lst[1] == "OR":
#             lst[2].append([lst[0]])
#             return lst[2]

#     # Two list[list[int]], picks one and iterates over it. Then unpicks each
#     # element of the other list[list[int]] and adds each constituent integer
#     # into the other list
#     elif isinstance(lst[0], list) and isinstance(lst[2], list):
#         if lst[1] == "AND":
#             new_list = []
#             for lst_1 in lst[0]:
#                 for lst_2 in lst[2]:
#                     new_list.append(lst_1 + lst_2)
#             return new_list

#         if lst[1] == "OR":
#             for lst_2 in lst[2]:
#                 lst[0].append(lst_2)
#             return lst[0]

#     return lst


# def iterate_list(lst: Any, indexer: list[int]) -> Tuple[list[Any], list[int]]:
#     """Hunts for the lowest unresolved Condition pair.
#     Check if the left hand condition has a sublist, if not checks the right
#     hand condition - once it reaches a Condition pair with no sublists, it
#     sends them to be resolved.

#     Each list that has a sublist is passed to this function again, in this way
#     it recursively iterates down the nested list stack"""
#     if is_empty_list(lst[0]):
#         indexer.append(0)
#         return lst[0][0], indexer
#     elif is_empty_list(lst[2]):
#         indexer.append(2)
#         return lst[2][0], indexer
#     elif is_sublist(lst[0]):
#         indexer.append(0)  # Record which index of the list was used
#         return iterate_list(lst[0], indexer)  # Now check that list
#     # Check right condition
#     elif is_sublist(lst[2]):
#         indexer.append(2)
#         return iterate_list(lst[2], indexer)
#     else:  # Found a Condition pair which just contains ints, no sublist
#         return parse_condition_element(lst), indexer


# def flatten_list(lst: list[Any]) -> list[list[int]]:
#     """Iterates over a list of nested lists, flattening out the nested
#     lists until it comprises of a list[list[int]]. This structure
#     represents all the possible Condition combinations."""

#     while is_empty_list(lst):
#         lst = lst[0]

#     # While either the left or right condition has a sublist
#     while is_sublist(lst[0]) or is_sublist(lst[2]):
#         # Recursively hunts for the lowest unresolved Condition pair
#         alteration, indexer = iterate_list(lst, [])

#         # Create a string containing python syntax to apply the alteration
#         # to the main list, so that it can be passed into the recursive function
#         # The indexer defines which element of the list needs to be changed
#         statement = "lst"
#         for x in indexer:
#             statement += f"[{x}]"
#         statement += f" = {alteration}"

#         exec(statement)

#     return parse_condition_element(lst)


# def create_condition_string(list_line: list[str]) -> str:
#     """Creates a string representation of a nested lists from the
#     IF command"""
#     cond_num = 1  # First Condition to be encountered is number 1
#     in_condition = False

#     # Recodes the command into a string representation of a python list
#     condition_string = "["
#     for word in list_line:
#         if word in IF_COMMANDS.keys():
#             # Recodes the structure to make it a list
#             condition_string += IF_COMMANDS[word]
#             in_condition = False
#         elif not in_condition:
#             # Every new condition is wholesale replaced by the next integer
#             condition_string += f"{str(cond_num)},"
#             in_condition = True
#             cond_num += 1
#     condition_string += "]"

#     return condition_string


# def map_conditions(
#     conditions: condition_dict, flattened_list: list[list[int]]
# ) -> condition_map_type:
#     """Looks up the corresponding Condition object using the integer
#     that was substituted for it and places it back"""
#     condition_map: condition_map_type = []
#     for int_list in flattened_list:
#         cond_list = [conditions[x] for x in int_list]
#         condition_map.append(cond_list)

#     return condition_map


# def process_conditions(
#     conditions: condition_dict, list_line: list[str]
# ) -> condition_map_type:
#     """Processes the structure of the IF statement. They are comprised of
#     Condition pairs (e.g., condition_1 AND condition_2 - where both conditions
#     must be true, or condition_1 OR condiion_2 - where either condition can be
#     true. This pair can be represented in a python object (list) thus:
#     [[condition_1, condition_2]] == AND
#     [[condition_1], [condition_2]] == OR

#     This function converts the IF statement string into nested lists of
#     Condition pairs. Each Condition pair comprises 3 elements (two Conditions
#     plus a connector (AND or OR).

#     That nested list can then be recursively iterated over to find the lowest
#     level Condition pair, which is reformatted to the above structure based on
#     its connector.

#     In this way, the list is progressively flattened from the lowest level up,
#     by iteratively taking the lowest level pair and collapsing it into a list
#     of lists. Ultimately the entire statement will be a single list containing
#     one or more nested lists.

#     Each Condition is treated as an integer for simplicity, with each subsequently
#     encountered Condition being given the next number off the stack. These are
#     then mapped to the dictionary of conditions previously identified - allowing
#     them to be inserted in place of the integers when the list is returned
#     """

#     # Create a string representation of the IF command and convert to a python list
#     lst = ast.literal_eval(create_condition_string(list_line))

#     # Puts a single Condition IF statement into a list
#     if is_sublist(lst):
#         flattened_list = flatten_list(lst)
#     else:
#         flattened_list = [[lst]]

#     return map_conditions(conditions, flattened_list)


# def pre_process_line(line: str) -> list[str]:
#     """Remove IF command, implant spaces around operators (so they can be
#     distinguished into individual words) and split all words into a list
#     of strings"""
#     line = line.replace("*if", "").lstrip().upper()

#     for symbol in OPERATORS:
#         line = line.replace(symbol, f" {symbol} ")

#     return line.split()


# def create_condition_map(line: str) -> Tuple[condition_map_type, str]:
#     """Processes an IF command line to create the full map of all possible
#     paths of conditions to be assessed. Returns a list of lists, each sub-list
#     contains a set of conditions, all of which must be true. Any of the sub-lists
#     can evaluate to true for the entire IF command to evaluate to true."""
#     list_line = pre_process_line(line)

#     conditions, error = identify_conditions(list_line)

#     condition_map = process_conditions(conditions, list_line)

#     return condition_map, error
