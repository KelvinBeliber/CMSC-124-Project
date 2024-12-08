literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

def arithmetic(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate(operator, operand1, operand2):
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
            value = symbol_table[var_name]
            if value in ("WIN", "FAIL"):
                value = 1 if value=="WIN" else 0
            elif type(value) == str:
                try:
                    value = int(value)
                except:
                    return errors+f"semantic error at {line+1}: YARN, which contains non-numeric characters, cannot be typecasted to NUMBR", value, None
            elif(type(value) not in (int, float)):
                return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", value, None
            operands.append(value)  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in ('NUMBR Literal', 'NUMBAR Literal') :  # Handle numeric literals
            operands.append(int(lexeme[index][0]) if lexeme[index][1] == 'NUMBR Literal' else float(lexeme[index][0]))
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index, errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for arithmetic operations", None, index
    # Perform the operation
    result = evaluate(operator, operands[0], operands[1])
    return errors, result, index

def comparison(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate_comparison(operator, operand1, operand2):
        if operator == 'DIFFRINT':
            return "WIN" if (operand1 != operand2) else "FAIL"
        elif operator == 'DIFFRINTBIGGR OF':
            return "WIN" if (operand1 > operand2) else "FAIL"
        elif operator == 'DIFFRINTSMALLR OF':
            return "WIN" if (operand1 < operand2) else "FAIL"
        elif operator == 'BOTH SAEM':
            return "WIN" if (operand1 == operand2) else "FAIL"
        elif operator == 'BOTH SAEMBIGGR OF':
            return "WIN" if (operand1 >= operand2) else "FAIL"
        elif operator == 'BOTH SAEMSMALLR OF':
            return "WIN" if (operand1 <= operand2) else "FAIL"
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
                        None if (lexeme[index][0] == 'NOOB') else
                        lexeme[index][0]
                    )
                    index+=2
                    continue
                if lexeme[index][0] in operators:  # Handle nested operators
                    errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index,errors)
                    if errors:
                        return errors, None, index
                    operands.append(nested_result)
                    index+1
                    continue
                continue
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for comparison", None, index
    # Perform the operation
    if len(operands)==3:
        if operands[0] != operands[1]:
            return errors+f"semantic error at {line+1}: BIGGR OF and SMALLR OF syntax requires 1st operand and 2nd operand to match", None, None
        del operands[1]
    if operator in ("DIFFRINTBIGGR OF","DIFFRINTSMALLR OF","BOTH SAEMBIGGR OF","BOTH SAEMSMALLR OF"):
        if type(operands[0]) not in (float, int):
            try:
                operands[0] = int(operands[0])
            except:
                return errors+f"semantic error at {line+1}: YARN, which contains non-numeric characters, cannot be implicitly typecasted to NUMBAR", None, None
        if type(operands[1]) not in (float, int):
            try:
                operands[1] = int(operands[1])
            except:
                return errors+f"semantic error at {line+1}: YARN, which contains non-numeric characters, cannot be implicitly typecasted to NUMBAR", None, None
    print(operands)
    result = evaluate_comparison(operator, operands[0], operands[1])
    return errors, result, index

