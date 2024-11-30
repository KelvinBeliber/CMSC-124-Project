def btw_comment(lexeme):
    index = next((i for i, sublist in enumerate(lexeme) if 'Comment Line' in sublist), -1)
    if index != -1:
        lexeme.pop(index)
    return lexeme

def obtw_comment(syntaxResult, lexeme, line, code_length, multi_comment):
    if lexeme[0] == ['OBTW', 'Comment Delimiter']:
        if line == code_length-1:
            syntaxResult += f'syntax error at {line+1}: Multi Comment line never enclosed\n'
            return syntaxResult
        return True
    else:
        if len(lexeme) > 1:
            syntaxResult += f'syntax error at {line+1}: Cannot place code right after declaring TLDR on the same line\n'
            return syntaxResult
        if multi_comment == False:
            syntaxResult += f'syntax error at {line+1}: OBTW was never declared\n'
            return syntaxResult
        return False