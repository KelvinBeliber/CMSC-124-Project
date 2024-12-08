from syntax_funcs.operators import operator
from semantic_funcs.operators import evaluate_operator
from semantic_funcs.statement import evaluate_visible
from semantic_funcs.statement import evaluate_gimmeh
from semantic_funcs.statement import evaluate_casting

def func_call_arg(lexeme, line, function_table, symbol_table, errors):
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]
    literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    def is_valid_expression(lexeme, index, errors):
        """Helper function to validate an arithmetic or logical expression."""
        if lexeme[index][0] in operators:  # Check for nested expressions
            errors, end_index = operator(lexeme, line, errors, symbol_table, index)
            if not end_index:
                return errors, None
            return errors, end_index
        elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
            var_name = lexeme[index][0]
            if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                errors += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                return errors, None
            return errors, index + 1  # Move to next index
        else:
            return errors, None

    index = 1
    if lexeme[index][0] not in function_table:
        return f"syntax error at line {line + 1}: the function called does not exist\n"
    if lexeme[index+1][0] != 'YR':
        return f"syntax error at line {line + 1}: Incorrect function call syntax\n"
    index+=2
    while index < len(lexeme):
        # Validate operand
        errors, next_index = is_valid_expression(lexeme, index, errors)
        if not next_index:
            errors += f"syntax error at line {line + 1}: Invalid argument in function declaration\n"
            break
        index = next_index

        # Check if there's an 'AN' keyword after each operand except the last
        if index < len(lexeme):
            if index+1>=len(lexeme):
                errors += f"syntax error at line {line + 1}: Expected 'YR' after 'AN' in function declaration\n"
                break
            if lexeme[index][0] != 'AN' or lexeme[index+1][0] != 'YR':
                errors += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in function arguments\n"
                break
            if index+2>=len(lexeme):
                errors += f"syntax error at line {line + 1}: Insufficient function arguments\n"
                break
            index += 2  # Move past 'AN'

    return errors

def casting(lexeme, line, symbol_table, errors):
    type = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    index = 0
    if lexeme[index][0] == 'MAEK':
        index+=1
        if lexeme[index] == ['A','Typecasting Operation']:
            index+=1
        if lexeme[index][1] != 'Identifier':
            errors += f"syntax error at line {line + 1}: No variable to typecast!\n"
        if lexeme[index][0] not in symbol_table:
            errors += f"syntax error at line {line + 1}: Variable was not declared!\n"
        var_name = lexeme[index][0]
        index+=1
        if lexeme[index][0] not in type:
            errors += f"syntax error at line {line + 1}: Invalid type for casting\n"
        # errors, symbol_table[var_name] = evaluate_casting(line, errors, symbol_table, var_name, lexeme[index][0]) evaluate_casting not yet finished
    elif lexeme[index][1] == 'Identifier' and lexeme[index+1][0] == 'IS NOW A':
        if lexeme[index][0] not in symbol_table:
            errors += f"syntax error at line {line + 1}: Variable was not declared!\n"
        var_name = lexeme[index][0]
        if lexeme[2][0] not in type:
            errors += f"syntax error at line {line + 1}: Invalid type for casting\n"
        # errors, symbol_table[var_name] = evaluate_casting(line, errors, symbol_table, var_name, lexeme[2][0]) evaluate_casting not yet finished
    return errors

def assignment(lexeme, symbol_table, line, errors):
    literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    
    # Check if the left-hand side is a valid identifier (variable)
    if lexeme[0][1] != 'Identifier':
        errors += f"syntax error at line {line + 1}: Invalid variable '{lexeme[0][0]}'!\n"
        return errors
    
    var_name = lexeme[0][0]  # Left-hand side variable name
    
    # Ensure that the variable is already declared in symbol_table
    if var_name not in symbol_table:
        errors += f"syntax error at line {line + 1}: Variable '{var_name}' not declared!\n"
        return errors
    
    # Check for the 'R' keyword, ensuring it's in the correct position
    if lexeme[1][0] != 'R':
        errors += f"syntax error at line {line + 1}: Invalid declaration, missing 'R'!\n"
        return errors
    
    # Handle type casting if the third token is 'MAEK' or 'IS NOW A'
    if ['MAEK', 'Typecasting Operation'] == lexeme[2] or ['IS NOW A', 'Typecasting Operation'] == lexeme[1]:
        errors = casting(lexeme[2:], line, symbol_table, errors)
        return errors

    # Handle the right-hand side expression, it can be a literal, an identifier, or an operator expression
    if lexeme[2][1] in literals:
        symbol_table[var_name] = (
                    int(lexeme[2][0]) if (lexeme[2][1] == 'NUMBR Literal') else 
                    float(lexeme[2][0]) if (lexeme[2][1] == 'NUMBAR Literal') else
                    lexeme[2][0] if (lexeme[2][1] == 'YARN Literal') else
                    lexeme[2][0]
                )
        return errors  # No further processing needed, literal assignment is valid
    elif lexeme[2][1] == 'Identifier':
        # If the right-hand side is a variable (check if it's declared)
        rhs_var = lexeme[2][0]
        if rhs_var not in symbol_table:
            errors += f"syntax error at line {line + 1}: Variable '{rhs_var}' not declared on the right-hand side!\n"
            return errors
        return errors
    else:
        # If the right-hand side is an operator expression (e.g., SUM OF, DIFF OF)
        # Use the operator function to process the expression
        errors, _ = operator(lexeme, line, errors, symbol_table, 2)
        temp = errors
        errors, symbol_table[var_name],_ = evaluate_operator(lexeme[2:], line, symbol_table, 0, errors)
        if len(temp)<len(errors):
            return errors
    return errors
    
