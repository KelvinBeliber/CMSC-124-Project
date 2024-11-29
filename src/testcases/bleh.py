import lexical
import os

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

def vardec(text, start, i, symbol_table, syntaxResult, obtw, tldr):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal'] ## for saving values
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if comment(lexeme, obtw, tldr)==True:
            continue
        if lexeme is not None:
            if lexeme[0][0] == 'I HAS A':
                var_name = lexeme[1][0]
                if var_name in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
                    continue
                if len(lexeme) == 2:
                    symbol_table.append(var_name)
                    continue
                if lexeme[2][0] != 'ITZ':
                    syntaxResult += f"syntax error at line {line + 1}: Missing ITZ for variable '{lexeme[1][0]}' initialization\n"
                    continue
                else:
                    if lexeme[3][1] not in ['NOOB Literal', 'NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal']:
                        syntaxResult += f"syntax error at line {line + 1}: Missing Type for ITZ '{lexeme[1][0]}' initialization\n"
                        continue
            else:
                if ['BUHBYE', 'Variable Declaration Delimiter'] in lexeme:
                    return line, symbol_table, syntaxResult
                syntaxResult += f"syntax error at line {line + 1}: Incorrect variable declaration syntax\n"
                continue

    return line, symbol_table, syntaxResult

def check_operator_syntax(lexeme, line, syntaxResult, operation_type):
    if len(lexeme) < 3:
        syntaxResult += f"syntax error at line {line + 1}: Incomplete {operation_type} operation\n"
        return syntaxResult

    if operation_type == "arithmetic":
        if lexeme[1][1] not in ['Identifier', 'Literal'] or lexeme[2][0] != 'AN':
            syntaxResult += f"syntax error at line {line + 1}: Invalid arithmetic operation syntax\n"
    
    elif operation_type == "boolean":
        if lexeme[1][1] not in ['Identifier', 'Literal']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid first operand in boolean operation, must be Identifier or Literal\n"
        if lexeme[2][0] != 'AN':
            syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' in boolean operation\n"
        if len(lexeme) < 4 or lexeme[3][1] not in ['Identifier', 'Literal']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid second operand in boolean operation, must be Identifier or Literal\n"
        elif lexeme[3][0] in ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']:
            syntaxResult += f"syntax error at line {line + 1}: Invalid second operand in boolean operation, cannot be another operator\n"
    return syntaxResult

def casting(lexeme, line, symbol_table, syntaxResult):
    type = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    if lexeme[0][0] == 'MAEK':
        if lexeme[1][1] != 'Identifier':
            syntaxResult += f"syntax error at line {line + 1}: No variable to typecast!\n"
        if lexeme[1][0] not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Variable was not declared!\n"
        if lexeme[2][0] not in type:
            syntaxResult += f"syntax error at line {line + 1}: Invalid type for casting\n"
    elif lexeme[1][0] == 'IS NOW A':
        if lexeme[2][0] not in type:
            syntaxResult += f"syntax error at line {line + 1}: Invalid type for casting\n"
    # put code to recast (semantics)
    return syntaxResult

def assignment(lexeme, symbol_table, line, syntaxResult):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    if lexeme[0][1] != 'Identifier':
        syntaxResult += f"syntax error at line {line+1}: Invalid variable!\n"
        return syntaxResult
    var_name = lexeme[0][0]
    if var_name not in symbol_table:
        syntaxResult += f"syntax error at line {line+1}: Variable was not declared!\n"
        return syntaxResult
    if lexeme[1][0] != 'R':
        syntaxResult += f"syntax error at line {line+1}: Invalid declaration, missing 'R'!\n"
        return syntaxResult
    if ['MAEK', 'Typecasting Operation'] == lexeme[2] or ['IS NOW A', 'Typecasting Operation'] == lexeme[2]:
        syntaxResult = casting(lexeme[2:], line, symbol_table, syntaxResult)
        return syntaxResult
    if lexeme[2][1] not in literals:
        syntaxResult += f"syntax error at line {line+1}: Value cannot be assigned to variable!\n"
        return syntaxResult
    return syntaxResult


