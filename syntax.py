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
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]
    
    def is_valid_variable_declaration(lexeme):
        """Helper function to check if it's a valid variable declaration."""
        return lexeme[0][0] == 'I HAS A'

    def handle_variable_assignment(lexeme, line, symbol_table, syntaxResult):
        """Handle variable initialization or assignment."""
        var_name = lexeme[1][0]
        if var_name in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
            return syntaxResult
        
        # Check if the value being assigned is a valid literal or identifier
        if lexeme[3][1] not in literals and lexeme[3][1] != 'Identifier' and lexeme[3][0] not in operators: 
            syntaxResult += f"syntax error at line {line + 1}: Invalid initialization for variable '{var_name}'\n"
            return syntaxResult
        
        # Validate identifier on right side
        if lexeme[3][0] in operators:
            temp = syntaxResult
            syntaxResult, _ = operator(lexeme[3:], line, syntaxResult, symbol_table, 0)
            if(len(temp)<len(syntaxResult)):
                return syntaxResult
        elif lexeme[3][1] == 'Identifier' and lexeme[3][0] not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Undefined variable '{lexeme[3][0]}' on right side of ITZ\n"
            return syntaxResult
        symbol_table.append(var_name)  # Add to symbol table with variable and its value
        return syntaxResult

    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        if comment(lexeme, obtw, tldr):
            continue
        
        if lexeme is not None:
            if is_valid_variable_declaration(lexeme):
                if len(lexeme) == 2:
                    # Declare variable without initialization (ITZ part is optional)
                    symbol_table.append(lexeme[1][0])
                elif len(lexeme) >= 4 and lexeme[2][0] == 'ITZ':
                    # Handle initialization with ITZ
                    syntaxResult = handle_variable_assignment(lexeme, line, symbol_table, syntaxResult)
                else:
                    syntaxResult += f"syntax error at line {line + 1}: Missing 'ITZ' in variable declaration\n"
            else:
                if ['BUHBYE', 'Variable Declaration Delimiter'] in lexeme:
                    return line, symbol_table, syntaxResult
                syntaxResult += f"syntax error at line {line + 1}: Incorrect variable declaration syntax\n"
    
    return line, symbol_table, syntaxResult




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
    
    # Check if the left-hand side is a valid identifier (variable)
    if lexeme[0][1] != 'Identifier':
        syntaxResult += f"syntax error at line {line + 1}: Invalid variable '{lexeme[0][0]}'!\n"
        return syntaxResult
    
    var_name = lexeme[0][0]  # Left-hand side variable name
    
    # Ensure that the variable is already declared in symbol_table
    if var_name not in symbol_table:
        syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared!\n"
        return syntaxResult
    
    # Check for the 'R' keyword, ensuring it's in the correct position
    if lexeme[1][0] != 'R':
        syntaxResult += f"syntax error at line {line + 1}: Invalid declaration, missing 'R'!\n"
        return syntaxResult
    
    # Handle type casting if the third token is 'MAEK' or 'IS NOW A'
    if ['MAEK', 'Typecasting Operation'] == lexeme[2] or ['IS NOW A', 'Typecasting Operation'] == lexeme[2]:
        syntaxResult = casting(lexeme[2:], line, symbol_table, syntaxResult)
        return syntaxResult

    # Handle the right-hand side expression, it can be a literal, an identifier, or an operator expression
    if lexeme[2][1] in literals:
        # If the right-hand side is a literal (e.g., '5', 'TRUE', etc.)
        return syntaxResult  # No further processing needed, literal assignment is valid
    elif lexeme[2][1] == 'Identifier':
        # If the right-hand side is a variable (check if it's declared)
        rhs_var = lexeme[2][0]
        if rhs_var not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Variable '{rhs_var}' not declared on the right-hand side!\n"
            return syntaxResult
        return syntaxResult
    else:
        # If the right-hand side is an operator expression (e.g., SUM OF, DIFF OF)
        # Use the operator function to process the expression
        syntaxResult, _ = operator(lexeme, line, syntaxResult, symbol_table, 2)
    return syntaxResult
    
def expression(lexeme, line, syntaxResult, symbol_table): # <operator> | <literal>
    literals = ['NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal']
    #check if the first element is a valid literal
    if lexeme[0][1] in literals:
        return syntaxResult
    else:
        return operator(lexeme, line, syntaxResult, symbol_table, 0)

