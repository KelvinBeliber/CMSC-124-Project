
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
        syntaxResult, index = statement(lexeme, line, syntaxResult, symbol_table, index)

    # Check for NO WAI block
    if index < len(lexeme) and lexeme[index][0] == "NO WAI":
        index += 1  # Move past 'NO WAI'

        # NO WAI block validator
        while index < len(lexeme):
            if lexeme[index][0] == "OIC":
                break  # Exit NO WAI block

            # NO WAI validator
            syntaxResult, index = statement(lexeme, line, syntaxResult, symbol_table, index)

    # Check for OIC to end the conditional block
    if index >= len(lexeme) or lexeme[index][0] != "OIC":
        syntaxResult += f"syntax error at line {line + 1}: Missing 'OIC' to close conditional block\n"
        return syntaxResult, index

    index += 1  # Move past 'OIC'

    return syntaxResult, index

def statement(lexeme, line, syntaxResult, symbol_table, index):
    if lexeme[index][0] == "VISIBLE":
        syntaxResult += f"Line {line + 1}: 'VISIBLE' statement recognized\n"
        index += 1
    else:
        syntaxResult += f"syntax error at line {line + 1}: Unrecognized statement '{lexeme[index][0]}'\n"
        index += 1

    return syntaxResult, index