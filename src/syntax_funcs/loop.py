import lexical
from syntax_funcs.statement import statement
from syntax_funcs.comment import obtw_comment
from syntax_funcs.comment import btw_comment
from syntax_funcs.operators import operator
from semantic_funcs.loop import evaluate_loop

def loop(text, start, errors, symbol_table, function_table):
    iminyr = False
    in_loop = False
    loop_label = None
    loop_variable = None
    loop_operation = None
    condition_type = None  # TIL or WILE
    condition_expression = None
    multi_comment = False
    lines_processed = 0
    code = ''
    temp = errors

    def is_valid_iminyr(lexeme):
        return lexeme[0][0] == "IM IN YR"

    def is_til(lexeme):
        return lexeme[5][0] == "TIL"

    def is_wile(lexeme):
        return lexeme[5][0] == "WILE"

    def is_outta(lexeme):
        return lexeme[0][0] == "IM OUTTA YR"

    for line in range(start, len(text.splitlines())):
        lines_processed+=1
        lexeme = lexical.lex(text.splitlines()[line].strip())
        # Comment skipping
        lexeme = btw_comment(lexeme)
        if len(lexeme) == 0:
            continue
        if lexeme[0] == ['OBTW', 'Comment Delimiter'] or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            multi_comment = obtw_comment(errors, lexeme, line, len(text.splitlines()), multi_comment)
            if type(multi_comment) == str:
                errors += multi_comment
                break
        if multi_comment or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            continue

        # Loop start
        if not iminyr:
            if is_valid_iminyr(lexeme):
                iminyr = True
                if len(lexeme) < 2 or lexeme[1][1] != "Identifier":
                    errors += f"syntax error at line {line + 1}: Missing or invalid loop label\n"
                    return errors, None, None
                loop_label = lexeme[1][0]
            else:
                errors += f"syntax error at line {line + 1}: Expected 'IM IN YR' to start loop block\n"
                return errors, None, None

        # Loop operation
        if not loop_operation:
            if lexeme[2][1] == "Loop Operation" and len(lexeme) > 2 and lexeme[3][0] == "YR":
                loop_operation = lexeme[2][0]  # UPPIN or NERFIN
                loop_variable = lexeme[4][0]
                if loop_variable not in symbol_table:
                    errors += f"syntax error at line {line + 1}: Undefined variable '{loop_variable}'\n"
                    return errors, None, None
                in_loop = True
            else:
                errors += f"syntax error at line {line + 1}: Expected loop operation (e.g., 'UPPIN YR' or 'NERFIN YR')\n"
                return errors, None, None

        # Loop condition
        if in_loop and not condition_type:
            if is_til(lexeme) or is_wile(lexeme):
                condition_type = lexeme[5][0]
                errors, index = operator(lexeme[6:], line, errors, symbol_table, 0)
                if len(temp)<len(errors):
                    return errors, None, None
                loop_condition = lexeme[6:]
                continue
            else:
                errors += f"syntax error at line {line + 1}: Expected 'TIL' or 'WILE' condition\n"
                return errors, None, None
            
        if is_outta(lexeme):
            if len(lexeme) < 2 or lexeme[1][0] != loop_label:
                errors += f"syntax error at line {line + 1}: Mismatched or missing loop label after 'IM OUTTA YR'\n"
                return errors, None
            errors, result = evaluate_loop(code, symbol_table, function_table, errors, loop_condition, loop_operation, loop_variable, condition_type)
            if len(temp)==len(errors):
                return errors, lines_processed, result
            return errors, None, None
        
        # Loop body and end
        if in_loop:
            # Parse statements inside the loop
            errors, _ = statement(lexeme, line, errors, symbol_table, function_table, True)
            if len(temp)<len(errors):
                return errors, None, None
            code += text.splitlines()[line].strip() + "\n"
    if in_loop:
        errors += "syntax error: Reached end of file without closing loop\n"
    return errors, None, None
