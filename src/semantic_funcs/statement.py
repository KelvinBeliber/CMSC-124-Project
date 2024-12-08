from semantic_funcs.operators import evaluate_operator

literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

# def sem_func_call_arg(lexeme, line, function_table, symbol_table, errors):
#     operators = [
#         'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
#         'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
#         'BOTH SAEM', 'DIFFRINT',
#         'SMOOSH'
#     ]
#     literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']

#     # # Ensure the function exists
#     func_name = lexeme[1][0]
#     # if func_name not in function_table:
#     #     errors += f"semantic error at line {line + 1}: Function '{func_name}' not declared.\n"
#     #     return errors

#     # Retrieve expected argument types
#     # expected_args = function_table[func_name]

#     # Validate the function arguments
#     index = 3  # Start after "I HAS A YR" part
#     actual_args = []
#     while index < len(lexeme):
#         if lexeme[index][1] in literals:  # Literal argument
#             actual_args.append(lexeme[index][1].replace(" Literal", "").upper())
#             index += 1
#         elif lexeme[index][1] == 'Identifier':  # Identifier argument
#             var_name = lexeme[index][0]
#             if var_name not in symbol_table:
#                 errors += f"semantic error at line {line + 1}: Variable '{var_name}' used in function call but not declared.\n"
#                 return errors
#             actual_args.append(symbol_table[var_name])  # Add the type from symbol_table
#             index += 1
#         elif lexeme[index][0] in operators:  # Operator argument (expression)
#             errors, result_type = operator(lexeme, line, errors, symbol_table, index)
#             if result_type is None:
#                 errors += f"semantic error at line {line + 1}: Invalid expression in function arguments.\n"
#                 return errors
#             actual_args.append(result_type)  # Add the result type of the expression
#             index += 1
#         else:
#             errors += f"semantic error at line {line + 1}: Invalid function argument '{lexeme[index][0]}'.\n"
#             return errors

#         # Skip 'AN' and 'YR' keywords for multi-argument functions
#         if index < len(lexeme) and lexeme[index][0] == 'AN':
#             index += 2  # Skip 'AN' and 'YR'

#     # compare expected and actual arguments
#     if len(expected_args) != len(actual_args):
#         errors += f"semantic error at line {line + 1}: Function '{func_name}' expects {len(expected_args)} arguments but got {len(actual_args)}.\n"
#     else:
#         for i, (expected, actual) in enumerate(zip(expected_args, actual_args)):
#             if expected != actual:
#                 errors += f"semantic error at line {line + 1}: Argument {i + 1} of function '{func_name}' expects '{expected}' but got '{actual}'.\n"

#     return errors

def evaluate_casting(line, errors, symbol_table, var_name, new_type):
    noob_cast = {
        'TROOF': 'FAIL',
        'NUMBR': int(0),
        'NUMBAR': float(0),
        'YARN': '',
        'NOOB': 'NOOB'
    }
    # numbr_cast = {
    #     'NUMBR': int(0),
    #     'NUMBAR': float(0),
    #     'YARN': '',
    #     'NOOB': 'NOOB'
    # }
    # yarn_cast = {
    #     'NUMBR': int(0),
    #     'NUMBAR': float(0),
    #     'YARN': '',
    #     'NOOB': 'NOOB'
    # }
    value = symbol_table[var_name]
    if value == 'NOOB':
        return errors, noob_cast[new_type]
    if value in ("WIN", "FAIL"):
        if new_type == 'NOOB':
            return errors, new_type
        if new_type == 'NUMBR':
            return errors, new_type
        if new_type == 'NUMBAR':
            return errors, new_type
        if new_type == 'YARN':
            return errors, new_type
        if new_type == 'TROOF':
            return errors, new_type
    if type(value) == int:
        if new_type == 'NOOB':
            return errors, new_type
        if new_type == 'NUMBR':
            return errors, new_type
        if new_type == 'NUMBAR':
            return errors, new_type
        if new_type == 'YARN':
            return errors, new_type
        if new_type == 'TROOF':
            return errors, new_type
    if type(value) == float:
        if new_type == 'NOOB':
            return errors, new_type
        if new_type == 'NUMBR':
            return errors, new_type
        if new_type == 'NUMBAR':
            return errors, new_type
        if new_type == 'YARN':
            return errors, new_type
        if new_type == 'TROOF':
            return errors, new_type
    if type(value) == str:
        if new_type == 'NOOB':
            return errors, new_type
        if new_type == 'NUMBR':
            return errors, new_type
        if new_type == 'NUMBAR':
            return errors, new_type
        if new_type == 'YARN':
            return errors, new_type
        if new_type == 'TROOF':
            return errors, new_type
    return errors

# def evaluate_assignment(lexeme, symbol_table, line, errors):
#     literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']

#     # getting the left-hand side variable
#     variable_name = lexeme[0][0]  # name of the left-hand side variable
#     declared_type = symbol_table.get(variable_name)

#     # we check here if the right-hand side TYPE matches the left-hand side TYPE
#     if lexeme[2][1] in literals:
#         literal_type = lexeme[2][1].replace(" Literal", "").upper()
#         if declared_type != literal_type:
#             errors += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but got '{literal_type}'.\n"
#         elif lexeme[2][1] == 'Identifier':
#             # right-hand side is another variable
#             rhs_var = lexeme[2][0]  
#             if rhs_var not in symbol_table:
#                 errors += f"semantic error at line {line + 1}: Variable '{rhs_var}' used on the right-hand side is not declared.\n"
#             else:
#                 rhs_type = symbol_table[rhs_var]
#                 if declared_type != rhs_type:
#                     errors += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but got '{rhs_type}' from variable '{rhs_var}'.\n"
#     else:
#         # right-hand side is an operator expression
#         # (Assume operator function validates its result type and returns it)
#         errors, result_type = operator(lexeme, line, errors, symbol_table, 2)
#         if declared_type != result_type:
#             errors += f"semantic error at line {line + 1}: Type mismatch. Variable '{variable_name}' expects '{declared_type}' but the expression evaluates to '{result_type}'.\n"

#     return errors

def evaluate_gimmeh():
    return input()

def evaluate_visible(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate(operands):
        result = str(operands[0]).replace('"', '')
        for i in range(1,len(operands)):
            result = result + " " + str(operands[i]).replace('"', '')
        return result+"\n"

    operands = []
    while index!=len(lexeme) and lexeme[index][0]!='MKAY':  # Two operands expected
        if lexeme[index][0] == 'AN' or lexeme[index][0] == '+':  # skip AN
            index+=1
            continue
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in literals :  # Handle numeric literals
            operands.append(
                    int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                    float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                    lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                    lexeme[index][0]
                )
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index, errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for SMOOSH operations", None, index
    # Perform the operation
    result = evaluate(operands)
    return errors, result, index

# def gimmeh(symbol_table, var_name):



