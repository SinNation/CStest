# def remove_common_non_variable_words(string: str) -> str:
#     for word in COMMON_NON_VARIABLE_WORDS:
#         string = re.sub(word, "", string)
#     return string


# def sq_bracket_handler(word: str) -> str:
#     bracketed_word = word.split("[")[1].replace("]", "")
#     return bracketed_word.split("#")[0] if "#" in bracketed_word else bracketed_word


# def remove_keywords(string: str, keyword_type: str) -> str:
#     keywords = KEYWORDS["common"] + KEYWORDS[keyword_type]
#     for keyword in keywords:
#         new_line = string.replace(keyword, " ")
#     return new_line


# def find_created_variables(self, string: str) -> None:
#         parts = string.split()
#         try:
#             name = parts[1]
#         except Exception:
#             self.errors["created_variable"] = "Create command has no variable name"
#             return
#         try:
#             value = parts[2]
#         except Exception:
#             self.errors[
#                 "created_variable"
#             ] = f"Created variable {name} has no initial value"
#             return

#         var_type = "str" if isinstance(value, str) else "number"
#         self.created_variable = DefinedVariable(name, var_type)

# def find_cmd_call_variables(self, string: str) -> None:
#     """Iterates over every word in the command. If it is a literal string
#     or a number, then it is rejected. Anything else should be a variable
#     of some kind"""

#     string = remove_keywords(string, "command")
#     string = remove_common_non_variable_words(string).split()  # type: ignore

#     multi_word_string = False

#     for word in string:
#         if multi_word_string:
#             if word.endswith(("'", '"')):
#                 multi_word_string = False
#                 continue
#             continue
#         if word.startswith(("'", '"')) and not word.endswith(("'", '"')):
#             multi_word_string = True
#             continue
#         if word.isnumeric():
#             continue
#         if word.startswith(("'", '"')) and word.endswith(("'", '"')):
#             continue
#         if "#" in word and "[" not in word:
#             self.called_variables.extend(word)
#             continue
#         if "[" in word:
#             self.called_bracket_variables.extend(word)
#             self.called_variables.extend(sq_bracket_handler(word))
#             continue
#         self.called_variables.extend(word)

#     def find_prose_call_variables(self, string: str) -> None:
#         """Iterates over every word in a prose string."""

#         string = remove_keywords(string, "prose").split()  # type: ignore
#         string = remove_common_non_variable_words(string)

#         if "{" in string:
#             for word in string:
#                 if "{" in word:
#                     word = word.split("}")[0].split("{")[1]
#                     if "[" in word:
#                         self.called_bracket_variables.extend(word)
#                         self.called_variables.extend(sq_bracket_handler(word))
#                     self.called_variables.extend(word)

#     def find_dual_call_variables(self, string: str) -> None:
#         cmd_string = string.split("#")[0]
#         prose_string = string.replace(cmd_string, "")
#         self.find_cmd_call_variables(cmd_string)
#         self.find_prose_call_variables(prose_string)

#     def evaluate_condition(self) -> None:
#         if self.command_type.value.conditional:
#             self.condition = create_condition(
#                 self.clean_line, self.command_type.value.name
#             )
