import lexical
from syntax_funcs.comment import comment
from syntax_funcs.statement import statement
from syntax_funcs.statement import expression

def func_arg(lexeme, line, syntaxResult):
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
            if index+1>=len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after 'AN' in function declaration\n"
                break
            if lexeme[index][0] != 'AN' or lexeme[index+1][0] != 'YR':
                syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in function arguments\n"
                break
            if index+2>=len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Insufficient function arguments\n"
                break
            index += 2  # Move past 'AN'

    return syntaxResult

def function(text, start, syntaxResult, symbol_table, obtw, tldr):
    # Variables to track the function state
    function_start_found = False
    gtfo_found = False
    foundyr_found = False
    parameters = []
    function_name = None
    inside_function = False
    
    def is_gtfo(lexeme):
        return lexeme[0][0] == 'GTFO'
    
    def is_found_yr(lexeme):
        return lexeme[0][0] == 'FOUND YR'
    
    def is_if_u_say_so(lexeme):
        return lexeme[0][0] == 'IF U SAY SO'

    
    # check function declaration
    lexeme = lexical.lex(text.splitlines()[start].strip())

    if len(lexeme) < 2:
        syntaxResult += f"syntax error at line {start + 1}: Incorrect format for function definition\n"
        return start, syntaxResult
    if lexeme[1][1] != 'Identifier':
        syntaxResult += f"syntax error at line {start + 1}: Expected function identifier right after 'HOW IZ I'\n"
        return start, syntaxResult
    function_name = lexeme[1][0]  # Assuming the function name is right after HOW IZ I
    if len(lexeme)>2:
        if lexeme[2][0] != 'YR':
            syntaxResult += f"syntax error at line {start + 1}: Incorrect function declaration syntax\n"
            return line, syntaxResult
        temp = syntaxResult
        syntaxResult = func_arg(lexeme[3:], start, syntaxResult)
        if len(temp) < len(syntaxResult):  # Syntax error occurred
            return start, syntaxResult
    # Main processing of the function block
    for line in range(start+1, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        if comment(lexeme, obtw, tldr):
            continue
        print(lexeme[0][0])
        # Check for GTFO 
        if is_gtfo(lexeme):
            # Check if there is at least one OMG or OMGWTF case before ending
            if is_found_yr(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: 'GTFO' cannot be declared after 'FOUND YR' declaration\n"
                return line, syntaxResult
            gtfo_found = True
            continue

        if is_found_yr(lexeme):
            if is_gtfo(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: 'GTFO' cannot be declared after 'FOUND YR' declaration\n"
                return line, syntaxResult
            foundyr_found = True
            continue

        if is_if_u_say_so(lexeme):
            if not gtfo_found and not foundyr_found:
                syntaxResult += f"syntax error at line {line + 1}: 'IF U SAY SO' cannot be declared without a 'FOUND YR' pr 'GTFO' declaration\n"
                return line, syntaxResult
            return line, syntaxResult

        # Process statements inside the function body
        if not gtfo_found and not foundyr_found:
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