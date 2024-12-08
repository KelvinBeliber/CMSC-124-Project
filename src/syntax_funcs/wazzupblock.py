import lexical
from syntax_funcs.comment import btw_comment
from syntax_funcs.comment import obtw_comment
from syntax_funcs.operators import operator
from semantic_funcs.operators import evaluate_operator

def vardec(text, start, symbol_table, errors):
    literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
    operators = [
        'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH'
    ]
    comment_line_count = 0
    multi_comment = False
    
    def is_valid_variable_declaration(lexeme):
        """Helper function to check if it's a valid variable declaration."""
        return lexeme[0][0] == 'I HAS A'

    def handle_variable_assignment(lexeme, line, symbol_table, errors):
        """Handle variable initialization or assignment."""
        var_name = lexeme[1][0]
        if var_name in symbol_table:
            errors += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
            return errors
        
        # Check if the value being assigned is a valid literal or identifier
        if lexeme[3][1] not in literals and lexeme[3][1] != 'Identifier' and lexeme[3][0] not in operators:
            errors += f"syntax error at line {line + 1}: Invalid initialization for variable '{var_name}'\n"
            return errors
        
        # Validate identifier on right side
        if lexeme[3][0] in operators:
            temp = errors
            errors, _ = operator(lexeme[3:], line, errors, symbol_table, 0)
            if(len(temp)<len(errors)):
                return errors
            temp = errors
            errors, symbol_table[var_name],_ = evaluate_operator(lexeme[3:], line, symbol_table, 0, errors) #arithmetic(lexeme[3:], line, symbol_table, 0, errors)
            if len(temp)<len(errors):
                return errors
            return errors
        elif lexeme[3][1] == 'Identifier':
            if lexeme[3][0] not in symbol_table:
                errors += f"syntax error at line {line + 1}: Undefined variable '{lexeme[3][0]}' on right side of ITZ\n"
                return errors
        symbol_table[var_name] = (
            int(lexeme[3][0]) if (lexeme[3][1] == 'NUMBR Literal') else 
            float(lexeme[3][0]) if (lexeme[3][1] == 'NUMBAR Literal') else
            lexeme[3][0] if (lexeme[3][1] == 'YARN Literal') else
            lexeme[3][0]
            )  # Add to symbol table with variable and its value (for both variable and literal value cases)
        return errors

    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
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
            comment_line_count+=1
            continue
        
        if lexeme is not None:
            if is_valid_variable_declaration(lexeme):
                if len(lexeme) == 2:
                    # Declare variable without initialization (ITZ part is optional)
                    var_name = lexeme[1][0]
                    if var_name in symbol_table:
                        errors += f"syntax error at line {line + 1}: Variable '{var_name}' already declared\n"
                        return errors, None, None
                        
                    symbol_table[var_name] = "NOOB"
                elif len(lexeme) >= 4 and lexeme[2][0] == 'ITZ':
                    # Handle initialization with ITZ
                    temp = errors
                    errors = handle_variable_assignment(lexeme, line, symbol_table, errors)
                    if len(temp)!=len(errors):
                        return errors, None, None
                else:
                    errors += f"syntax error at line {line + 1}: Missing 'ITZ' in variable declaration\n"
                    return errors, None, None
            else:
                if ['BUHBYE', 'Variable Declaration Delimiter'] in lexeme:
                    return errors, symbol_table, line-comment_line_count
                errors += f"syntax error at line {line + 1}: Incorrect variable declaration syntax\n"
                return errors, None, None
    errors += f"syntax error at line {line + 1}: 'BUHBYE' keyword never called\n"
    return errors, None, None