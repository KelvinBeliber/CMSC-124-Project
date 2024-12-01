from syntax_funcs.statement import expression
from syntax_funcs.statement import statement

def loop(lexeme, line, syntaxResult, symbol_table, index=0):
    if lexeme[index][0] != "IM IN YR":
        syntaxResult += f"syntax error at line {line + 1}: Expected 'IM IN YR' to start a loop block\n"
        return syntaxResult, index + 1

    index += 1  # Move past 'IM IN YR'

    # checks identifiers
    if index >= len(lexeme) or lexeme[index][1] != "Identifier":
        syntaxResult += f"syntax error at line {line + 1}: Loop name expected after 'IM IN YR'\n"
        return syntaxResult, index + 1

    loop_name = lexeme[index][0]
    index += 1  

    # checks if there is a til or wile
    condition_type = None
    if index < len(lexeme) and lexeme[index][0] in ["TIL", "WILE"]:
        condition_type = lexeme[index][0]  # Store the condition type
        index += 1  # Move past TIL or WILE

        # make sure there is a valid expression
        if index >= len(lexeme):
            syntaxResult += f"syntax error at line {line + 1}: Missing condition expression after '{condition_type}'\n"
            return syntaxResult, index

        # validate
        syntaxResult = expression(lexeme, line, syntaxResult, symbol_table)

    # reads loop
    while index < len(lexeme):
        if lexeme[index][0] == "IM OUTTA YR":
            index += 1  # Move past 'IM OUTTA YR'

            # matches loop name
            if index >= len(lexeme) or lexeme[index][0] != loop_name:
                syntaxResult += f"syntax error at line {line + 1}: Loop name mismatch or missing after 'IM OUTTA YR'\n"
                return syntaxResult, index + 1

            index += 1  # Move past loop name
            return syntaxResult, index

        # validator
        if lexeme[index][0] == "IM IN YR":
            syntaxResult += f"Line {line + 1}: Nested loop detected\n"
            syntaxResult = loop(lexeme, line, syntaxResult, symbol_table)
        else:
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)

    syntaxResult += f"syntax error at line {line + 1}: Missing 'IM OUTTA YR {loop_name}' to close loop block\n"
    return syntaxResult, index