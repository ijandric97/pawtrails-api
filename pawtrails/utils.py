from typing import Any, get_args


def is_allowed_literal(var: Any, var_name: str, literals: object) -> None:
    """Check if the variable contains one of the defined type-hinted literal values.

    Args:
        var (Any): The variable to check
        var_name (str): The name of the variable; used for the Exception message
        literals (object): The list of allowed literal values

    Raises:
        ValueError: The variable does not contain any of the values defined in the list
        of literals
    """
    AllowedLiterals = list(get_args(literals))
    if var not in AllowedLiterals:
        raise ValueError(f"{var_name} {var} is not one of {AllowedLiterals}.")
