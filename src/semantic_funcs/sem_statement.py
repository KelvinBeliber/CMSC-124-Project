from syntax_funcs.operators import operator

def sem_func_call_arg(lexeme, line, function_table, symbol_table, semanticResult):
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']

    # Ensure the function exists
    func_name = lexeme[1][0]
    if func_name not in function_table:
        semanticResult += f"semantic error at line {line + 1}: Function '{func_name}' not declared.\n"
        return semanticResult

    # Retrieve expected argument types
    expected_args = function_table[func_name]

    # Validate the function arguments
    index = 3  # Start after "I HAS A YR" part
    actual_args = []
    while index < len(lexeme):
        if lexeme[index][1] in literals:  # Literal argument
            actual_args.append(lexeme[index][1].replace(" Literal", "").upper())
            index += 1
        elif lexeme[index][1] == 'Identifier':  # Identifier argument
            var_name = lexeme[index][0]
            if var_name not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' used in function call but not declared.\n"
                return semanticResult
            actual_args.append(symbol_table[var_name])  # Add the type from symbol_table
            index += 1
        elif lexeme[index][0] in operators:  # Operator argument (expression)
            semanticResult, result_type = operator(lexeme, line, semanticResult, symbol_table, index)
            if result_type is None:
                semanticResult += f"semantic error at line {line + 1}: Invalid expression in function arguments.\n"
                return semanticResult
            actual_args.append(result_type)  # Add the result type of the expression
            index += 1
        else:
            semanticResult += f"semantic error at line {line + 1}: Invalid function argument '{lexeme[index][0]}'.\n"
            return semanticResult

        # Skip 'AN' and 'YR' keywords for multi-argument functions
        if index < len(lexeme) and lexeme[index][0] == 'AN':
            index += 2  # Skip 'AN' and 'YR'

    # compare expected and actual arguments
    if len(expected_args) != len(actual_args):
        semanticResult += f"semantic error at line {line + 1}: Function '{func_name}' expects {len(expected_args)} arguments but got {len(actual_args)}.\n"
    else:
        for i, (expected, actual) in enumerate(zip(expected_args, actual_args)):
            if expected != actual:
                semanticResult += f"semantic error at line {line + 1}: Argument {i + 1} of function '{func_name}' expects '{expected}' but got '{actual}'.\n"

    return semanticResult

def sem_casting(lexeme, line, symbol_table, semanticResult):
    type = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    index = 0
    if lexeme[index][0] not in type:
        semanticResult += f"semantic error at line {line + 1}: Invalid type for casting \n"
    else:
        variable_name = lexeme[index][0]
        if variable_name not in symbol_table:
            semanticResult += f"semantic error at {line + 1}: Variable '{variable_name}' does not exist in symbol_table"
        else:
            current_type = symbol_table[variable_name]
            if current_type not in type:
                semanticResult += f"semantic error at {line + 1}: Casting is incompatible from type '{current_type}' to '{lexeme[index][0]}'!\n"

    return semanticResult

def sem_assignment(lexeme, symbol_table, line, semanticResult):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']

    # getting the left-hand side variable
    variable_name = lexeme[0][0]  # name of the left-hand side variable
    declared_type = symbol_table.get(variable_name)

    # If the variable is not declared, flag an error
    if declared_type is None:
        semanticResult += f"semantic error at line {line + 1}: Variable '{variable_name}' not declared.\n"
        return semanticResult

    # we check here if the right-hand side TYPE matches the left-hand side TYPE
    if lexeme[2][1] in literals:
        literal_type = lexeme[2][1].replace(" Literal", "").upper()
        if declared_type != literal_type:
            semanticResult += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but got '{literal_type}'.\n"
        elif lexeme[2][1] == 'Identifier':
            # right-hand side is another variable
            rhs_var = lexeme[2][0]  
            if rhs_var not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{rhs_var}' used on the right-hand side is not declared.\n"
            else:
                rhs_type = symbol_table[rhs_var]
                if declared_type != rhs_type:
                    semanticResult += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but got '{rhs_type}' from variable '{rhs_var}'.\n"
    else:
        # right-hand side is an operator expression
        # (Assume operator function validates its result type and returns it)
        semanticResult, result_type = operator(lexeme, line, semanticResult, symbol_table, 2)
        if declared_type != result_type:
            semanticResult += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but the expression evaluates to '{result_type}'.\n"

    return semanticResult

def sem_visible(lexeme, line, symbol_table, semanticResult):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]

    def evaluate_expression(lexeme, index, semanticResult):
        """Helper function to evaluate the type of an expression."""
        if lexeme[index][0] in operators:  # For nested expressions
            semanticResult, result_type = operator(lexeme, line, semanticResult, symbol_table, index)
            return result_type, semanticResult, index + 1  # Assume operator returns result type
        elif lexeme[index][1] in literals:  # For literals
            return lexeme[index][1].replace(" Literal", "").upper(), semanticResult, index + 1
        elif lexeme[index][1] == 'Identifier':  # For variables
            var_name = lexeme[index][0]
            if var_name not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not declared\n"
                return None, semanticResult, index + 1
            return symbol_table[var_name], semanticResult, index + 1
        else:
            semanticResult += f"semantic error at line {line + 1}: Invalid operand '{lexeme[index][0]}' in VISIBLE expression\n"
            return None, semanticResult, index + 1

    index = 0
    while index < len(lexeme):
        # evaluate operand
        result_type, semanticResult, next_index = evaluate_expression(lexeme, index, semanticResult)
        if result_type is None:
            semanticResult += f"semantic error at line {line + 1}: Invalid operand in VISIBLE expression\n"
            break
        index = next_index

        # check for 'AN' keyword between arguments
        if index < len(lexeme):
            if lexeme[index][0] != 'AN' and lexeme[index][0] != '+':
                semanticResult += f"semantic error at line {line + 1}: Missing or incorrect 'AN' keyword in VISIBLE arguments\n"
                break
            if index + 1 >= len(lexeme):
                semanticResult += f"semantic error at line {line + 1}: Insufficient VISIBLE arguments\n"
                break
            index += 1  # Move past 'AN'

    return semanticResult




