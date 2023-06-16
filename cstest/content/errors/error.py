ERR = {
    # Variable struct errors
    "first_alpha": "Variable name must start with a letter",
    "inv_symbol": "Variable contains an invalid symbol",
    "mismatch_bracket": "Variable does not contain equal number of '[' and ']'",
    "multiple_hash": "Variable name can not contain more than one #",
    "hash_not_number": "Value following a # must be a number",
    "hash_place": "Use of # must always occur within a single set of []."
    " You can not slice a variable value that is being used to construct a full"
    " variable name",
    # Variable resolver errors
    "inv_var": "Variable name is not defined in a *create or *temp command",
    "inv_hash": "Value given with # is higher than the length of the variable value",
    # IF errors
    "if_param_count": "*IF statement is incorrectly formed, either containing"
    " more than 4, or 0, components for a single condition",
    "if_true": "*IF condition containing a single component must be a"
    " variable name and not a mathematical operation or number",
    "if_false": "*IF condition containing only 2 components can only"
    " take the form of *IF NOT [variable]",
    "if_operator": "*IF statement contains an invalid operator",
    "if_equality_variable": "*IF statement must contain a string variable name",
    "if_equality_value_str": "*IF statement value can not be a string if the"
    " operator is > or <",
    "if_equality_value_opr": "*IF statement value can not be an operator",
    "if_double_value": "*IF statement has two arguments passed for the value component",
}


def var_error_string(err_type: str, variable: str) -> str:
    return f"{ERR[err_type]}. Variable: {variable}"
