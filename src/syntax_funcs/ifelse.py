from syntax_funcs.statement import statement
import lexical
from syntax_funcs.comment import obtw_comment
from syntax_funcs.comment import btw_comment

def conditional(text, start, syntaxResult, symbol_table, function_table):
    orly = False
    yarly = False
    nowai = False
    comment_line_count = 0
    multi_comment = False
    in_conditional = False

    def is_valid_orly_start(lexeme):
        return lexeme[0][0] == "O RLY?"
    
    def is_yarly(lexeme):
        return lexeme[0][0] == "YA RLY"
    
    def is_nowai(lexeme):
        return lexeme[0][0] == "NO WAI"
    
    def is_oic(lexeme):
        return lexeme[0][0] == "OIC"
    
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        ## comment skipping
        lexeme = btw_comment(lexeme)
        if len(lexeme) == 0:
            continue
        if lexeme[0] == ['OBTW', 'Comment Delimiter'] or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            multi_comment = obtw_comment(syntaxResult, lexeme, line, len(text.splitlines()), multi_comment)
            if type(multi_comment) == str:
                syntaxResult += multi_comment
                break
        if multi_comment or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            comment_line_count+=1
            continue

        if not orly:
            if is_valid_orly_start(lexeme):
                orly = True 
                continue
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'O RLY?' to start conditional block\n"
                return syntaxResult, None
            
        if orly:
            if is_valid_orly_start(lexeme):
                syntaxResult, skip = conditional(text, line, syntaxResult, symbol_table, function_table)
                if skip == None:
                    syntaxResult += f"syntax error at line {line + 1}: Unexpected syntax in nested conditional\n"
                    return syntaxResult, None
                skip -= line
                continue
            
        if is_yarly(lexeme):
            if orly == False:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'YA RLY' after 'O RLY?\n"
                return syntaxResult, None
            yarly = True
            in_conditional = True
            continue

        if is_nowai(lexeme):
            if yarly == False:
                syntaxResult += f"syntax error at line {line + 1}: Unexpected 'NO WAI' without 'YA RLY'\n"
                return syntaxResult, None
            nowai = True
            in_conditional = True
            continue

        if is_oic(lexeme):
            if yarly == False:
                syntaxResult += f"syntax error at line {line + 1}: 'OIC' without 'YA RLY'\n"
                return syntaxResult, None
            elif orly == False:
                syntaxResult += f"syntax error at line {line + 1}: 'OIC' without 'O RLY?''\n"
                return syntaxResult, None
            return syntaxResult, line-comment_line_count
        
        if in_conditional:
            temp = syntaxResult
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table, function_table)
            if len(temp) < len(syntaxResult):  # Syntax error occurred
                return syntaxResult, None
            continue


        # Handle invalid lines within the if-else block
        syntaxResult += f"syntax error at line {line + 1}: Unexpected syntax in 'O RLY?' block\n"
        return syntaxResult, None
    
    syntaxResult += f"syntax error at line {line + 1}: No OIC to close conditional\n"
    return syntaxResult, None

        