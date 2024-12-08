from semantic_funcs.operators import evaluate_operator
import lexical
import tkinter as tk
from tkinter import simpledialog

literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

def evaluate_function_call(lexeme, line, index, function_table, symbol_table, errors):
    temp = errors
    # Helper function to evaluate an operator
    def evaluate(function_table, function_name, errors):
        temp = errors
        visible_output=''
        symbol_table = function_table[function_name]['local_symbol_table']
        text = function_table[function_name]['function_code']
        for line in range(0, len(text.splitlines())):
            lexeme = lexical.lex(text.splitlines()[line].strip())
            if lexeme[0][0] == 'FOUND YR':
                if lexeme[1][1] == 'Identifier':  # Handle variables
                    var_name = lexeme[1][0]
                    return errors, symbol_table[var_name], visible_output
                if lexeme[1][1] in literals :  # Handle numeric literals
                    return None, (
                            int(lexeme[1][0]) if (lexeme[1][1] == 'NUMBR Literal') else 
                            float(lexeme[1][0]) if (lexeme[1][1] == 'NUMBAR Literal') else
                            lexeme[1][0]
                        ), visible_output
                if lexeme[1][0] in operators:  # Handle nested operators
                    errors,nested_result,_ = evaluate_operator(lexeme[1:], line, symbol_table, 0, errors)
                    if errors:
                        return errors, None, None
                    return errors, nested_result, visible_output
                raise ValueError(f"semantic error at {line+1}: Unknown syntax error")
            if lexeme[0][0] == 'GTFO':
                return errors, "NOOB", visible_output
            if lexeme[0][0] == 'GIMMEH':
                symbol_table[lexeme[1][0]] = evaluate_gimmeh()
                continue
            if lexeme[0][0] == 'VISIBLE':
                errors, result, _ = evaluate_visible(lexeme, line, symbol_table, 0, errors)
                if result:
                    visible_output+=result
                continue
    index+=1
    function_name = lexeme[index][0]
    index+=2
    result2=''
    for key in function_table[function_name]['local_symbol_table']:  # Two operands expected
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            function_table[function_name]['local_symbol_table'][key] = symbol_table[var_name]  # Fetch variable value
            index+=3
            continue
        if lexeme[index][1] in literals :  # Handle numeric literals
            function_table[function_name]['local_symbol_table'][key] = (
                int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                True if (lexeme[index][0] == 'WIN') else
                False if (lexeme[index][0] == 'FAIL') else
                None if (lexeme[index][0] == 'NOOB') else
                lexeme[index][0]
            )
            index+=3
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index, errors)
            index+2
            if errors:
                return errors, None, index
            function_table[function_name]['local_symbol_table'][key] = nested_result
            continue
        return errors+f"semantic error at {line+1}: invalid argument for function call", None, index
    # Perform the operation
    errors, result1, result2 = evaluate(function_table, function_name, errors)
    return errors, result1, result2

