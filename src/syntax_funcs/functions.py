import lexical
from syntax_funcs.comment import btw_comment
from syntax_funcs.comment import obtw_comment
from syntax_funcs.statement import statement
from syntax_funcs.statement import expression

def func_def_arg(lexeme, line, errors):
    index = 0
    multi_comment_found = False
    function_table = {}
    while index < len(lexeme):
        # Validate operand
        if lexeme[index][1] != 'Identifier':
            errors += f"syntax error at line {line + 1}: Invalid function argument\n"
            break
        else:
            var_name = lexeme[index][0]
            if var_name in function_table:
                errors += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
                break
            function_table[var_name] = ''
        index += 1

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

    return errors, function_table

def func_def(text, start, errors, function_table):
    # Variables to track the function state
    gtfo_found = False
    foundyr_found = False
    function_name = None
    function_lines = 0
    multi_comment = False
    lines_processed = 1
    local_symbol_table = {}
    function_code = ''
    
    def is_gtfo(lexeme):
        return lexeme[0][0] == 'GTFO'
    
    def is_found_yr(lexeme):
        return lexeme[0][0] == 'FOUND YR'
    
    def is_if_u_say_so(lexeme):
        return lexeme[0][0] == 'IF U SAY SO'

    
    # check function declaration
    lexeme = lexical.lex(text.splitlines()[start].strip())
    if len(lexeme) < 2:
        errors += f"syntax error at line {start + 1}: Incorrect format for function definition\n"
        return start, errors
    if lexeme[1][1] != 'Identifier':
        errors += f"syntax error at line {start + 1}: Expected function identifier right after 'HOW IZ I'\n"
        return start, errors
    function_name = lexeme[1][0]  # Assuming the function name is right after HOW IZ I
    if len(lexeme)>2:
        if lexeme[2][0] != 'YR':
            errors += f"syntax error at line {start + 1}: Incorrect function declaration syntax\n"
            return line, errors
        temp = errors
        errors, local_symbol_table = func_def_arg(lexeme[3:], start, errors)
        if len(temp) < len(errors):  # Syntax error occurred
            return start, errors
    # Main processing of the function block
    for line in range(start+1, len(text.splitlines())):
        lines_processed+=1
        lexeme = lexical.lex(text.splitlines()[line].strip())
        ## comment skipping
        lexeme = btw_comment(lexeme)
        if len(lexeme) == 0:
            continue
        if lexeme[0] == ['OBTW', 'Comment Delimiter'] or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            multi_comment = obtw_comment(errors, lexeme, line, len(text.splitlines()), multi_comment)
            if type(multi_comment) == str:
                errors += multi_comment
                break
        if multi_comment or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            continue
        # Check for GTFO 
        if is_gtfo(lexeme):
            # Check if there is at least one OMG or OMGWTF case before ending
            if is_found_yr(lexeme):
                errors += f"syntax error at line {line + 1}: 'GTFO' cannot be declared after 'FOUND YR' declaration\n"
                return errors, None
            gtfo_found = True
            function_code += text.splitlines()[line].strip() + "\n"
            function_lines+=1
            continue

        if is_found_yr(lexeme):
            if is_gtfo(lexeme):
                errors += f"syntax error at line {line + 1}: 'GTFO' cannot be declared after 'FOUND YR' declaration\n"
                return errors, None
            foundyr_found = True
            function_code += text.splitlines()[line].strip() + "\n"
            function_lines+=1
            continue

        if is_if_u_say_so(lexeme):
            if not gtfo_found and not foundyr_found:
                errors += f"syntax error at line {line + 1}: 'IF U SAY SO' cannot be declared without a 'FOUND YR' pr 'GTFO' declaration\n"
                return errors, None
            function_table[function_name] = {'local_symbol_table': local_symbol_table, 'function_code': function_code}
            return errors, lines_processed

        # Process statements inside the function body
        if not gtfo_found and not foundyr_found:
            temp = errors
            errors,_ = statement(lexeme, line, errors, local_symbol_table, function_table, True)
            if len(temp) < len(errors):  # Syntax error occurred
                return errors, None
            function_code += text.splitlines()[line].strip() + "\n"
            function_lines+=1
            continue



        # Handle invalid lines within the function block
        errors += f"syntax error at line {line + 1}: Unexpected syntax in function block\n"
        return errors, lines_processed

    # If we exit the loop without finding IF U SAY SO
    errors += f"syntax error: 'IF U SAY SO' not found to close function block\n"
    return lines_processed