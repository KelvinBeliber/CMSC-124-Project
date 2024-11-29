def operator(lexeme, line, syntaxResult, symbol_table, index=0):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]

    def comparison(lexeme, line, syntaxResult, symbol_table, index):
        def is_valid_expression(lexeme, index, syntaxResult):
            """Helper function to validate an arithmetic or logical expression."""
            if lexeme[index][0] in operators:  # Check for nested operators
                temp = syntaxResult
                syntaxResult, next_index = operator(lexeme, line, syntaxResult, symbol_table, index)
                if len(temp) < len(syntaxResult):  # Syntax error occurred
                    return False, syntaxResult, next_index
                return True, syntaxResult, next_index
            elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return False, syntaxResult, index
                return True, syntaxResult, index + 1  # Move to next index
            else:
                return False, syntaxResult, index
        # Check for BOTH SAEM or DIFFRINT keyword
        if lexeme[index][0] not in ['BOTH SAEM', 'DIFFRINT']:
            syntaxResult += f"syntax error at line {line + 1}: Expected boolean comparison operator\n"
            return syntaxResult, index + 1

        comparison_type = lexeme[index][0]  # Save comparison type (BOTH SAEM / DIFFRINT)
        index += 1  # Move to the first operand

        # Validate the first operand
        if index >= len(lexeme):
            syntaxResult += f"syntax error at line {line + 1}: Missing first operand in comparison\n"
            return syntaxResult, index

        is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
        if not is_valid:
            syntaxResult += f"syntax error at line {line + 1}: Invalid operand in {comparison_type} expression\n"
            return syntaxResult, index
        index = next_index

        # Check for 'AN' keyword
        if index >= len(lexeme) or lexeme[index][0] != 'AN':
            syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' after first operand\n"
            return syntaxResult, index
        index += 1  # Move past 'AN'

        # Validate the second operand (supports BIGGR OF and SMALLR OF)
        if index >= len(lexeme):
            syntaxResult += f"syntax error at line {line + 1}: Missing second operand in comparison\n"
            return syntaxResult, index

        if lexeme[index][0] in ['BIGGR OF', 'SMALLR OF']:
            # Handle nested arithmetic expression (BIGGR OF / SMALLR OF)
            nested_operator = lexeme[index][0]
            index += 1  # Move to the first operand of BIGGR OF / SMALLR OF

            # Validate first operand of BIGGR OF / SMALLR OF
            if index >= len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Missing first operand for '{nested_operator}'\n"
                return syntaxResult, index
            if lexeme[index][1] == 'Identifier' and lexeme[index][0] not in symbol_table:
                syntaxResult += f"syntax error at line {line + 1}: Variable '{lexeme[index][0]}' not declared\n"
                return syntaxResult, index
            elif lexeme[index][1] not in literals and lexeme[index][1] != 'Identifier':
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand for '{nested_operator}'\n"
                return syntaxResult, index
            index += 1

            # Check for 'AN' keyword
            if index >= len(lexeme) or lexeme[index][0] != 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' keyword in '{nested_operator}'\n"
                return syntaxResult, index
            index += 1  # Move past 'AN'

            # Validate second operand of BIGGR OF / SMALLR OF
            if index >= len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Missing second operand for '{nested_operator}'\n"
                return syntaxResult, index
            if lexeme[index][1] == 'Identifier' and lexeme[index][0] not in symbol_table:
                syntaxResult += f"syntax error at line {line + 1}: Variable '{lexeme[index][0]}' not declared\n"
                return syntaxResult, index
            elif lexeme[index][1] not in literals and lexeme[index][1] != 'Identifier':
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand for '{nested_operator}'\n"
                return syntaxResult, index
            index += 1

        else:
            # Validate second operand directly (non-nested case)
            is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
            if not is_valid:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in {comparison_type} expression\n"
                return syntaxResult, index
            index = next_index

        # Successfully parsed comparison
        return syntaxResult, index


    def boolean(lexeme, line, syntaxResult, symbol_table, index):
        def is_valid_expression(lexeme, index, syntaxResult):
            """Helper function to validate an arithmetic or logical expression."""
            if lexeme[index][0] in operators:  # Check for nested operators
                temp = syntaxResult
                syntaxResult, next_index = operator(lexeme, line, syntaxResult, symbol_table, index)
                if len(temp) < len(syntaxResult):  # Syntax error occurred
                    return False, syntaxResult, next_index
                return True, syntaxResult, next_index
            elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return False, syntaxResult, index
                return True, syntaxResult, index + 1  # Move to next index
            else:
                return False, syntaxResult, index

        boolType = lexeme[index][0]
        index += 1  # Move past the operator

        # Handle infinite-arity boolean operators (ALL OF, ANY OF)
        if boolType in operators[11:13]:  # ALL OF, ANY OF
            has_operands = False
            while index < len(lexeme):
                # Check for the terminating MKAY
                if lexeme[index][0] == 'MKAY':
                    if not has_operands:
                        syntaxResult += f"syntax error at line {line + 1}: {boolType} requires at least one operand\n"
                    return syntaxResult, index + 1  # Move past MKAY

                # Validate each operand
                is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
                if not is_valid:
                    syntaxResult += f"syntax error at line {line + 1}: Invalid operand in {boolType} expression\n"
                    return syntaxResult, index
                index = next_index
                has_operands = True

                # Check if there's an 'AN' keyword between operands
                if index < len(lexeme) and lexeme[index][0] == 'AN':
                    index += 1  # Move past 'AN'
                elif index < len(lexeme) and lexeme[index][0] != 'MKAY':
                    syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in {boolType} expression\n"
                    return syntaxResult, index

            # If loop ends without finding MKAY
            syntaxResult += f"syntax error at line {line + 1}: Missing 'MKAY' to terminate {boolType} expression\n"
            return syntaxResult, index

        # Handle NOT operator
        elif boolType == 'NOT':
            is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
            if not is_valid:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in NOT expression\n"
                return syntaxResult, index
            index = next_index

        # Handle binary boolean operators (BOTH OF, EITHER OF, WON OF)
        elif boolType in operators[7:10]:
            for _ in range(2):  # Expect exactly two operands
                if index >= len(lexeme):
                    syntaxResult += f"syntax error at line {line + 1}: Missing operand in {boolType} expression\n"
                    return syntaxResult, index

                is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
                if not is_valid:
                    syntaxResult += f"syntax error at line {line + 1}: Invalid operand in {boolType} expression\n"
                    return syntaxResult, index
                index = next_index

                # Check for 'AN' keyword between operands
                if _ == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
                    index += 1
                elif _ == 0:  # If missing 'AN'
                    syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' keyword in {boolType} expression\n"
                    return syntaxResult, index

        else:
            syntaxResult += f"syntax error at line {line + 1}: Invalid boolean operator '{boolType}'\n"
            return syntaxResult, index

        return syntaxResult, index



    def arithmetic(lexeme, line, syntaxResult, symbol_table, index):
        # Simplified Arithmetic Implementation
        if lexeme[index][0] not in operators[:7]:  # Check for arithmetic operators
            syntaxResult += f"syntax error at line {line + 1}: Invalid arithmetic operator '{lexeme[index][0]}'\n"
            return syntaxResult, index + 1

        index += 1  # Move to first operand
        for i in range(2):  # Two operands expected
            if index >= len(lexeme) or lexeme[index][0] == 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Incomplete arithmetic expression\n"
                return syntaxResult, index

            if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return syntaxResult, index
                index += 1
            elif lexeme[index][0] in operators:  # Nested operator
                syntaxResult, index = operator(lexeme, line, syntaxResult, symbol_table, index)
            else:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic expression\n"
                return syntaxResult, index

            # Check for 'AN' keyword between operands
            if i == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
                index += 1
        return syntaxResult, index

    def smoosh(lexeme, line, syntaxResult, symbol_table, index):
        # Simplified SMOOSH Implementation
        if lexeme[index][0] != 'SMOOSH':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'SMOOSH'\n"
            return syntaxResult, index + 1

        index += 1
        def is_valid_expression(lexeme, index, syntaxResult):
            """Helper function to validate an arithmetic or logical expression."""
            if lexeme[index][0] in operators:  # Check for nested expressions
                syntaxResult, end_index = operator(lexeme, line, syntaxResult, symbol_table, index)
                return True, syntaxResult, end_index
            elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return False, syntaxResult, index
                return True, syntaxResult, index + 1  # Move to next index
            else:
                return False, syntaxResult, index
            
        while index < len(lexeme):
            # Validate operand
            is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
            if not is_valid:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in SMOOSH expression\n"
                return syntaxResult, index
            index = next_index

            # Check if there's an 'AN' keyword after each operand except the last
            if index < len(lexeme):
                if lexeme[index][0] != 'AN':
                    syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in SMOOSH arguments\n"
                    return syntaxResult, index
                if index+1>=len(lexeme):
                    syntaxResult += f"syntax error at line {line + 1}: Insufficient SMOOSH arguments\n"
                    return syntaxResult, index
                index += 1  # Move past 'AN'
                
        return syntaxResult, index

    # Determine which operator function to call
    if lexeme[index][0] in ['SMOOSH']:
        return smoosh(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[:7]:  # Arithmetic operators
        return arithmetic(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[7:13]:  # Boolean operators
        return boolean(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[13:15]:  # comparison operators
        return comparison(lexeme, line, syntaxResult, symbol_table, index)
    else:
        syntaxResult += f"syntax error at line {line + 1}: Unknown operator '{lexeme[index][0]}'\n"
        return syntaxResult, index + 1