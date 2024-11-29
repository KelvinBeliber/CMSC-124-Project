import lexical
from syntax_funcs.comment import comment
from syntax_funcs.statement import statement
from syntax_funcs.statement import expression

def func_arg(lexeme, line, syntaxResult, symbol_table):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]


    index = 0
    while index < len(lexeme):
        # Validate operand
        if lexeme[index][1] != 'Identifier':
            print(lexeme, "\n", lexeme[index], index)
            syntaxResult += f"syntax error at line {line + 1}: Invalid function argument\n"
            break
        index += 1

        # Check if there's an 'AN' keyword after each operand except the last
        if index < len(lexeme):
            if lexeme[index][0] != 'AN' or lexeme[index+1][0] != 'YR':
                syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in function arguments\n"
                break
            if index+1>=len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Insufficient function arguments\n"
                break
            index += 2  # Move past 'AN'

    return syntaxResult

def function(text, start, syntaxResult, symbol_table, obtw, tldr):
    # Variables to track the function state
    function_start_found = False
    parameters = []
    function_name = None
    inside_function = False

    # Helper function to check if it's the start of a HOW IZ I function definition
    def is_valid_how_iz_i_start(lexeme):
        return lexeme[0][0] == 'HOW IZ I'

    # Helper function to check for the YR keyword (for parameters)
    def is_yr(lexeme):
        return lexeme[0][0] == 'YR'

    # Helper function to check for the AN YR keyword (for multiple parameters)
    def is_an_yr(lexeme):
        return lexeme[0][0] == 'AN YR'

    # Helper function to check for the FOUND YR keyword (for expressions)
    def is_found_yr(lexeme):
        return lexeme[0][0] == 'FOUND YR'

    # Helper function to check for the IF U SAY SO closing keyword
    def is_if_u_say_so(lexeme):
        return lexeme[0][0] == 'IF U SAY SO'

    # Main processing of the function block
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        
        if comment(lexeme, obtw, tldr):
            continue
        
        # Check for the start of the function definition
        if not function_start_found:
            if is_valid_how_iz_i_start(lexeme):
                if len(lexeme) < 2:
                    syntaxResult += f"syntax error at line {line + 1}: Incorrect format for function definition\n"
                    return line, syntaxResult

                function_start_found = True
                if lexeme[1][1] != 'Identifier':
                    syntaxResult += f"syntax error at line {line + 1}: Expected function identifier right after 'HOW IZ I'\n"
                    return line, syntaxResult
                function_name = lexeme[1][0]  # Assuming the function name is right after HOW IZ I
                if len(lexeme)>2:
                    if lexeme[2][0] != 'YR':
                        syntaxResult += f"syntax error at line {line + 1}: Incorrect function declaration syntax\n"
                        return line, syntaxResult
                    temp = syntaxResult
                    syntaxResult = func_arg(lexeme[3:], line, syntaxResult, symbol_table)
                    if len(temp) < len(syntaxResult):  # Syntax error occurred
                        return line, syntaxResult
                continue
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'HOW IZ I <function name>' to start function definition\n"
                return line, syntaxResult
        
        # Check for parameters (YR and AN YR)
        # if is_yr(lexeme) and not parameters:
        #     parameters.append(lexeme[1][0])  # Add first parameter
        #     continue
        # elif is_an_yr(lexeme):
        #     parameters.append(lexeme[1][0])  # Add additional parameter
        #     continue

        # Check for the FOUND YR expression
        if is_found_yr(lexeme):
            # Handle the expression part after FOUND YR
            line += 1
            lexeme = lexical.lex(text.splitlines()[line].strip())
            syntaxResult = expression(lexeme, line, syntaxResult, symbol_table)[0]
            if syntaxResult.endswith("error"):  # Assuming expression appends "error" on failure
                return line, syntaxResult
            continue

        # Check for the closing IF U SAY SO
        if is_if_u_say_so(lexeme):
            if not function_start_found:
                syntaxResult += f"syntax error at line {line + 1}: 'IF U SAY SO' without a preceding function definition\n"
                return line, syntaxResult

            # If no statements were found or the function block was empty
            if not inside_function:
                syntaxResult += f"syntax error at line {line + 1}: Function block must contain at least one statement\n"
                return line, syntaxResult

            return line, syntaxResult

        # Process statements inside the function body
        if function_start_found and not inside_function:
            temp = syntaxResult
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)
            if len(temp) < len(syntaxResult):  # Syntax error occurred
                return line, syntaxResult
            inside_function = True
            continue

        # Handle invalid lines within the function block
        syntaxResult += f"syntax error at line {line + 1}: Unexpected syntax in function block\n"
        return line, syntaxResult

    # If we exit the loop without finding IF U SAY SO
    syntaxResult += f"syntax error: 'IF U SAY SO' not found to close function block\n"
    return line, syntaxResult
