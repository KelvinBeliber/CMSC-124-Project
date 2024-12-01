from syntax_funcs.statement import statement

def conditional(lexeme, line, syntaxResult, symbol_table, index=0):
    if lexeme[index][0] != "O RLY?":
        syntaxResult += f"syntax error at line {line + 1}: Expected 'O RLY?' to start conditional block\n"
        return syntaxResult, index + 1

    index += 1  # Move past 'O RLY?'

    # Check for YA RLY block
    if index >= len(lexeme) or lexeme[index][0] != "YA RLY":
        syntaxResult += f"syntax error at line {line + 1}: Missing 'YA RLY' block in conditional statement\n"
        return syntaxResult, index

    index += 1  # Move past 'YA RLY'

    # Validate YA RLY block
    while index < len(lexeme):
        if lexeme[index][0] == "NO WAI":
            break  # Checks NO WAI, exits YA RLY
        elif lexeme[index][0] == "OIC":
            syntaxResult += f"syntax error at line {line + 1}: Unexpected 'OIC' without 'NO WAI'\n"
            return syntaxResult, index

        # YA RLY
        if lexeme[index][0] == "O RLY?":
            syntaxResult = conditional(lexeme, line, syntaxResult, symbol_table)
        else:
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)

    # Check for NO WAI block
    if index < len(lexeme) and lexeme[index][0] == "NO WAI":
        index += 1  # Move past 'NO WAI'

        # NO WAI block validator
        while index < len(lexeme):
            if lexeme[index][0] == "OIC":
                break  # Exit NO WAI block

            
            if lexeme[index][0] == "O RLY?":# nested conditional
                syntaxResult = conditional(lexeme, line, syntaxResult, symbol_table)
            else:# NO WAI validator
                syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)

    # Check for OIC to end the conditional block
    if index >= len(lexeme) or lexeme[index][0] != "OIC":
        syntaxResult += f"syntax error at line {line + 1}: Missing 'OIC' to close conditional block\n"
        return syntaxResult, index

    index += 1  # Move past 'OIC'

    return syntaxResult, index