def value(lexeme, line, syntaxResult): # varident | <literal> | <expression>
    valid_literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    
    #check if lexeme is a VARIDENT 
    if lexeme[0][1] == 'Identifier':

        return syntaxResult  # valid varident (variable identifier)
    
    #check if lexeme is a LITERAL
    elif lexeme[1][1] in valid_literals:
        return syntaxResult  # valid literal
    
    # #check if it's an EXPRESSION
    # #wala pa to lalagyan pa implementation
    
    else:
        syntaxResult += f"syntax error at line {line + 1}: Invalid value syntax\n"
        return syntaxResult
    
def expression(lexeme, line, syntaxResult, symbol_table): # <operator> | <literal>
    literals = ['NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal']
    #check if the first element is a valid literal
    if lexeme[0][1] in literals:
        return syntaxResult
    else:
        return operator(lexeme, line, syntaxResult, symbol_table)

def operator(lexeme, line, syntaxResult, symbol_table): # <arithmetic> | <boolean> | <comparison> | <concatenation> | <casting>
    expResult = [syntaxResult,0]
    for i in range(0, len(lexeme)):
        # placeholder for arithmetic operators
        if lexeme[0][0] in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
            expResult = arithmetic(lexeme, line, syntaxResult, symbol_table)  # future logic for arithmetic operators (left as placeholder)
        
    #     # placeholder for boolean operators
    #     elif lexeme[1][0] in ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']:
    #         return syntaxResult  # future logic for boolean operators (left as placeholder)

    #     # placeholder for comparison operators
    #     elif lexeme[0][0] in ['BOTH SAEM', 'DIFFRINT']:
    #         return syntaxResult  # future logic for comparison operators (left as placeholder)

    #     # placeholder for concatenation operators
    #     elif lexeme[1][0] in ['SMOOSH']:
    #         syntaxResult # future logic for concatenation operators (left as placeholder)
    #         break
        
    #     # no operator match
        # else:
        #     if i==len(lexeme)+1:
        #         syntaxResult += f"syntax error at line {line + 1}: Invalid syntax\n"
        #         break
    return expResult

def arithmetic(lexeme, line, syntaxResult, symbol_table):
    index = 0
    literals = ['NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
        ]
    print(lexeme)
    if len(lexeme) < 4:  # Minimum length for valid arithmetic operation
        syntaxResult += f"syntax error at line {line + 1}: Incomplete arithmetic operation\n"

    valid_operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']
    if lexeme[0][0] not in valid_operators:
        syntaxResult += f"syntax error at line {line + 1}: Invalid arithmetic operator '{lexeme[0][0]}'\n"
    
    if lexeme[1][1] in operators:
        temp = len(syntaxResult)
        expResult = operator(lexeme[1:], line, syntaxResult, symbol_table)
        syntaxResult = expResult[0]
        index += expResult[1]
        if(temp<len(syntaxResult)):
            syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic operation, must be Identifier, Literal or an expression\n"

    if lexeme[1][1] not in ['Identifier'] or lexeme[1][1] not in literals:
        syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic operation, must be Identifier, Literal or an expression\n"


    if lexeme[2][0] != 'AN':
        syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' keyword in arithmetic operation\n"

    if lexeme[3][1] in operators:
        temp = len(syntaxResult)
        expResult = operator(lexeme[3:], line, syntaxResult, symbol_table)
        syntaxResult = expResult[0]
        index += expResult[1]
        if(temp<len(syntaxResult)):
            syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic operation, must be Identifier, Literal or an expression\n"

    if lexeme[3][1] not in ['Identifier', literals]:
        temp = len(syntaxResult)
        expResult = operator(lexeme[3:], line, syntaxResult, symbol_table)
        syntaxResult = expResult[0]
        index += expResult[1]
        if(temp<len(syntaxResult)):
            syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic operation, must be Identifier, Literal or an expression\n"
    index += 4

    return syntaxResult,index