def boolean(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate(operator, operands):
        if operator == 'BOTH OF':
            return "WIN" if operands[0] and operands[1] else "FAIL"
        elif operator == 'EITHER OF':
            return "WIN" if operands[0] or operands[1] else "FAIL"
        elif operator == 'WON OF':
            return "WIN" if (operands[0] ^ operands[1]) else "FAIL"
        elif operator == 'NOT':
            return "WIN" if not operands else "FAIL"
        elif operator == 'ALL OF':
            for i in range(len(operands)):
                if operands[i]:
                    continue
                return "FAIL"
            return "WIN"
        elif operator == 'ANY OF':
            for i in range(len(operands)):
                if not operands[i]:
                    continue
                return "WIN"
            return "FAIL"
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
    def two_operand(lexeme, line, symbol_table, index, errors):
        # Collect operands
        operands = []
        for i in range(3):  # Two operands expected
            if lexeme[index][0] == 'AN':  # skip AN
                index+=1
                continue
            if lexeme[index][1] == 'Identifier':  # Handle variables
                var_name = lexeme[index][0]
                operands.append(True if symbol_table[var_name]=="WIN" else False if symbol_table in ("FAIL", "NOOB") else symbol_table[var_name])  # Fetch variable value
                index+=1
                continue
            if lexeme[index][1] in literals :  # Handle numeric literals
                operands.append(
                        int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                        float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                        lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                        True if (lexeme[index][0] == 'WIN') else
                        False if (lexeme[index][0] == 'FAIL') else
                        None if (lexeme[index][0] == 'NOOB') else
                        lexeme[index][0]
                    )
                index+=1
                continue
            if lexeme[index][0] in operators:  # Handle nested operators
                errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index,errors)
                if errors:
                    return errors, None, index
                operands.append(True if nested_result=="WIN" else False if nested_result in ("NOOB", "FAIL") else nested_result)
                continue
            return errors+f"semantic error at {line+1}: invalid operand type for {operator} operations", None, index
        # Perform the operation
        result = evaluate(operator, operands)
        return errors, result, index
    
    def one_operand(lexeme, line, symbol_table, index, errors):
        operands = []
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            operands.append(True if symbol_table[var_name]=="WIN" else False if symbol_table in ("FAIL", "NOOB") else symbol_table[var_name])
            index+=1
        elif lexeme[index][1] in literals :  # Handle numeric literals
            operands.append(
                        int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                        float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                        lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                        True if (lexeme[index][0] == 'WIN') else
                        False if (lexeme[index][0] == 'FAIL') else
                        None if (lexeme[index][0] == 'NOOB') else
                        lexeme[index][0]
                    )
            index+=1
        elif lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index,errors)
            if errors:
                return errors, None, index
            operands.append("NOT", True if nested_result=="WIN" else False if nested_result in ("NOOB", "FAIL") else nested_result)
        else:
            raise ValueError(f"Invalid Operand")
        # Perform the operation
        result = evaluate(operator, operands)
        return errors, result, index

    def inf_operand(lexeme, line, symbol_table, index, errors):
        # Collect operands
        operands = []
        while lexeme[index][0]!='MKAY':  # Two operands expected
            if lexeme[index][0] == 'AN':  # skip AN
                index+=1
                continue
            if lexeme[index][1] == 'Identifier':  # Handle variables
                var_name = lexeme[index][0]
                operands.append(symbol_table[var_name])  # Fetch variable value
                index+=1
                continue
            if lexeme[index][1] in literals :  # Handle numeric literals
                operands.append(
                        int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                        float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                        lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                        True if (lexeme[index][0] == 'WIN') else
                        False if (lexeme[index][0] == 'FAIL') else
                        None if (lexeme[index][0] == 'NOOB') else
                        lexeme[index][0]
                    )
                index+=1
                continue
            if lexeme[index][0] in operators:  # Handle nested operators
                errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index, errors)
                if errors:
                    return errors, None, index
                operands.append(nested_result)
                continue
            return errors+f"semantic error at {line+1}: invalid operand type for {operator} operations", None, index
        # Perform the operation
        result = evaluate(operator, operands)
        return errors, result, index

    operator = lexeme[index][0]
    index+=1
    if operator in ("BOTH OF", "EITHER OF", "WON OF"):
        return two_operand(lexeme, line, symbol_table, index, errors)
    elif operator == "NOT":
        return one_operand(lexeme, line, symbol_table, index, errors)
    elif operator in ("ANY OF", "ALL OF"):
        return inf_operand(lexeme, line, symbol_table, index, errors)
    else: 
        raise ValueError(f"Invalid Operand")

def smoosh(lexeme, line, symbol_table, index, errors):
    # Helper function to evaluate an operator
    def evaluate(operands):
        result = str(operands[0])
        for i in range(1,len(operands)):
            result = result + " " + str(operands[i]).replace('"', '')
        return result

    operands = []
    while index!=len(lexeme) and lexeme[index][0]!='MKAY':  # Two operands expected
        if lexeme[index][0] == 'AN':  # skip AN
            index+=1
            continue
        if lexeme[index][1] == 'Identifier':  # Handle variables
            var_name = lexeme[index][0]
            operands.append(symbol_table[var_name])  # Fetch variable value
            index+=1
            continue
        if lexeme[index][1] in literals :  # Handle numeric literals
            operands.append(
                    int(lexeme[index][0]) if (lexeme[index][1] == 'NUMBR Literal') else 
                    float(lexeme[index][0]) if (lexeme[index][1] == 'NUMBAR Literal') else
                    lexeme[index][0] if (lexeme[index][1] == 'YARN Literal') else
                    lexeme[index][0]
                )
            index+=1
            continue
        if lexeme[index][0] in operators:  # Handle nested operators
            errors,nested_result,index = evaluate_operator(lexeme, line, symbol_table, index, errors)
            if errors:
                return errors, None, index
            operands.append(nested_result)
            continue
        return errors+f"semantic error at {line+1}: invalid operand type for SMOOSH operations", None, index
    # Perform the operation
    result = evaluate(operands)
    return errors, result, index

def evaluate_operator(lexeme, line, symbol_table, index, errors):
    operator = lexeme[index][0]
    # Determine which operator function to call
    if operator in ['SMOOSH']:
        return smoosh(lexeme, line, symbol_table, 1, errors)
    if operator in operators[:7]:  # Arithmetic operators
        return arithmetic(lexeme, line, symbol_table, index, errors)
    elif operator in operators[7:13]:  # Boolean operators
        return boolean(lexeme, line, symbol_table, index, errors)
    elif operator in operators[13:15]:  # Comparison operators
        return comparison(lexeme, line, symbol_table, index, errors)
    else:
        raise ValueError(f"syntax error at line {line + 1}: Unknown operator '{lexeme[index][0]}'\n")
