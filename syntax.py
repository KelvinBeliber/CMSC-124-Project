import lexical
import os

def comment(lexeme, obtw, tldr):
    index = next((i for i, sublist in enumerate(lexeme) if 'Comment line' in sublist), -1)
    if index != -1:
        lexeme.pop(lexeme.index(index))
    # print(f'{lexeme}\n') <-- debugging
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

def vardec(text, start, i, declared_vars, syntaxResult, obtw, tldr):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    ihasa = 0
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if lexeme is not None:
            if lexeme[0][0] == 'I HAS A':
                var_name = lexeme[1][0]
                if var_name in declared_vars:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
                    continue
                if len(lexeme) == 2:
                    declared_vars.append(var_name)
                    continue
                if lexeme[2][0] != 'ITZ':
                    syntaxResult += f"syntax error at line {line + 1}: Missing ITZ for variable '{lexeme[1][0]}' initialization\n"
                    continue
            else:
                if ['BUHBYE', 'Variable Declaration Delimiter'] in lexeme:
                    return line, declared_vars, syntaxResult
                syntaxResult += f"syntax error at line {line + 1}: Incorrect variable declaration syntax\n"
                continue

    return line, declared_vars, syntaxResult

# def check_arith_bool_syntax(lexeme, line, syntaxResult, operation_type):
#     if len(lexeme) < 3:
#         syntaxResult += f"syntax error at line {line + 1}: Incomplete {operation_type} operation\n"
#         return syntaxResult

#     if operation_type == "arithmetic":
#         if lexeme[1][1] not in ['Identifier', 'Literal'] or lexeme[2][0] != 'AN':
#             syntaxResult += f"syntax error at line {line + 1}: Invalid arithmetic operation syntax\n"
    
#     elif operation_type == "boolean":
#         if lexeme[1][1] not in ['Identifier', 'Literal']:
#             syntaxResult += f"syntax error at line {line + 1}: Invalid first operand in boolean operation, must be Identifier or Literal\n"
#         if lexeme[2][0] != 'AN':
#             syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' in boolean operation\n"
#         if len(lexeme) < 4 or lexeme[3][1] not in ['Identifier', 'Literal']:
#             syntaxResult += f"syntax error at line {line + 1}: Invalid second operand in boolean operation, must be Identifier or Literal\n"
#         elif lexeme[3][0] in ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']:
#             syntaxResult += f"syntax error at line {line + 1}: Invalid second operand in boolean operation, cannot be another operator\n"

#     return syntaxResult

def casting(lexeme, line, syntaxResult):
    if lexeme[1][0] == 'R':
        if lexeme[2][1] not in ['Identifier', 'Literal']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid assignment value\n"
        return syntaxResult

    if lexeme[1][0] == 'MAEK' or lexeme[1][0] == 'IS':
        if len(lexeme) < 5 or lexeme[2][0] != 'A':
            syntaxResult += f"syntax error at line {line + 1}: Missing 'A' or incorrect type\n"
        if lexeme[3][0] not in ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid type for casting\n"
    return syntaxResult

def syntax(text):
    hai = -1
    kthxbye = -1
    wazzup = -1
    buhbye = -1
    obtw = -1
    tldr = -1
    declared_vars = []
    syntaxResult = ''
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    arithmetic_ops = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    boolean_ops = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']
    for line in range(0, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if lexeme is not None:
            # Skip 'BTW' comment lexemes and 'OBTW' 'TLDR' multi line lexemes
            if comment(lexeme, obtw, tldr)==True:
                continue
            
            # checking code proper
            for i in range(0,len(lexeme)):
                # check for hai keyword
                if lexeme[i][0] != 'HAI' and hai!=1:
                    return f'syntax error at line 0: HAI is not declared'
                if  hai == -1 and kthxbye == -1:
                    hai = 1
                # check for declaration keyword
                if lexeme[i][0] == 'WAZZAP' or lexeme[i][0] == 'BUHBYE' and wazzup == 0 and buhbye == 0:
                    syntaxResult += f"syntax error at line {line+1}: WAZZUP-BUHBYE block has already been declared\n"
                    break
                if lexeme[i][0] == 'WAZZUP':
                    if wazzup != -1:
                        syntaxResult += f"syntax error at line {line+1}: WAZZUP has already been declared\n"
                        break
                    if buhbye != -1:
                        syntaxResult += f"syntax error at line {line+1}: WAZZUP cannot be declared after BUHBYE\n"
                        break
                    if wazzup == -1 and buhbye == -1:
                        vardecResult = vardec(text, line+1, 0, declared_vars, syntaxResult, obtw, tldr)
                        line = vardecResult[0]
                        declared_vars = vardecResult[1]
                        syntaxResult = vardecResult[2]
                        wazzup = 1
                        continue
                if lexeme[i][0] == 'BUHBYE':
                    if wazzup != 1:
                        syntaxResult += f"syntax error at line {line+1}: BUHBYE declared without a WAZZUP\n"
                        break
                    elif buhbye != -1:
                        syntaxResult += f"syntax error at line {line+1}: BUHBYE has already been declared\n"
                        break
                    else:
                        wazzup = 0
                        buhbye = 0
                        continue
                # printing output
                if lexeme[i][0] == 'VISIBLE':
                    while(i<len(lexeme)):
                        i+=1
                        if lexeme[i][1] not in literals or lexeme[i][1] != 'Identifier':
                            syntaxResult += f"syntax error at line {line+1}: Incorrect VISIBLE syntax!\n"
                            break
                    if i>=len(lexeme):
                        break
                # taking input
                if lexeme[i][0] == 'GIMMEH':
                    if lexeme[i+1][1] != 'Identifier':
                        syntaxResult += f"syntax error at line {line+1}: Incorrect GIMMEH syntax!\n"
                        break
                    continue
                # check for arithmetic and boolean operations
                # if lexeme[i][0] in arithmetic_ops:
                #     syntaxResult = check_arith_bool_syntax(lexeme[i:], line, syntaxResult, "arithmetic")
                # elif lexeme[i][0] in boolean_ops:
                #     syntaxResult = check_arith_bool_syntax(lexeme[i:], line, syntaxResult, "boolean")
                if lexeme[i][0] in ['R', 'MAEK', 'IS']:
                    syntaxResult = casting(lexeme[i:], line, syntaxResult)
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
