def sem_vardec(lexeme, line, symbol_table, semanticResult):

    # Check for unused variables
    if lexeme[0][0] == "I HAS A":
        var_name = lexeme[1][0]

        # warn if a variable is declared but never used
        if var_name in symbol_table and symbol_table[var_name] is None:
            semanticResult += f"warning at line {line + 1}: Variable '{var_name}' declared but never initialized or used\n"

        # check for redeclaration of variables
        if var_name in symbol_table:
            semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' redeclared\n"
            return semanticResult

    # handle initialization and ensure type consistency
    if len(lexeme) >= 4 and lexeme[2][0] == "ITZ":
        var_name = lexeme[1][0]
        assigned_value = lexeme[3]

        # ensure variable exists in the symbol table
        if var_name not in symbol_table:
            semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not declared before use\n"
            return semanticResult

        # ensure type compatibility
        var_type = symbol_table[var_name]
        if var_type is not None and not is_type_compatible(var_type, assigned_value[1]):
            semanticResult += (
                f"semantic error at line {line + 1}: Type mismatch for variable '{var_name}'. "
                f"Expected '{var_type}', got '{assigned_value[1]}'\n"
            )
            return semanticResult

        # Update symbol table with assigned value
        symbol_table[var_name] = assigned_value

    # check for use of undeclared variables
    for token in lexeme:
        if token[1] == "Identifier" and token[0] not in symbol_table:
            semanticResult += f"semantic error at line {line + 1}: Variable '{token[0]}' used before declaration\n"
            return semanticResult

    return semanticResult


def is_type_compatible(var_type, assigned_type):
    """
    # Helper function to check if the assigned value type is compatible with the variable type.

    Args:
        var_type (str): Expected type of the variable.
        assigned_type (str): Type of the assigned value.

    Returns:
        bool: True if types are compatible, False otherwise.
    """
    type_compatibility = {
        "NUMBR": ["NUMBR Literal"],
        "NUMBAR": ["NUMBAR Literal"],
        "YARN": ["YARN Literal"],
        "TROOF": ["TROOF Literal"],
    }
    return assigned_type in type_compatibility.get(var_type, [])
