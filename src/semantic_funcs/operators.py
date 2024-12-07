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
    for i in range(2):  # Two operands expected
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=2
            continue
        if lexeme[index][1] in ('NUMBR Literal', 'NUMBAR Literal') :  # Handle numeric literals
            operands.append(int(lexeme[index][0]))
            index+=2
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = arithmetic(lexeme, line, symbol_table, index,errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type", None, index
    # Perform the operation
    result = evaluate_operator(operator, operands[0], operands[1])
    return errors, result, index