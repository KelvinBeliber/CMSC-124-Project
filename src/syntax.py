import lexical
import os

from syntax_funcs.comment import comment

from syntax_funcs.wazzupblock import vardec

from syntax_funcs.operators import operator

from syntax_funcs.statement import statement

from syntax_funcs.func import function

from syntax_funcs.switch import wtf_switch

def syntax(text):
    hai = -1
    kthxbye = -1
    wazzup = -1
    buhbye = -1
    obtw = -1
    tldr = -1
    symbol_table = []
    syntaxResult = ''
    skip = 0
    types = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    arithmetic_ops = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_ops = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']
    for line in range(0, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if lexeme is not None:
            # Skip 'BTW' comment lexemes and 'OBTW' 'TLDR' multi line lexemes
            if comment(lexeme, obtw, tldr)==True:
                continue
            if skip>0:
                skip-=1
                continue
            # checking code proper
            # check for hai keyword
            if lexeme[0][0] != 'HAI' and hai!=1:
                return f'syntax error at line 0: HAI is not declared'
            if  hai == -1 and kthxbye == -1:
                hai = 1
            # check for declaration keyword
            if (lexeme[0][0] == 'WAZZUP' or lexeme[0][0] == 'BUHBYE') and wazzup == 0 and buhbye == 0:
                print(lexeme)
                return f"syntax error at line {line+1}: WAZZUP-BUHBYE block has already been declared\n"
            if lexeme[0][0] == 'WAZZUP':
                if wazzup != -1:
                    return f"syntax error at line {line+1}: WAZZUP has already been declared\n"
                if buhbye != -1:
                    return f"syntax error at line {line+1}: WAZZUP cannot be declared after BUHBYE\n"
                if wazzup == -1 and buhbye == -1:
                    if len(lexeme) > 1:
                        return f"syntax error at line {line+1}: Incorrect WAZZUP syntax\n"
                    vardecResult = vardec(text, line+1, 0, symbol_table, syntaxResult, obtw, tldr)
                    skip = vardecResult[0]-line
                    symbol_table = vardecResult[1]
                    syntaxResult = vardecResult[2]
                    wazzup = 1
                    continue
            if lexeme[0][0] == 'BUHBYE':
                if wazzup != 1:
                    return f"syntax error at line {line+1}: BUHBYE declared without a WAZZUP\n"
                elif buhbye != -1:
                    return f"syntax error at line {line+1}: BUHBYE has already been declared\n"
                else:
                    if len(lexeme) > 1:
                        return f"syntax error at line {line+1}: Incorrect BUHBYE syntax\n"
                    wazzup = 0
                    buhbye = 0
                    continue
            ## ----------------------------- statement tree -----------------------------
            if lexeme[0][0] == 'HOW IZ I':
                skip, syntaxResult = function(text, line, syntaxResult, symbol_table, obtw, tldr)
                skip -= line
                continue
            elif lexeme[0][0] == 'WTF?':
                skip, syntaxResult = wtf_switch(text, line, syntaxResult, symbol_table, obtw, tldr)
                continue
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)
    if len(syntaxResult)==0:
        return "syntax correct"
    return syntaxResult

def main():
    filename = input("Enter the name of the .lol file: ")
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return
    with open(filename, 'r') as file:
        text = file.read()
    print(syntax(text))

# Execute main function
if __name__ == "__main__":
    main()
