from syntax_funcs.statement import statement
import lexical
from syntax_funcs.comment import obtw_comment
from syntax_funcs.comment import btw_comment
from semantic_funcs.ifelse import evaluate_ifelse

def conditional(text, start, errors, symbol_table, function_table):
    orly = False
    yarly = False
    nowai = False
    lines_processed = 0
    multi_comment = False
    in_conditional = False
    cases = {}

    def is_valid_orly_start(lexeme):
        return lexeme[0][0] == "O RLY?"
    
    def is_yarly(lexeme):
        return lexeme[0][0] == "YA RLY"
    
    def is_nowai(lexeme):
        return lexeme[0][0] == "NO WAI"
    
    def is_oic(lexeme):
        return lexeme[0][0] == "OIC"
    
    for line in range(start, len(text.splitlines())):
        lines_processed+=1
        lexeme = lexical.lex(text.splitlines()[line].strip())
        ## comment skipping
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

        if not orly:
            if is_valid_orly_start(lexeme):
                orly = True 
                continue
            else:
                errors += f"syntax error at line {line + 1}: Expected 'O RLY?' to start conditional block\n"
                return errors, None, None
            
        if orly and is_valid_orly_start(lexeme):
            errors += f"syntax error at line {line + 1}: Improper redeclaration of O RLY? keyword\n"
            return errors, None, None
            
        if is_yarly(lexeme):
            if orly == False:
                errors += f"syntax error at line {line + 1}: Expected 'YA RLY' after 'O RLY?\n"
                return errors, None, None
            yarly = True
            in_conditional = True
            condition = True
            cases[condition] = ''
            continue

        if is_nowai(lexeme):
            if yarly == False:
                errors += f"syntax error at line {line + 1}: Unexpected 'NO WAI' without 'YA RLY'\n"
                return errors, None, None
            nowai = True
            in_conditional = True
            condition = False
            cases[condition] = ''
            continue

        if is_oic(lexeme):
            if yarly == False:
                errors += f"syntax error at line {line + 1}: 'OIC' without 'YA RLY'\n"
                return errors, None, None
            elif orly == False:
                errors += f"syntax error at line {line + 1}: 'OIC' without 'O RLY?''\n"
                return errors, None, None
            errors, result = evaluate_ifelse(cases, symbol_table, function_table, errors)
            if len(temp)==len(errors):
                return errors, lines_processed, result
            return errors, None, None
        
        if in_conditional:
            temp = errors
            errors,_ = statement(lexeme, line, errors, symbol_table, function_table, True)
            if len(temp) < len(errors):  # Syntax error occurred
                return errors, None, None
            cases[condition] += text.splitlines()[line].strip() + "\n"
            continue

        # Handle invalid lines within the if-else block
        errors += f"syntax error at line {line + 1}: Unexpected syntax in 'O RLY?' block\n"
        return errors, None, None
    
    errors += f"syntax error at line {line + 1}: No OIC to close conditional\n"
    return errors, None, None