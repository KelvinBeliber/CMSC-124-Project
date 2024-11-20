# Alde, Aeron Deine A.        | 2022-05620
# Beliber, Kelvin James A.    | 2022-06090
# Virtucio, Gabriel Luigi L.  | 2022-06120
# CMSC 124 - S4L
# Milestone 1 - Lexical Analyzer

import re
import os

compiled_lex = []

class LOLLexer:
    def __init__(self, source_code_file):
        self.source_code = source_code_file
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        in_comment = False
        while self.current_position < len(self.source_code):
            token = self.match_token()
            if token is not None:
                if token.type == 'Comment Delimiter' and token.value.strip() == 'OBTW':
                    in_comment = True
                    self.tokens.append(token)
                elif token.type == 'Comment Delimiter' and token.value.strip() == 'TLDR':
                    in_comment = False
                    self.tokens.append(token)
                    continue
                elif in_comment:
                    if token.type == 'Comment Line':
                        self.tokens.append(token)
                else:
                    self.tokens.append(token)
            else:
                break
        return self.tokens

    def match_token(self):
        for pattern, token_type in token_patterns.items():
            match = re.match(pattern, self.source_code[self.current_position:])
            if match:
                value = match.group(0).strip()
                self.current_position += len(match.group(0))
                return Token(token_type, value)
        return None


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

token_patterns = {
    r'\s*HAI\s*': 'Code Delimiter',
    r'\s*KTHXBYE\s*': 'Code Delimiter',
    r'\s*WAZZUP\s*': 'Variable Declaration Delimiter',
    r'\s*BUHBYE\s*': 'Variable Declaration Delimiter',
    r'\s*OBTW\s*': 'Comment Delimiter',
    r'\s*TLDR\s*': 'Comment Delimiter',
    r'^\s*BTW\b.*': 'Comment Line',
    r'\s*I HAS A\s+': 'Variable Declaration',
    r'\s*ITZ\s+': 'Variable Assignment',
    r'\s*R\s+': 'Variable Assignment',
    r'\s*AN\s+': 'Parameter Delimiter',
    r'\s*SUM OF\s+': 'Arithmetic Operation',
    r'\s*DIFF OF\s+': 'Arithmetic Operation',
    r'\s*PRODUKT OF\s+': 'Arithmetic Operation',
    r'\s*QUOSHUNT OF\s+': 'Arithmetic Operation',
    r'\s*MOD OF\s+': 'Arithmetic Operation',
    r'\s*BIGGR OF\s+': 'Arithmetic Operation',
    r'\s*SMALLR OF\s+': 'Arithmetic Operation',
    r'\s*BOTH OF\s+': 'Boolean Operation',
    r'\s*EITHER OF\s+': 'Boolean Operation',
    r'\s*WON OF\s+': 'Boolean Operation',
    r'\s*NOT\s+': 'Boolean Operation',
    r'\s*ANY OF\s+': 'Boolean Operation',
    r'\s*ALL OF\s+': 'Boolean Operation',
    r'\s*BOTH SAEM\s+': 'Comparison Operation',
    r'\s*DIFFRINT\s+': 'Comparison Operation',
    r'\s*SMOOSH\s+': 'String Concatenation',
    r'\s*MAEK\s+': 'Typecasting Operation',
    r'\s*A\s+': 'Typecasting Operation',
    r'\s*IS NOW A\s+': 'Typecasting Operation',
    r'\s*VISIBLE\s+': 'Output Keyword',
    r'\s*\+\s+': 'Output Delimiter',
    r'\s*GIMMEH\s+': 'Input Keyword',
    r'\s*O\sRLY\?\s*': 'If-then Keyword',
    r'\s*YA RLY\s*': 'If-then Keyword',
    r'\s*MEBBE\s+': 'If-then Keyword',
    r'\s*NO WAI\s*': 'If-then Keyword',
    r'\s*OIC\s+': 'If-then Keyword',
    r'\s*WTF\?\s+': 'Switch-Case Keyword',
    r'\s*OMG\s+': 'Switch-Case Keyword',
    r'\s*OMGWTF\s+': 'Switch-Case Keyword',
    r'\s*IM IN YR\s+': 'Loop Keyword',
    r'\s*UPPIN\s+': 'Loop Operation',
    r'\s*NERFIN\s+': 'Loop Operation',
    r'\s*YR\s+': 'Parameter Delimiter',
    r'\s*TIL\s+': 'Loop Keyword',
    r'\s*WILE\s+': 'Loop Keyword',
    r'\s*IM OUTTA YR\s+': 'Loop Keyword',
    r'\s*HOW IZ I\s+': 'Function Keyword',
    r'\s*IF U SAY SO\s+': 'Function Keyword',
    r'\s*GTFO\s+': 'Return Keyword',
    r'\s*FOUND YR\s+': 'Return Keyword',
    r'\s*I IZ\s+': 'Function Call',
    r'\s*MKAY\s+': 'Concatenation Delimiter',
    r'\s*NOOB\s+': 'Void Literal',
    r'\s*(NUMBR|NUMBAR|YARN|TROOF|NOOB)\s?': 'Type Literal',
    r'\s*(WIN|FAIL)\s*': 'TROOF Literal',
    r'\s*[a-zA-Z][a-zA-Z0-9_]*\s*': 'Identifier',
    r'\s*-?(0|[1-9][0-9]*)?\.[0-9]+\s*': 'NUMBAR Literal',
    r'\s*0\s*|^-?[1-9][0-9]*\s*': 'NUMBR Literal',
    r'\s*\"[^\"]*\"\s*': 'YARN Literal',
    r'\s?.*\s?': 'Special Characters'
}

def lex(str):
    compiled_lex.clear()
    lexer = LOLLexer(str)
    tokens = lexer.tokenize()
    for token in tokens:
        if token.type != "YARN Literal":
            compiled_lex.append([token.value.strip(), token.type])
        else:
            compiled_lex.append([token.value, token.type])
    return compiled_lex

# def main():
#     filename = input("Enter the name of the .lol file: ")
#     if not os.path.exists(filename):
#         print(f"Error: The file '{filename}' does not exist.")
#         return
#     tokens = lex(filename)
#     print("Tokenized Output:\n")
#     for token_value, token_type in tokens:
#         print(f"{token_type:>30} : {token_value}")

# if __name__ == "__main__":
#     main()