def operator(lexeme, line, syntaxResult, symbol_table, index=0):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]

    def comparison(lexeme, line, syntaxResult, symbol_table, index):
        # Check for BOTH SAEM keyword
        if lexeme[index][0] not in operators[13:15]:
            syntaxResult += f"syntax error at line {line + 1}: Expected boolean identifier\n"
            return syntaxResult, index + 1


        index += 1  # Move to the first operand
        if index >= len(lexeme):
            syntaxResult += f"syntax error at line {line + 1}: Missing first operand in comparison\n"
            return syntaxResult, index
        
        # First operand
        
        operand1 = lexeme[index][0]
        is_var1 = lexeme[index][1] == 'Identifier'
        if is_var1:
            if operand1 not in symbol_table:
                syntaxResult += f"syntax error at line {line + 1}: Variable '{operand1}' not declared\n"
                return syntaxResult, index
        elif lexeme[index][1] in operators:
            temp = syntaxResult
            syntaxResult, index = operator(lexeme[index:], line, syntaxResult, symbol_table, index)
            if(len(temp)<len(syntaxResult)):
                return syntaxResult, index
        index += 1
        
        # Check for 'AN'
        if index >= len(lexeme) or lexeme[index][0] != 'AN':
            syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' after first operand\n"
            return syntaxResult, index

        # Check for BIGGR OF or SMALLR OF (3rd operand only allowed with these)
        index += 1
        if index >= len(lexeme): 
            syntaxResult += f"syntax error at line {line + 1}: Missing second operand in comparison\n"
            return syntaxResult, index

        if lexeme[index][0] in ['BIGGR OF', 'SMALLR OF']:
            second_operator = lexeme[index][0]
            index += 1  # Move to the operands of BIGGR OF / SMALLR OF

        operand2 = lexeme[index][0]
        print(operand1,operand2)
        is_var2 = lexeme[index][1] == 'Identifier'
        if is_var2:
            if operand2 not in symbol_table:
                syntaxResult += f"syntax error at line {line + 1}: Variable '{operand2}' not declared\n"
                return syntaxResult, index
        elif lexeme[index][1] in operators:
            temp = syntaxResult
            syntaxResult, index = operator(lexeme[index:], line, syntaxResult, symbol_table, index)
            if(len(temp)<len(syntaxResult)):
                return syntaxResult, index

        index += 1
        # If no further operands, finish here (valid 2-operand comparison)
        if index >= len(lexeme) or lexeme[index][0] != 'AN' or not second_operator:
            return syntaxResult, index

        # Validate first two operands are the same variable/value
        if operand1 != operand2:
            syntaxResult += f"syntax error at line {line + 1}: First two operands must match to use '{second_operator}'\n"
            return syntaxResult, index

        # third operand of BIGGR OF / SMALLR OF
        if index >= len(lexeme):
            syntaxResult += f"syntax error at line {line + 1}: Missing first operand for '{second_operator}'\n"
            return syntaxResult, index
        if lexeme[index][1] == 'Identifier' and lexeme[index][0] not in symbol_table:
            syntaxResult += f"syntax error at line {line + 1}: Variable '{lexeme[index][0]}' not declared\n"
            return syntaxResult, index
        return syntaxResult, index

    def bool(lexeme, line, syntaxResult, symbol_table, index):
        # Simplified Arithmetic Implementation
        if lexeme[index][0] not in operators[7:13]:  # Check for arithmetic operators
            syntaxResult += f"syntax error at line {line + 1}: Invalid boolean operator '{lexeme[index][0]}'\n"
            return syntaxResult, index + 1

        index += 1  # Move to first operand
        for i in range(2):  # Two operands expected
            if index >= len(lexeme) or lexeme[index][0] == 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Incomplete boolean expression\n"
                return syntaxResult, index

            if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return syntaxResult, index
                index += 1
            elif lexeme[index][0] in operators:  # Nested operator
                syntaxResult, index = operator(lexeme, line, syntaxResult, symbol_table, index)
            else:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in boolean expression\n"
                return syntaxResult, index

            # Check for 'AN' keyword between operands
            if i == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
                index += 1
        return syntaxResult, index

    def arithmetic(lexeme, line, syntaxResult, symbol_table, index):
        # Simplified Arithmetic Implementation
        if lexeme[index][0] not in operators[:7]:  # Check for arithmetic operators
            syntaxResult += f"syntax error at line {line + 1}: Invalid arithmetic operator '{lexeme[index][0]}'\n"
            return syntaxResult, index + 1

        index += 1  # Move to first operand
        for i in range(2):  # Two operands expected
            if index >= len(lexeme) or lexeme[index][0] == 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Incomplete arithmetic expression\n"
                return syntaxResult, index

            if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return syntaxResult, index
                index += 1
            elif lexeme[index][0] in operators:  # Nested operator
                syntaxResult, index = operator(lexeme, line, syntaxResult, symbol_table, index)
            else:
                syntaxResult += f"syntax error at line {line + 1}: Invalid operand in arithmetic expression\n"
                return syntaxResult, index

            # Check for 'AN' keyword between operands
            if i == 0 and index < len(lexeme) and lexeme[index][0] == 'AN':
                index += 1
        return syntaxResult, index

    def smoosh(lexeme, line, syntaxResult, symbol_table, index):
        # Simplified SMOOSH Implementation
        if lexeme[index][0] != 'SMOOSH':
            syntaxResult += f"syntax error at line {line + 1}: Expected 'SMOOSH'\n"
            return syntaxResult, index + 1

        index += 1
        while index < len(lexeme):
            if lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':
                var_name = lexeme[index][0]
                if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                    syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                    return syntaxResult, index
                index += 1
            elif lexeme[index][0] in operators:  # Nested operator
                syntaxResult, index = operator(lexeme, line, syntaxResult, symbol_table, index)
            else:
                syntaxResult += f"syntax error at line {line + 1}: Invalid argument in SMOOSH expression\n"
                return syntaxResult, index

            # Check for 'AN' keyword after each argument except the last
            if index < len(lexeme) and lexeme[index][0] == 'AN':
                index += 1
            elif index < len(lexeme):
                syntaxResult += f"syntax error at line {line + 1}: Missing 'AN' in SMOOSH arguments\n"
                return syntaxResult, index

        return syntaxResult, index

    # Determine which operator function to call
    if lexeme[index][0] in ['SMOOSH']:
        return smoosh(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[:7]:  # Arithmetic operators
        return arithmetic(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[7:13]:  # Boolean operators
        return bool(lexeme, line, syntaxResult, symbol_table, index)
    elif lexeme[index][0] in operators[13:15]:  # comparison operators
        return comparison(lexeme, line, syntaxResult, symbol_table, index)
    else:
        syntaxResult += f"syntax error at line {line + 1}: Unknown operator '{lexeme[index][0]}'\n"
        return syntaxResult, index + 1

def visible(lexeme, line, syntaxResult, symbol_table):
    literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]

    def is_valid_expression(lexeme, index, syntaxResult):
        """Helper function to validate an arithmetic or logical expression."""
        if lexeme[index][0] in operators:  # Check for nested expressions
            syntaxResult, end_index = operator(lexeme, line, syntaxResult, symbol_table, index)
            return True, syntaxResult, end_index
        elif lexeme[index][1] in literals or lexeme[index][1] == 'Identifier':  # Check for literals or identifiers
            var_name = lexeme[index][0]
            if lexeme[index][1] == 'Identifier' and var_name not in symbol_table:
                syntaxResult += f"syntax error at line {line + 1}: Variable '{var_name}' not declared\n"
                return False, syntaxResult, index
            return True, syntaxResult, index + 1  # Move to next index
        else:
            return False, syntaxResult, index

    index = 0
    while index < len(lexeme):
        # Validate operand
        is_valid, syntaxResult, next_index = is_valid_expression(lexeme, index, syntaxResult)
        if not is_valid:
            syntaxResult += f"syntax error at line {line + 1}: Invalid operand in VISIBLE expression\n"
            break
        index = next_index

        # Check if there's an 'AN' keyword after each operand except the last
        if index < len(lexeme):
            if lexeme[index][0] != 'AN':
                syntaxResult += f"syntax error at line {line + 1}: Missing or incorrect 'AN' keyword in VISIBLE arguments\n"
                break
            index += 1  # Move past 'AN'

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
