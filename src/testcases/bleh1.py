def bool(lexeme, line, syntaxResult, symbol_table, index):
        boolean_operators = operators[7:13]  # Boolean operators: 'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF'
        def infarity(lexeme, line, syntaxResult, symbol_table):
            literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
            operators = [
                'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
                'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
                'BOTH SAEM', 'DIFFRINT',
                'SMOOSH'
            ]

            def is_valid_expression(lexeme, index, syntaxResult,symbol_table):
                """Helper function to validate an expression."""
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

            index = 0
            while index < len(lexeme):
                # Validate operand
                is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult, symbol_table)
                if not is_valid:
                    syntaxResult += f"syntax error at line {line + 1}: Invalid operand in boolean expression\n"
                    break
                index = next_index
                # Check if there's an 'AN' keyword after each operand except the last
                if index < len(lexeme):
                    if lexeme[index][0] != 'AN':
                        syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in boolean arguments\n"
                        break
                    index += 1  # Move past 'AN'

            return syntaxResult
        
        # If it's a NOT operator, it only takes one operand
        if lexeme[index][0] == 'NOT':
            index += 1
            if index >= len(lexeme) or lexeme[index][0] == 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Incomplete NOT expression\n"
                return syntaxResult, index

            # Check the operand after NOT
            if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return syntaxResult, index
                index += 1
            elif lexeme[index][0] in operators:  # Nested operator
                syntaxResult, index = operator(lexeme, line, syntaxResult, symbol_table, index)
            else:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in NOT expression\n"
                return syntaxResult, index

            return syntaxResult, index

        # Handle 'ALL OF' and 'ANY OF', which can take multiple operands
        if lexeme[index][0] in ['ALL OF', 'ANY OF']:
            syntaxResult = visible(lexeme[index+1:], line, syntaxResult, symbol_table)
            

        # Handle other boolean operators (e.g., 'BOTH OF', 'EITHER OF', 'WON OF')
        if lexeme[index][0] in boolean_operators:
            index += 1
            for i in range(2):  # Two operands expected
                if index >= len(lexeme) or lexeme[index][0] == 'AN':
                    syntaxResult += f"syntax error at line {line + 1}: Incomplete boolean expression\n"
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
                    syntaxResult += f"syntax error at line {line + 1}: Invalid operand in boolean expression\n"
                    return syntaxResult, index

                # Check for 'AN' keyword between operands
                if i == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
                    index += 1

            return syntaxResult, index
        



for i in range(0,len(lexeme)):
                ## ----------------------------- CHECKS PER WORD -----------------------------
                # check for hai keyword
                if skip>0:
                    skip-=1
                    break
                if lexeme[i][0] != 'HAI' and hai!=1:
                    return f'syntax error at line 0: HAI is not declared'
                if  hai == -1 and kthxbye == -1:
                    hai = 1
                # check for declaration keyword
                if lexeme[i][0] == 'WAZZAP' or lexeme[i][0] == 'BUHBYE' and wazzup == 0 and buhbye == 0:
                    syntaxResult += f"syntax error at line {line+1}: WAZZUP-BUHBYE block has already been declared\n"
                    break
                if lexeme[i][0] == 'WAZZUP':
                    if wazzup != -1:
                        syntaxResult += f"syntax error at line {line+1}: WAZZUP has already been declared\n"
                        break
                    if buhbye != -1:
                        syntaxResult += f"syntax error at line {line+1}: WAZZUP cannot be declared after BUHBYE\n"
                        break
                    if wazzup == -1 and buhbye == -1:
                        vardecResult = vardec(text, line+1, 0, symbol_table, syntaxResult, obtw, tldr)
                        skip = vardecResult[0]-line
                        symbol_table = vardecResult[1]
                        syntaxResult = vardecResult[2]
                        wazzup = 1
                        break
                if lexeme[i][0] == 'BUHBYE':
                    if wazzup != 1:
                        syntaxResult += f"syntax error at line {line+1}: BUHBYE declared without a WAZZUP\n"
                        break
                    elif buhbye != -1:
                        syntaxResult += f"syntax error at line {line+1}: BUHBYE has already been declared\n"
                        break
                    else:
                        wazzup = 0
                        buhbye = 0
                        break