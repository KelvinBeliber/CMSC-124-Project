def btw_comment(lexeme):
    index = next((i for i, sublist in enumerate(lexeme) if 'Comment Line' in sublist), -1)
    if index != -1:
        lexeme.pop(index)
    return lexeme

def obtw_comment(errors, lexeme, line, code_length, multi_comment):
    if lexeme[0] == ['OBTW', 'Comment Delimiter']:
        if line == code_length-1:
            errors += f'syntax error at {line+1}: Multi Comment line never enclosed\n'
            return errors
        return True
    else:
        if len(lexeme) > 1:
            errors += f'syntax error at {line+1}: Cannot place code right after declaring TLDR on the same line\n'
            return errors
        if multi_comment == False:
            errors += f'syntax error at {line+1}: OBTW was never declared\n'
            return errors
        return False