literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

def arithmetic(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate_operator(operator, operand1, operand2):
        if operator == 'SUM OF':
            return operand1 + operand2
        elif operator == 'DIFF OF':
            return operand1 - operand2
        elif operator == 'PRODUKT OF':
            return operand1 * operand2
        elif operator == 'QUOSHUNT OF':
            return operand1 / operand2 if operand2 != 0 else float('inf')  # Avoid division by zero
        elif operator == 'MOD OF':
            return operand1 % operand2
        elif operator == 'BIGGR OF':
            return max(operand1, operand2)
        elif operator == 'SMALLR OF':
            return min(operand1, operand2)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    operator = lexeme[index][0]
    index += 1  # Move to first operand
    # Collect operands
    operands = []
    for i in range(3):  # Two operands expected
        if lexeme[index][0] == 'AN':  # skip AN
            index+=1
            continue
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            if(type(symbol_table[var_name]) not in (int, float)):
                return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", None, index
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in ('NUMBR Literal', 'NUMBAR Literal') :  # Handle numeric literals
            operands.append(int(lexeme[index][0]))
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = arithmetic(lexeme, line, symbol_table, index,errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", None, index
    # Perform the operation
    result = evaluate_operator(operator, operands[0], operands[1])
    return errors, result, index

def comparison(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate_comparison(operator, operand1, operand2):
        if operator == 'DIFFRINT':
            return operand1 != operand2
        elif operator == 'DIFFRINTBIGGR OF':
            return operand1 > operand2
        elif operator == 'DIFFRINTSMALLR OF':
            return operand1 < operand2
        elif operator == 'BOTH SAEM':
            return operand1 == operand2
        elif operator == 'BOTH SAEMBIGGR OF':
            return operand1 >= operand2
        elif operator == 'BOTH SAEMSMALLR OF':
            return operand1 <= operand2
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    operator = lexeme[index][0]
    index += 1  # Move to first operand
    # Collect operands
    operands = []
    for i in range(3):  # Two operands expected
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in literals :  # Handle literals
            operands.append(
                int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                True if (lexeme[index][0] == 'WIN') else
                False if (lexeme[index][0] == 'FAIL') else
                lexeme[index][0]
            )
            print(lexeme[index][0], line+1)
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index,errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        if lexeme[index][0] == 'AN':  # Handle nested operators
            index+=1
            if lexeme[index][0] in ('BIGGR OF', 'SMALLR OF'):
                operator += lexeme[index][0]
                index+=1
                if lexeme[index][1] == 'Identifier':  # Handle variables
                    var_name = lexeme[index][0]
                    operands.append(symbol_table[var_name])  # Fetch variable value
                    index+=2
                    continue
                if lexeme[index][1] in literals :  # Handle literals
                    operands.append(
                        int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                        float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                        lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                        True if (lexeme[index][0] == 'WIN') else
                        False if (lexeme[index][0] == 'FAIL') else
                        lexeme[index][0]
                    )
                    index+=2
                    continue
                if lexeme[index][0] in operators:  # Handle nested operators
                    errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index,errors)
                    if errors:
                        return errors, None, index
                    operands.append(nested_result)
                    print(operands)
                    index+1
                    continue
                continue
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for comparison", None, index
    # Perform the operation
    if len(operands)==3:
        if operands[0] != operands[1]:
            return errors+f"semantic error at {line+1}: BIGGR OF and SMALLR OF syntax requires 1st operand and 2nd operand to match", None, index
        del operands[1]
    if (type(operands[0]) not in (float, int) or type(operands[1]) not in (float,int)) and operator in ("DIFFRINTBIGGR OF","DIFFRINTSMALLR OF","BOTH SAEMBIGGR OF","BOTH SAEMSMALLR OF"):
        return errors+f"semantic error at {line+1}: invalid operand type for comparison", None, index
    result = evaluate_comparison(operator, operands[0], operands[1])
    return errors, result, index


def boolean(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate_operator(operator, operands):
        if operator == 'BOTH OF':
            return operands[0] and operands[1]
        elif operator == 'EITHER OF':
            return operands[0] or operands[1]
        elif operator == 'WON OF':
            return operands[0] ^ operands[1]
        elif operator == 'NOT':
            return not operands[0]
        elif operator == 'ALL OF':
            for i in len(operands):
                if operands[i]:
                    continue
                return False
            return True
        elif operator == 'ANY OF':
            for i in len(operands):
                if not operands[i]:
                    continue
                return True
            return False
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    operator = lexeme[index][0]
    index += 1  # Move to first operand
    # Collect operands
    operands = []
    for i in range(3):  # Two operands expected
        if lexeme[index][0] == 'AN':  # skip AN
            index+=1
            continue
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            if(type(symbol_table[var_name]) not in (int, float)):
                return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", None, index
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in ('NUMBR Literal', 'NUMBAR Literal') :  # Handle numeric literals
            operands.append(int(lexeme[index][0]))
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = arithmetic(lexeme, line, symbol_table, index,errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", None, index
    # Perform the operation
    result = evaluate_operator(operator, operands[0], operands[1])
    return errors, result, index

def evaluate_operator(lexeme, line, symbol_table, index, errors):
    operator = lexeme[index][0]

    # Determine which operator function to call
    # if operator in ['SMOOSH']:
    #     return smoosh(lexeme, line, symbol_table, index, errors)
    if operator in operators[:7]:  # Arithmetic operators
        return arithmetic(lexeme, line, symbol_table, index, errors)
    # elif operator in operators[7:13]:  # Boolean operators
    #     return boolean(lexeme, line, symbol_table, index, errors)
    elif operator in operators[13:15]:  # Comparison operators
        return comparison(lexeme, line, symbol_table, index, errors)
    else:
        errors += f"syntax error at line {line + 1}: Unknown operator '{operator}'\n"
        return errors, None, index
