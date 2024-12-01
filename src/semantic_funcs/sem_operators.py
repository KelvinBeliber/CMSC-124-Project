# pacheck if okay lang ba yung redundant checks or not
# padagdag if may kulang
# wala pa ung sa valid expressions (idk yet)

def sem_operator(lexeme, line, semanticResult, symbol_table, index=0):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

    def sem_boolean(lexeme, line, semanticResult, symbol_table, index=0):
        def is_valid_operand(lexeme, index, semanticResult):
        # check if the operand is valid for boolean expressions
            if lexeme[index][1] not in ['TROOF Literal', 'Identifier']:
                semanticResult += f"semantic error at line {line + 1}: Invalid operand '{lexeme[index][0]}' in boolean expression\n"
                return False
            # if it's an identifier, check if it's declared already or not
            if lexeme[index][1] == 'Identifier' and lexeme[index][0] not in symbol_table:
                semanticResult += f"semantic error at line {line + 1}: Variable '{lexeme[index][0]}' not declared\n"
                return False
            return True

        def validate_boolean_expression(lexeme, line, semanticResult, symbol_table, index):
            #checks the boolean operator expressions if valid.
            bool_type = lexeme[index][0] 
            index += 1  

            # this will handle boolean operators that require multiple operands (ALL OF, ANY OF)
            if bool_type in ['ALL OF', 'ANY OF']:
                has_operands = False
                while index < len(lexeme):
                    # check for the terminating MKAY
                    if lexeme[index][0] == 'MKAY':
                        if not has_operands:
                            semanticResult += f"semantic error at line {line + 1}: {bool_type} requires at least one operand\n"
                        return semanticResult, index + 1  # Move past MKAY

                    # checkeach operand
                    if not is_valid_operand(lexeme, index, semanticResult):
                        return semanticResult, index
                    has_operands = True
                    index += 1

                    # check if the 'AN' keyword is between operands
                    if index < len(lexeme) and lexeme[index][0] == 'AN':
                        index += 1  # Move past 'AN'
                    elif index < len(lexeme) and lexeme[index][0] != 'MKAY':
                        semanticResult += f"semantic error at line {line + 1}: Missing or incorrect 'AN' keyword in {bool_type} expression\n"
                        return semanticResult, index

                # If loop ends without finding MKAY
                semanticResult += f"semantic error at line {line + 1}: Missing 'MKAY' to terminate {bool_type} expression\n"
                return semanticResult, index

            # Handle unary NOT operator
            elif bool_type == 'NOT':
                # Validate the operand for NOT operator
                if index >= len(lexeme) or not is_valid_operand(lexeme, index, semanticResult):
                    semanticResult += f"semantic error at line {line + 1}: Invalid operand in NOT expression\n"
                    return semanticResult, index
                index += 1

            # handle binary boolean operators -> (BOTH OF, EITHER OF, WON OF)
            elif bool_type in ['BOTH OF', 'EITHER OF', 'WON OF']:
                # we expect two operands for binary operators
                for _ in range(2):
                    if index >= len(lexeme) or not is_valid_operand(lexeme, index, semanticResult):
                        semanticResult += f"semantic error at line {line + 1}: Invalid operand in {bool_type} expression\n"
                        return semanticResult, index
                    index += 1

                    # checks for AN keyword between operands
                    if index < len(lexeme) and lexeme[index][0] == 'AN':
                        index += 1
                    elif index < len(lexeme) and lexeme[index][0] != 'MKAY':
                        semanticResult += f"semantic error at line {line + 1}: Missing 'AN' keyword in {bool_type} expression\n"
                        return semanticResult, index

            else:
                semanticResult += f"semantic error at line {line + 1}: Invalid boolean operator '{bool_type}'\n"
                return semanticResult, index

            return semanticResult, index

        # make sure that it's a valid boolean expression
        if lexeme[index][0] in operators:
            return validate_boolean_expression(lexeme, line, semanticResult, symbol_table, index)
        else:
            semanticResult += f"semantic error at line {line + 1}: Unknown operator '{lexeme[index][0]}'\n"
            return semanticResult, index
    
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
    
    def semantic_comparison(lexeme, line, semanticResult, symbol_table, index):
        # check if the token is a valid comparison operator
        if lexeme[index][0] not in ['BOTH SAEM', 'DIFFRINT']:
            semanticResult += f"semantic error at line {line + 1}: Expected comparison operator, got '{lexeme[index][0]}'\n"
            return semanticResult, None

        comparison_type = lexeme[index][0]  # save the comparison type
        index += 1  #moving to the 1st operand

        operand_types = []  #collects operand types for type compatibility check

        def validate_operand(lexeme, line, semanticResult, symbol_table, index): #validates operand and returns what type it is

            if lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if var_name not in symbol_table:
                    semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return semanticResult, index, None
                if not symbol_table[var_name].get("initialized", False):
                    semanticResult += f"semantic error at line {line + 1}: Variable '{var_name}' not initialized\n"
                    return semanticResult, index, None
                operand_type = symbol_table[var_name]["type"]
            elif lexeme[index][1] in literals:
                operand_type = "NUMBR" if lexeme[index][1] == "Integer" else "NUMBAR" if lexeme[index][1] == "Float" else None
            else:
                semanticResult += f"semantic error at line {line + 1}: Invalid operand '{lexeme[index][0]}'\n"
                return semanticResult, index, None

            return semanticResult, index + 1, operand_type

        # check the first operand
        semanticResult, index, operand_type = validate_operand(lexeme, line, semanticResult, symbol_table, index)
        if not operand_type:
            semanticResult += f"semantic error at line {line + 1}: Invalid first operand in {comparison_type} expression\n"
            return semanticResult, None
        operand_types.append(operand_type)

        # Check for 'AN' keyword
        if index >= len(lexeme) or lexeme[index][0] != 'AN':
            semanticResult += f"semantic error at line {line + 1}: Missing 'AN' after first operand\n"
            return semanticResult, None
        index += 1  # Move past 'AN'

        # check the second operand
        if index >= len(lexeme):
            semanticResult += f"semantic error at line {line + 1}: Missing second operand in comparison\n"
            return semanticResult, None

        if lexeme[index][0] in ['BIGGR OF', 'SMALLR OF']:
            # handles nested arithmetic expression
            nested_operator = lexeme[index][0]
            index += 1  # Move to the first operand of BIGGR OF / SMALLR OF

            # check both operands of BIGGR OF / SMALLR OF
            for _ in range(2): # no need for loop variable so just put _ we'll check n times
                if index >= len(lexeme):
                    semanticResult += f"semantic error at line {line + 1}: Missing operand for '{nested_operator}'\n"
                    return semanticResult, None

                semanticResult, index, operand_type = validate_operand(lexeme, line, semanticResult, symbol_table, index)
                if not operand_type:
                    semanticResult += f"semantic error at line {line + 1}: Invalid operand in '{nested_operator}'\n"
                    return semanticResult, None

                # check for 'AN' between operands
                if _ == 0 and (index >= len(lexeme) or lexeme[index][0] != 'AN'):
                    semanticResult += f"semantic error at line {line + 1}: Missing 'AN' in '{nested_operator}'\n"
                    return semanticResult, None
                if _ == 0:
                    index += 1  # Move past 'AN'

        else:
            # validate second operand directly (non-nested case)
            semanticResult, index, operand_type = validate_operand(lexeme, line, semanticResult, symbol_table, index)
            if not operand_type:
                semanticResult += f"semantic error at line {line + 1}: Invalid second operand in {comparison_type} expression\n"
                return semanticResult, None
            operand_types.append(operand_type)

        # check if type is compatible
        if len(operand_types) == 2 and operand_types[0] != operand_types[1]:
            semanticResult += f"semantic error at line {line + 1}: Type mismatch in {comparison_type} expression ({operand_types[0]} and {operand_types[1]})\n"
            return semanticResult, None

        return semanticResult, index
    
# need pa ng function calls dito