def expression(lexeme, line, errors, symbol_table): # <operator> | <literal>
    literals = ['Void Literal', 'NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal']
    #check if the first element is a valid literal
    if lexeme[0][1] in literals:
        return errors, None
    else:
        return operator(lexeme, line, errors, symbol_table, 0)

def visible(lexeme, line, errors, symbol_table):
    temp = errors
    literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]

    def is_valid_expression(lexeme, index, errors):
        """Helper function to validate an arithmetic or logical expression."""
        if lexeme[index][0] in operators:  # Check for nested expressions
            errors, end_index = operator(lexeme, line, errors, symbol_table, index)
            return True, errors, end_index
        elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
            var_name = lexeme[index][0]
            if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                errors += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                return False, errors, index
            return True, errors, index + 1  # Move to next index
        else:
            return False, errors, index

    index = 0
    while index < len(lexeme):
        # Validate operand
        is_valid, errors, next_index = is_valid_expression(lexeme, index, errors)
        if not is_valid:
            errors += f"syntax error at line {line + 1}: Invalid operand in VISIBLE expression\n"
            break
        index = next_index

        # Check if there's an 'AN' keyword after each operand except the last
        if index < len(lexeme):
            if lexeme[index][0] != 'AN' and lexeme[index][0] != '+':
                errors += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in VISIBLE arguments\n"
                break
            if index+1>=len(lexeme):
                errors += f"syntax error at line {line + 1}: Insufficient VISIBLE arguments\n"
                break
            index += 1  # Move past 'AN'
    if len(temp) == len(errors):
        errors, result, _ = evaluate_visible(lexeme, line, symbol_table, 0, errors)
        if len(temp) == len(errors):
            return errors, result
    return errors, None

def statement(lexeme, line, errors, symbol_table, function_table):
        # printing output
    if lexeme[0][0] == 'VISIBLE':
        return visible(lexeme[1:], line, errors, symbol_table)
    
    # taking input
    if lexeme[0][0] == 'GIMMEH':
        if len(lexeme) > 2 or len(lexeme) <= 1:
            return errors + f"syntax error at line {line+1}: Incorrect GIMMEH syntax!\n", None
        if lexeme[1][1] != 'Identifier':
            return errors + f"syntax error at line {line+1}: Incorrect GIMMEH syntax!\n", None
        if lexeme[1][0] not in symbol_table:
            return errors + f"syntax error at line {line+1}: Variable {lexeme[1][0]} not declared!\n", None
        symbol_table[lexeme[1][0]] = evaluate_gimmeh()
        return errors, None  # Correct GIMMEH syntax
    
    if lexeme[0][0] == 'I IZ':
        if len(lexeme) < 4:
             return errors + f"syntax error at line {line+1}: Incorrect 'I IZ' syntax!\n", None
        return func_call_arg(lexeme, line, function_table, symbol_table, errors), None

    # handle assignment, casting, and expressions
    if len(lexeme) >= 3:  # assignment or expression has at least 3 tokens
        # assignment
        if ['R', 'Variable Assignment'] == lexeme[1]:
            return assignment(lexeme, symbol_table, line, errors), None
        
        # casting
        elif ['MAEK', 'Typecasting Operation'] == lexeme[0] or ['IS NOW A', 'Typecasting Operation'] == lexeme[1]:
            return casting(lexeme, line, symbol_table, errors), None
        
        # expression
        else:
            return expression(lexeme, line, errors, symbol_table)[0], None

    errors += f"syntax error at line {line + 1}: Unexpected syntax\n"
    return errors