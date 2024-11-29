import lexical
from syntax_funcs.comment import comment
from syntax_funcs.operators import operator

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