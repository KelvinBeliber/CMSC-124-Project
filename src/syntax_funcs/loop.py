import lexical
from syntax_funcs.statement import statement
from syntax_funcs.comment import obtw_comment
from syntax_funcs.comment import btw_comment
from syntax_funcs.operators import operator

def loop(text, start, syntaxResult, symbol_table, function_table):
    iminyr = False
    in_loop = False
    loop_label = None
    loop_variable = None
    loop_operation = None
    condition_type = None  # TIL or WILE
    condition_expression = None
    multi_comment = False
    comment_line_count = 0

    def is_valid_iminyr(lexeme):
        return lexeme[0][0] == "IM IN YR"

    def is_til(lexeme):
        return lexeme[5][0] == "TIL"

    def is_wile(lexeme):
        return lexeme[5][0] == "WILE"

    def is_outta(lexeme):
        return lexeme[0][0] == "IM OUTTA YR"

    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        # Comment skipping
        lexeme = btw_comment(lexeme)
        if len(lexeme) == 0:
            continue
        if lexeme[0] == ['OBTW', 'Comment Delimiter'] or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            multi_comment = obtw_comment(syntaxResult, lexeme, line, len(text.splitlines()), multi_comment)
            if type(multi_comment) == str:
                syntaxResult += multi_comment
                break
        if multi_comment or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            comment_line_count += 1
            continue

        # Loop start
        if not iminyr:
            if is_valid_iminyr(lexeme):
                iminyr = True
                if len(lexeme) < 2 or lexeme[1][1] != "Identifier":
                    syntaxResult += f"syntax error at line {line + 1}: Missing or invalid loop label\n"
                    return syntaxResult, None
                loop_label = lexeme[1][0]
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'IM IN YR' to start loop block\n"
                return syntaxResult, None

        # Loop operation
        if not loop_operation:
            if lexeme[2][1] == "Loop Operation" and len(lexeme) > 2 and lexeme[3][0] == "YR":
                loop_operation = lexeme[2][0]  # UPPIN or NERFIN
                loop_variable = lexeme[4][0]
                if loop_variable not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Undefined variable '{loop_variable}'\n"
                    return syntaxResult, None
                in_loop = True
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected loop operation (e.g., 'UPPIN YR' or 'NERFIN YR')\n"
                return syntaxResult, None

        # Loop condition
        if in_loop and not condition_type:
            if is_til(lexeme) or is_wile(lexeme):
                condition_type = lexeme[5][0]
                try:
                    condition_expression = operator(lexeme, line, syntaxResult, symbol_table, 0)
                except Exception as e:
                    syntaxResult += f"syntax error at line {line + 1}: Invalid condition expression ({e})\n"
                    return syntaxResult, None
                continue
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'TIL' or 'WILE' condition\n"
                return syntaxResult, None

        # Loop body and end
        if in_loop:
            if is_outta(lexeme):
                if len(lexeme) < 2 or lexeme[1][0] != loop_label:
                    syntaxResult += f"syntax error at line {line + 1}: Mismatched or missing loop label after 'IM OUTTA YR'\n"
                    return syntaxResult, None
                return syntaxResult, line  # Successfully parsed loop block
            # Parse statements inside the loop
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table, function_table)
            if syntaxResult is not None:
                line = line + 1  # Update the line index based on statement parsing

    if in_loop:
        syntaxResult += "syntax error: Reached end of file without closing loop\n"
    return syntaxResult, None
