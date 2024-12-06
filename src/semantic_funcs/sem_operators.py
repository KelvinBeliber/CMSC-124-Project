literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

def sem_comparison(lexeme, line, semanticResult, symbol_table):
    # check if the first token is a comparison operator
    if lexeme[0][0] not in ['BOTH SAEM', 'DIFFRINT']:
        semanticResult += f"semantic error at line {line + 1}: Expected a comparison operator 'BOTH SAEM' or 'DIFFRINT'\n"
        return semanticResult

    comparison_type = lexeme[0][0]  # Save comparison type

    # Validate the first operand
    if len(lexeme) < 2:
        semanticResult += f"semantic error at line {line + 1}: Missing first operand in '{comparison_type}' comparison\n"
        return semanticResult

    first_operand = lexeme[1]
    if first_operand[1] == 'Identifier' and first_operand[0] not in symbol_table:
        semanticResult += f"semantic error at line {line + 1}: Variable '{first_operand[0]}' not declared\n"
        return semanticResult
    elif first_operand[1] not in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'YARN Literal', 'Identifier']:
        semanticResult += f"semantic error at line {line + 1}: Invalid first operand type '{first_operand[1]}'\n"
        return semanticResult

    # Validate 'AN' keyword
    if len(lexeme) < 3 or lexeme[2][0] != 'AN':
        semanticResult += f"semantic error at line {line + 1}: Missing 'AN' keyword after first operand\n"
        return semanticResult

    # Validate the second operand
    if len(lexeme) < 4:
        semanticResult += f"semantic error at line {line + 1}: Missing second operand in '{comparison_type}' comparison\n"
        return semanticResult

    second_operand = lexeme[3]
    if second_operand[1] == 'Identifier' and second_operand[0] not in symbol_table:
        semanticResult += f"semantic error at line {line + 1}: Variable '{second_operand[0]}' not declared\n"
        return semanticResult
    elif second_operand[1] not in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'YARN Literal', 'Identifier']:
        semanticResult += f"semantic error at line {line + 1}: Invalid second operand type '{second_operand[1]}'\n"
        return semanticResult

    # compatibility of operand types 
    if first_operand[1] != second_operand[1] and 'Literal' in first_operand[1] and 'Literal' in second_operand[1]:
        semanticResult += f"semantic error at line {line + 1}: Type mismatch between operands in '{comparison_type}' comparison\n"
        return semanticResult

    # No semantic errors found
    return semanticResult

def sem_boolean(lexeme, line, semanticResult, symbol_table):
    boolType = lexeme[0][0]  # extract the boolean operator

    # handle infinite-arity boolean operators (ALL OF, ANY OF)
    if boolType in ['ALL OF', 'ANY OF']:
        has_operands = False
        for i in range(1, len(lexeme)):
            token = lexeme[i]

            # check for the terminating 'MKAY'
            if token[0] == 'MKAY':
                if not has_operands:
                    semanticResult += f"semantic error at line {line + 1}: {boolType} requires at least one operand\n"
                return semanticResult

            # Validate each operand
            if token[1] == 'Identifier' and token[0] not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{token[0]}' not declared\n"
                return semanticResult
            elif token[1] not in ['TROOF Literal', 'Identifier']:
                semanticResult += f"semantic error at line {line + 1}: Invalid operand type '{token[1]}' in {boolType} expression\n"
                return semanticResult
            has_operands = True

        # If no 'MKAY' is found
        semanticResult += f"semantic error at line {line + 1}: Missing 'MKAY' to terminate {boolType} expression\n"
        return semanticResult

    # Handle NOT operator
    elif boolType == 'NOT':
        if len(lexeme) < 2:
            semanticResult += f"semantic error at line {line + 1}: Missing operand in NOT expression\n"
            return semanticResult

        operand = lexeme[1]
        if operand[1] == 'Identifier' and operand[0] not in symbol_table:
            semanticResult += f"semantic error at line {line + 1}: Variable '{operand[0]}' not declared\n"
            return semanticResult
        elif operand[1] not in ['TROOF Literal', 'Identifier']:
            semanticResult += f"semantic error at line {line + 1}: Invalid operand type '{operand[1]}' in NOT expression\n"
            return semanticResult

    # Handle binary boolean operators (BOTH OF, EITHER OF, WON OF)
    elif boolType in ['BOTH OF', 'EITHER OF', 'WON OF']:
        if len(lexeme) < 4:
            semanticResult += f"semantic error at line {line + 1}: Missing operands in {boolType} expression\n"
            return semanticResult

        for i in [1, 3]:  # Validate both operands
            operand = lexeme[i]
            if operand[1] == 'Identifier' and operand[0] not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{operand[0]}' not declared\n"
                return semanticResult
            elif operand[1] not in ['TROOF Literal', 'Identifier']:
                semanticResult += f"semantic error at line {line + 1}: Invalid operand type '{operand[1]}' in {boolType} expression\n"
                return semanticResult

        # Ensure 'AN' keyword exists between operands
        if lexeme[2][0] != 'AN':
            semanticResult += f"semantic error at line {line + 1}: Missing 'AN' keyword in {boolType} expression\n"
            return semanticResult

    else:
        semanticResult += f"semantic error at line {line + 1}: Invalid boolean operator '{boolType}'\n"
        return semanticResult

    # No semantic errors found
    return semanticResult

def sem_arithmetic(lexeme, line, semanticResult, symbol_table, index):
    # make sure that the current token is a valid arithmetic operator
    if lexeme[index][0] not in operators[:7]:  # Arithmetic operators
        semanticResult += f"semantic error at line {line + 1}: Invalid operator '{lexeme[index][0]}'\n"
        return semanticResult, None

    index += 1  
    operands = []  # ? operand collector ? to check types and initialization

    for i in range(2):  # two operands is expected
        if index >= len(lexeme) or lexeme[index][0] == 'AN':
            semanticResult += f"semantic error at line {line + 1}: Incomplete arithmetic expression\n"
            return semanticResult, None

        if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
            var_name = lexeme[index][0]

            if lexeme[index][1] == 'Identifier':
                # check if the variable is declared
                if var_name not in symbol_table:
                    semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return semanticResult, index
                # check if the variable is initialized
                if not symbol_table[var_name].get("initialized", False):
                    semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not initialized\n"
                    return semanticResult, index
                # add the type of the variable to operands
                operands.append(symbol_table[var_name]["type"])
            else:
                # if it's a literal; determine the type
                literal_type = "NUMBR" if lexeme[index][1] == "Integer" else "NUMBAR" if lexeme[index][1] == "Float" else None
                operands.append(literal_type)

            index += 1
        elif lexeme[index][0] in operators:  # nested arithmetic operation
            semanticResult, index = sem_arithmetic(lexeme, line, semanticResult, symbol_table, index)
        else:
            semanticResult += f"semantic error at line {line + 1}: Invalid operand '{lexeme[index][0]}'\n"
            return semanticResult, index

        # check for 'AN' keyword between operands
        if i == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
            index += 1

    # check type compatibility of operands
    if len(operands) == 2:
        if operands[0] != operands[1]:
            semanticResult += f"semantic error at line {line + 1}: Type mismatch in arithmetic expression ({operands[0]} and {operands[1]})\n"
            return semanticResult, None

    return semanticResult, index

#def sem_smoosh?

