import lexical
from syntax_funcs.comment import btw_comment
from syntax_funcs.comment import obtw_comment
from syntax_funcs.statement import statement
from semantic_funcs.switch import evaluate_switch

def wtf_switch(text, start, errors, symbol_table, function_table):
    # Variables to track state
    wtf_start_found = False
    omg = False
    omgwtf = False
    in_case_block = False
    cases = {}
    default_case = None
    lines_processed = 0
    multi_comment = False
    temp = errors

    # Helper function to check if it's the start of a WTF? block
    def is_valid_wtf_start(lexeme):
        return lexeme[0][0] == 'WTF?'

    # Helper function to check if it's an OMG case
    def is_omg_case(lexeme):
        literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
        if len(lexeme)!=2:
            return False
        return lexeme[0][0] == 'OMG' and lexeme[1][1] in literals

    # Helper function to check if it's an OMGWTF case
    def is_omgwtf_case(lexeme):
        return lexeme[0][0] == 'OMGWTF'

    # Helper function to check if it's the GTFO keyword
    def is_gtfo(lexeme):
        return lexeme[0][0] == 'GTFO'

    # Helper function to check if it's the closing OIC
    def is_oic(lexeme):
        return lexeme[0][0] == 'OIC'
    
    choice = symbol_table[lexical.lex(text.splitlines()[start-1].strip())[0][0]]
    
    # Main processing of the WTF? block
    for line in range(start, len(text.splitlines())):
        lines_processed+=1
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
            continue
        # Check for the start of WTF? IT
        if not wtf_start_found:
            if is_valid_wtf_start(lexeme):
                wtf_start_found = True
                continue
            else:
                errors += f"syntax error at line {line + 1}: Expected 'WTF?' to start switch block\n"
                return errors, None
            
        # Check for OMG cases
        if is_omg_case(lexeme):
            if in_case_block:
                errors += f"syntax error at line {line + 1}: 'OMG' cannot appear inside an 'OMG' case\n"
                return errors, None
            elif omgwtf:
                errors += f"syntax error at line {line + 1}: 'OMGWTF' has to be the last case\n"
                return errors, None
            in_case_block = True
            omg = True
            omg_condition = int(lexeme[1][0]) if lexeme[1][1] == 'NUMBR Literal' else float(lexeme[1][0]) if lexeme[1][1] == 'NUMBAR Literal' else lexeme[1][0]
            cases[omg_condition] = ''
            continue

        # Check for OMGWTF case
        if is_omgwtf_case(lexeme):
            if default_case is not None:
                errors += f"syntax error at line {line + 1}: 'OMGWTF' can only appear once\n"
                return errors, None, None
            if in_case_block:
                errors += f"syntax error at line {line + 1}: 'OMGWTF' cannot appear inside an 'OMG' case\n"
                return errors, None, None
            in_case_block = True
            omgwtf = True
            omg_condition = None
            cases[omg_condition] = ''
            continue

        # Check for OIC closure
        if is_oic(lexeme):
            if not wtf_start_found:
                errors += f"syntax error at line {line + 1}: 'OIC' without a 'WTF?' block\n"
                return errors, None, None

            # Check if there is at least one OMG or OMGWTF case before ending
            if not omg and not omgwtf:
                errors += f"syntax error at line {line + 1}: 'WTF?' block must contain at least one 'OMG' or 'OMGWTF' case\n"
                return errors, None, None
            errors, result = evaluate_switch(choice, cases, symbol_table, function_table, errors)
            if len(temp)==len(errors):
                return errors, lines_processed, result
            return errors, None, None
        
        if is_gtfo(lexeme):
            if not in_case_block:
                errors += f"syntax error at line {line + 1}: Expected an 'OMG' or 'OMGWTF' before declaring 'GTFO'\n"
                return errors, None, None
            in_case_block = False
            continue
        
        if in_case_block:
            temp = errors
            errors,_ = statement(lexeme, line, errors, symbol_table, function_table, True)
            if len(temp) < len(errors):  # Syntax error occurred
                return errors, None, None
            cases[omg_condition] += text.splitlines()[line].strip() + "\n"
            continue


        # Handle invalid lines within the switch-case block
        errors += f"syntax error at line {line + 1}: Unexpected syntax in 'WTF?' block\n"
        return errors, None, None

    # If we exit the loop without finding OIC
    errors += f"syntax error: 'OIC' not found to close 'WTF?' block\n"
    return errors, None, None