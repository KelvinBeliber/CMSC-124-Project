from statement import statement

def function(lexeme, line, syntaxResult, symbol_table, index=0):
    def func_def(lexeme, line, syntaxResult, symbol_table, index):
        # HOW IZ I
        if lexeme[index][0] != 'HOW IZ I':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'HOW IZ I' for function definition\n"
            return syntaxResult, index + 1
        index += 1

        # function identifier
        if lexeme[index][1] != 'Identifier':
            syntaxResult += f"syntax error at line {line + 1}: Missing or invalid function identifier\n"
            return syntaxResult, index + 1
        func_name = lexeme[index][0]
        symbol_table[func_name] = 'Function'  #add to symbol table
        index += 1

        # YR
        if lexeme[index][0] != 'YR':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after function identifier\n"
            return syntaxResult, index + 1
        index += 1

        # call function argument
        syntaxResult, index = func_arg(lexeme, line, syntaxResult, symbol_table, index)

        # linebreak
        if lexeme[index][0] != '<linebreak>':
            syntaxResult += f"syntax error at line {line + 1}: Expected linebreak after function arguments\n"
            return syntaxResult, index + 1
        index += 1

        # Validate function body (statements)
        while lexeme[index][0] != '<linebreak>':  # End body on linebreak
            # Assuming statement is defined elsewhere for general statement validation
            syntaxResult, index = statement(lexeme, line, syntaxResult, symbol_table, index)

        index += 1  # Skip linebreak

        # Check for function return
        if lexeme[index][0] != 'FOUND YR':
            syntaxResult += f"syntax error at line {line + 1}: Missing return statement 'FOUND YR'\n"
            return syntaxResult, index + 1
        index += 1

        # Check return value
        if lexeme[index][1] not in ['Identifier', 'Literal']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid return value in function\n"
            return syntaxResult, index + 1
        index += 1

        # Check for "IF U SAY SO"
        if lexeme[index][0] != 'IF U SAY SO':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'IF U SAY SO' to end function definition\n"
            return syntaxResult, index + 1

        return syntaxResult, index + 1

    def func_call(lexeme, line, syntaxResult, symbol_table, index):
        # I IZ
        if lexeme[index][0] != 'I IZ':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'I IZ' for function call\n"
            return syntaxResult, index + 1
        index += 1

        # function identifier
        if lexeme[index][1] != 'Identifier' or lexeme[index][0] not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Undefined function '{lexeme[index][0]}'\n"
            return syntaxResult, index + 1
        index += 1

        # YR
        if lexeme[index][0] != 'YR':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after function identifier\n"
            return syntaxResult, index + 1
        index += 1

        # call function argument
        syntaxResult, index = func_arg(lexeme, line, syntaxResult, symbol_table, index)

        # MKAY
        if lexeme[index][0] != 'MKAY':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'MKAY' at the end of function call\n"
            return syntaxResult, index + 1

        return syntaxResult, index + 1

    def func_arg(lexeme, line, syntaxResult, symbol_table, index):
        # first argument
        if lexeme[index][1] != 'Identifier':
            syntaxResult += f"syntax error at line {line + 1}: Invalid function argument\n"
            return syntaxResult, index + 1
        index += 1

        # AN YR
        while index < len(lexeme) and lexeme[index][0] == 'AN':
            index += 1  # Skip "AN"
            if lexeme[index][0] != 'YR':
                syntaxResult += f"syntax error at line {line + 1}: Expected 'YR' after 'AN' in arguments\n"
                return syntaxResult, index + 1
            index += 1
            if lexeme[index][1] != 'Identifier':
                syntaxResult += f"syntax error at line {line + 1}: Invalid argument after 'AN YR'\n"
                return syntaxResult, index + 1
            index += 1

        return syntaxResult, index

    if lexeme[index][0] == 'HOW IZ I':
        return func_def(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] == 'I IZ':
        return func_call(lexeme, line, syntaxResult, symbol_table, index)
    else:
        syntaxResult += f"syntax error at line {line + 1}: Unexpected token '{lexeme[index][0]}'\n"
        return syntaxResult, index + 1