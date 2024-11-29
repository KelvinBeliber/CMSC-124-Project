from syntax_funcs.statement import statement
import lexical

def func_call(lexeme, line, syntaxResult, symbol_table):
        # I IZ
        if lexeme[0][0] != 'I IZ':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'I IZ' for function call\n"
            return syntaxResult
        index = 1

        # function identifier
        if lexeme[index][1] != 'Identifier' or lexeme[index][0] not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Undefined function '{lexeme[index][0]}'\n"
            return syntaxResult
        index += 1

        # YR
        if lexeme[index][0] != 'YR':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after function identifier\n"
            return syntaxResult
        index += 1

        # call function argument
        syntaxResult, index = func_arg(lexeme, line, syntaxResult, symbol_table, index)

        # MKAY
        if lexeme[index][0] != 'MKAY':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'MKAY' at the end of function call\n"
            return syntaxResult

        return syntaxResult

def func_arg(lexeme, line, syntaxResult, symbol_table, index):
    # first argument
    if lexeme[index][1] != 'Identifier':
        syntaxResult += f"syntax error at line {line + 1}: Invalid function argument\n"
        return syntaxResult, index
    index += 1

    # AN YR
    while index < len(lexeme) and lexeme[index][0] == 'AN':
        index += 1  # Skip "AN"
        if lexeme[index][0] != 'YR':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after 'AN' in arguments\n"
            return syntaxResult, index
        index += 1
        if lexeme[index][1] != 'Identifier':
            syntaxResult += f"syntax error at line {line + 1}: Invalid argument after 'AN YR'\n"
            return syntaxResult, index
        index += 1

    return syntaxResult, index

def function(text, start, syntaxResult, symbol_table):
    funcdec = False

    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        # HOW IZ I
        if funcdec == False:
            if lexeme[0][0] != 'HOW IZ I':
                syntaxResult += f"syntax error at line {line + 1}: Expected 'HOW IZ I' for function definition\n"
                return syntaxResult
            index = 1

            # function identifier
            if lexeme[index][1] != 'Identifier':
                syntaxResult += f"syntax error at line {line + 1}: Missing or invalid function identifier\n"
                return syntaxResult
            # func_name = lexeme[index][0]
            # symbol_table[func_name] = 'Function'  # Add to symbol table
            index += 1

            # YR
            if lexeme[index][0] != 'YR':
                syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after function identifier\n"
                return syntaxResult
            index += 1

            # call function argument
            syntaxResult, index = func_arg(lexeme, line, syntaxResult, symbol_table, index)

        # statement
        print(lexeme)
        if lexeme[0][0] != 'FOUND YR':  # look for return statement instead of linebreak
            #para sa statement checker
            syntaxResult, index = statement(lexeme, line, syntaxResult, symbol_table, index)
            continue

        # check for function return
        if lexeme[index][0] != 'FOUND YR':
            syntaxResult += f"syntax error at line {line + 1}: Missing return statement 'FOUND YR'\n"
            return syntaxResult
        index += 1

        # check return value
        if lexeme[index][1] not in ['Identifier', 'Literal']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid return value in function\n"
            return syntaxResult
        index += 1

        # check for "IF U SAY SO"
        if lexeme[index][0] != 'IF U SAY SO':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'IF U SAY SO' to end function definition\n"
            return syntaxResult

        return syntaxResult

        # Determine if it's a function definition or function call
        if lexeme[0][0] == 'HOW IZ I':
            syntaxResult = func_def(lexeme, line, syntaxResult, symbol_table)
        elif lexeme[0][0] == 'I IZ':
            syntaxResult = func_call(lexeme, line, syntaxResult, symbol_table)
        else:
            syntaxResult += f"syntax error at line {line + 1}: Unexpected token '{lexeme[0][0]}'\n"
    
    return syntaxResult