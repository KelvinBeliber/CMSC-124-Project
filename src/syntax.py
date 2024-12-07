import lexical
import os

from syntax_funcs.comment import btw_comment
from syntax_funcs.comment import obtw_comment
from syntax_funcs.wazzupblock import vardec
from syntax_funcs.statement import statement
from syntax_funcs.func import func_def
from syntax_funcs.switch import wtf_switch
from syntax_funcs.loop import loop
from syntax_funcs.ifelse import conditional

def syntax(text):
    hai = -1
    kthxbye = -1
    wazzup = -1
    buhbye = -1
    multi_comment = False
    symbol_table = {'IT':None}
    function_table = {}
    errors = ''
    skip = 0
    types = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    arithmetic_ops = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_ops = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']
    for line in range(0, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if lexeme is not None:
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
            if skip>0:
                skip-=1
                continue
            # checking code proper
            # check for hai keyword
            if lexeme[0][0] != 'HAI' and hai!=1:
                return f'syntax error at line 0: HAI is not declared'
            if  hai == -1 and kthxbye == -1:
                hai = 1
                continue
            if lexeme[0][0] == 'KTHXBYE':
                if hai != 1:
                    return f"syntax error at line {line+1}: KTHXBYE declared without a HAI\n"
                else:
                    if len(lexeme) > 1:
                        return f"syntax error at line {line+1}: Incorrect KTHXBYE syntax\n"
                    break
            # check for declaration keyword
            if (lexeme[0][0] == 'WAZZUP' or lexeme[0][0] == 'BUHBYE') and wazzup == 0 and buhbye == 0:
                return f"syntax error at line {line+1}: WAZZUP-BUHBYE block has already been declared\n"
            if lexeme[0][0] == 'WAZZUP':
                if wazzup != -1:
                    return f"syntax error at line {line+1}: WAZZUP has already been declared\n"
                if buhbye != -1:
                    return f"syntax error at line {line+1}: WAZZUP cannot be declared after BUHBYE\n"
                if wazzup == -1 and buhbye == -1:
                    if len(lexeme) > 1:
                        return f"syntax error at line {line+1}: Incorrect WAZZUP syntax\n"
                    errors, symbol_table, skip = vardec(text, line+1, symbol_table, errors)
                    if not skip and not symbol_table:
                        return errors
                    skip -= line
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
            if line==len(text.splitlines())-1:
                return f"syntax error at line {line+1}: Missing KTHXBYE at the end of the code\n"
            ## ----------------------------- statement tree -----------------------------
            if lexeme[0][0] == 'HOW IZ I':
                errors, skip = func_def(text, line, errors, function_table)
                if not skip:
                    break
                skip -= line
                continue
            if lexeme[0][0] == 'WTF?' and possible_switch:
                errors, skip = wtf_switch(text, line, errors, symbol_table, function_table)
                if not skip:
                    break
                skip -= line
                continue
            if lexeme[0][0] == 'IM IN YR':
                errors, skip = loop(text, line, errors, symbol_table, function_table)
                if not skip:
                    break
                skip -= line
                continue
            if lexeme[0][0] == 'O RLY?':
                errors, skip = conditional(text, line, errors, symbol_table, function_table)
                if not skip:
                    break
                skip -= line
                continue
            if lexeme[0][1]=='Identifier' and len(lexeme)==1:
                possible_switch = True
                continue
            temp = errors
            errors = statement(lexeme, line, errors, symbol_table, function_table)
            if len(temp) < len(errors):
                break
    # debugging: tracking symbols and defined functions
    for key in symbol_table:
        print(f'{key}: {symbol_table[key]}')
    for key in function_table:
        print(f'{key}: {function_table[key]}')
    if len(errors)==0:
        return "syntax correct"
    return errors

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