def comparison(lexeme, line, syntaxResult, symbol_table):
    type = ['NOOB', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
    if lexeme[0][1] == 'Identifier':
        syntaxResult += f"syntax error at line {line + 1}: Invalid operator syntax\n"
    else:
        syntaxResult = expression(lexeme, line, syntaxResult, symbol_table)
    # put code to recast (semantics)
    return syntaxResult

def boolean(lexeme, line, syntaxResult): 
    valid_boolean_ops = ['BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF']

    if lexeme[0][0] == 'NOT':
        # NOT operation requires a single operand
        if len(lexeme) < 2: 
            if lexeme[1][1] not in ['Identifier', 'Literal']:
                syntaxResult += f"syntax error at line {line + 1}: NOT operation requires a valid operand\n"
            else:
                expression(lexeme, line, syntaxResult)
        return syntaxResult

    if lexeme[0][0] not in valid_boolean_ops:
        syntaxResult += f"syntax error at line {line + 1}: Invalid boolean operator '{lexeme[0][0]}'\n"
        return syntaxResult

    if len(lexeme) < 4:
        syntaxResult += f"syntax error at line {line + 1}: Incomplete boolean operation\n"
        return syntaxResult

    if lexeme[1][1] not in ['Identifier', 'Literal']:
        syntaxResult += f"syntax error at line {line + 1}: Invalid first operand in boolean operation, must be Identifier or Literal\n"

    if lexeme[2][0] != 'AN':
        syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' keyword in boolean operation\n"

    if len(lexeme) < 4 or lexeme[3][1] not in ['Identifier', 'Literal']:
        syntaxResult += f"syntax error at line {line + 1}: Invalid second operand in boolean operation, must be Identifier or Literal\n"

    return syntaxResult

def visible(lexeme, line, syntaxResult, symbol_table):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
        ]


    skip = 0
    for i in range(0,len(lexeme)):
        # if skip>0:
        #     skip-=1
        #     continue
        if (i+1)%2 == 1:
            if lexeme[i][1] in literals:
                continue
            if lexeme[i][1] in 'Identifier':
                
                var_name = lexeme[i][0]
                if var_name in symbol_table:
                    continue
                syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                break
            if lexeme[i][0] in operators:
                temp = len(syntaxResult)
                expResult = expression(lexeme[i:], line, syntaxResult, symbol_table)
                syntaxResult = expResult[0]
                if(temp<len(syntaxResult)):
                    syntaxResult += f"syntax error at line {line+1}: Incorrect VISIBLE syntax!\n"
                    break
                skip = expResult[1]
        else:
            # print(f'{line+1}:{i+1}:{lexeme[i]} <--- else block\n')
            if lexeme[i][0] != 'AN':
                syntaxResult += f"syntax error at line {line+1}: Incorrect concatenation of VISIBLE arguments!\n"
                break
    return syntaxResult

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
            # checking code proper
            for i in range(0,len(lexeme)):
                # check for hai keyword
                if skip>0:
                    skip-=1
                    break
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
                        vardecResult = vardec(text, line+1, 0, symbol_table, syntaxResult, obtw, tldr)
                        skip = vardecResult[0]-line
                        symbol_table = vardecResult[1]
                        syntaxResult = vardecResult[2]
                        wazzup = 1
                        break
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
                        break
                ## ----------------------------- <statement> tree -----------------------------
                # printing output
                if lexeme[i][0] == 'VISIBLE':
                    syntaxResult = visible(lexeme[i+1:], line, syntaxResult, symbol_table)
                    break
                # taking input
                if lexeme[i][0] == 'GIMMEH':
                    if len(lexeme) > 2 or len(lexeme) <= 1:
                        syntaxResult += f"syntax error at line {line+1}: Incorrect GIMMEH syntax!\n"
                        break
                    if lexeme[i+1][1] != 'Identifier':
                        syntaxResult += f"syntax error at line {line+1}: Incorrect GIMMEH syntax!\n"
                        break
                if len(lexeme[i:])>=i+3: ## i+3 the smallest assignment and expression statements can be
                    ## assignment
                    if ['R', 'Variable Assignment'] == lexeme[i+1]:
                        syntaxResult = assignment(lexeme[i:], symbol_table, line, syntaxResult)
                    ## check for casting 
                    elif ['MAEK', 'Typecasting Operation'] == lexeme[i] or ['IS NOW A', 'Typecasting Operation'] == lexeme[i+1]:
                        syntaxResult = casting(lexeme[i:], line, symbol_table, syntaxResult)
                    ## expression
                    else:
                        syntaxResult = expression(lexeme, line, syntaxResult, symbol_table)
                    break

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
