def comment(lexeme, obtw, tldr):
    # Remove 'BTW' comment lexemes
    index = next((i for i, sublist in enumerate(lexeme) if 'Comment Line' in sublist), -1)
    if index != -1:
        lexeme.pop(index)
    # Remove 'OBTW' & 'TLDR' multi-line comment lexemes
    if obtw==1:
        if ['TLDR','Comment Delimiter'] not in lexeme:
            return True
        else:                                                           # OBTW and TLDR has been paired
            obtw = 0                                                    
            tldr = 0
            del lexeme[:lexeme.index(['TLDR','Comment Delimiter'])]
    if ['OBTW','Comment Delimiter'] in lexeme:
        obtw = 1                                                        # OBTW exists in the source code
        del lexeme[lexeme.index(['OBTW', 'Comment Delimiter']):]
    if ['TLDR', 'Comment Delimiter'] in lexeme:
        tldr = 1                                                        # TLDR exists in the source code
        del lexeme[:lexeme.index(['TLDR', 'Comment Delimiter'])]
    if len(lexeme)==0:
        return True
    return False