def evaluate_casting(line, errors, symbol_table, var_name, new_type):
    noob_cast = {
        'TROOF': 'FAIL',
        'NUMBR': int(0),
        'NUMBAR': float(0),
        'YARN': 'NOOB'
    }

    value = symbol_table[var_name]
    if value == 'NOOB':
        if new_type == 'NOOB':
            return errors+f"semantic error at {line+1}: redundant NOOB typecasting", symbol_table[var_name]
        if new_type not in noob_cast:
            raise ValueError(f"semantic error at {line+1}: Unknown value type")
        return errors, noob_cast[new_type]
    if value in ("WIN", "FAIL"):
        if new_type == 'NOOB':
            return errors+f"semantic error at {line+1}: cannot typecast TROOF to NOOB", symbol_table[var_name]
        if new_type == 'NUMBR':
            return errors, int(1) if value=='WIN' else int(0)
        if new_type == 'NUMBAR':
            return errors, float(1) if value=='WIN' else float(0)
        if new_type == 'YARN':
            return errors, "WIN" if value else "FAIL"
        if new_type == 'TROOF':
            return errors+f"semantic error at {line+1}: redundant TROOF typecasting", symbol_table[var_name]
        raise ValueError(f"semantic error at {line+1}: Unknown value type")
    if type(value) == int:
        if new_type == 'NUMBR':
            return errors+f"semantic error at {line+1}: redundant NUMBR typecasting", symbol_table[var_name]
        if new_type == 'NUMBAR':
            return errors, float(value)
        if new_type == 'YARN':
            return errors, str(value)
        if new_type == 'TROOF':
            return errors, "WIN" if value!=0 else "FAIL"
        if new_type == 'NOOB':
            return errors+f"semantic error at {line+1}: cannot typecast NUMBR to NOOB", symbol_table[var_name]
        raise ValueError(f"semantic error at {line+1}: Unknown value type")
    if type(value) == float:
        if new_type == 'NOOB':
            return errors+f"semantic error at {line+1}: cannot typecast NUMBR to NOOB", symbol_table[var_name]
        if new_type == 'NUMBR':
            return errors, int(value)
        if new_type == 'NUMBAR':
            return errors+f"semantic error at {line+1}: redundant NUMBAR typecasting", symbol_table[var_name]
        if new_type == 'YARN':
            return errors, f"{value:.2f}"
        if new_type == 'TROOF':
            return errors, "WIN" if value!=float(0) else "FAIL"
        raise ValueError(f"semantic error at {line+1}: Unknown value type")
    if type(value) == str:
        if new_type == 'NOOB':
            return errors+f"semantic error at {line+1}: cannot typecast NUMBR to NOOB", symbol_table[var_name]
        if new_type == 'NUMBR':
            try:
                return errors, int(value)
            except:
                return errors+f"semantic error at {line+1}: YARN, which contains non-numeric characters, cannot be typecasted to NUMBR", symbol_table[var_name]
        if new_type == 'NUMBAR':
            try:
                return errors, float(value)
            except:
                return errors+f"semantic error at {line+1}: YARN, which contains non-numeric characters, cannot be typecasted to NUMBAR", symbol_table[var_name]
        if new_type == 'YARN':
            return errors+f"semantic error at {line+1}: redundant NUMBAR typecasting", symbol_table[var_name]
        if new_type == 'TROOF':
            return errors, "WIN" if len(value)!=0 else "FAIL"
    return errors

def evaluate_gimmeh():
    # Create the Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Display the input dialog box
    user_input = simpledialog.askstring("GIMMEH", "Please enter a value:")
    
    # Close the Tkinter root window
    root.destroy()
    
    return user_input


def evaluate_visible(lexeme, line, symbol_table, index, errors):
    index+=1
    # Helper function to evaluate an operator
    def evaluate(operands):
        result = str(operands[0]).replace('"', '')
        for i in range(1,len(operands)):
            result = result + " " + str(operands[i]).replace('"', '')
        return result+"\n"

    operands = []
    while index!=len(lexeme):  # Two operands expected
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
        raise ValueError(f"semantic error at {line+1}: invalid operand type for VISIBLE operations")
    # Perform the operation
    result = evaluate(operands)
    return errors, result, index

# def evaluate_assign(lexeme, symbol_table, line, errors):
#     literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    
    
#     var_name = lexeme[0][0]  # Left-hand side variable name
    
#     # Handle type casting if the third token is 'MAEK' or 'IS NOW A'
#     if ['MAEK', 'Typecasting Operation'] == lexeme[2] or ['IS NOW A', 'Typecasting Operation'] == lexeme[1]:
#         temp = errors
#         errors, symbol_table[var_name] = evaluate_casting(line, errors, symbol_table, var_name, lexeme[2][0])
#         return errors

#     # Handle the right-hand side expression, it can be a literal, an identifier, or an operator expression
#     if lexeme[2][1] in literals:
#         symbol_table[var_name] = (
#                     int(lexeme[2][0]) if (lexeme[2][1] == 'NUMBR Literal') else 
#                     float(lexeme[2][0]) if (lexeme[2][1] == 'NUMBAR Literal') else
#                     lexeme[2][0] if (lexeme[2][1] == 'YARN Literal') else
#                     lexeme[2][0]
#                 )
#         return errors  # No further processing needed, literal assignment is valid
#     elif lexeme[2][1] == 'Identifier':
#         # If the right-hand side is a variable (check if it's declared)
#         rhs_var = lexeme[2][0]
#         if rhs_var not in symbol_table:
#             errors += f"syntax error at line {line + 1}: Variable '{rhs_var}' not declared on the right-hand side!\n"
#             return errors
#         return errors
#     else:
#         # If the right-hand side is an operator expression (e.g., SUM OF, DIFF OF)
#         # Use the operator function to process the expression
#         errors, _ = operator(lexeme, line, errors, symbol_table, 2)
#         temp = errors
#         errors, symbol_table[var_name],_ = evaluate_operator(lexeme[2:], line, symbol_table, 0, errors)
#         if len(temp)<len(errors):
#             return errors
#     return errors



