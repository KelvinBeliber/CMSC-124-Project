import lexical
from syntax_funcs.comment import btw_comment
from syntax_funcs.comment import obtw_comment
from syntax_funcs.operators import operator
from syntax_funcs.statement import statement

def wtf_switch(text, start, syntaxResult, symbol_table, function_table):
    # Variables to track state
    wtf_start_found = False
    omg = False
    omgwtf = False
    in_case_block = False
    cases = []
    default_case = None
    comment_line_count = 0
    multi_comment = False

    # Helper function to check if it's the start of a WTF? block
    def is_valid_wtf_start(lexeme):
        return lexeme[0][0] == 'WTF?'

    # Helper function to check if it's an OMG case
    def is_omg_case(lexeme):
        literals = ['Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
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

    # Main processing of the WTF? block
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].strip())
        ## comment skipping
        lexeme = btw_comment(lexeme)
        if len(lexeme) == 0:
            continue
        if lexeme[0] == ['OBTW', 'Comment Delimiter'] or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            multi_comment = obtw_comment(syntaxResult, lexeme, line, len(text.splitlines()), multi_comment)
            if type(multi_comment) == str:
                syntaxResult += multi_comment
                break
        if multi_comment or lexeme[0] == ['TLDR', 'Comment Delimiter']:
            comment_line_count+=1
            continue
        # Check for the start of WTF? IT
        if not wtf_start_found:
            if is_valid_wtf_start(lexeme):
                wtf_start_found = True
                continue
            else:
                syntaxResult += f"syntax error at line {line + 1}: Expected 'WTF?' to start switch block\n"
                return syntaxResult, None
            
        # Check for OMG cases
        if is_omg_case(lexeme):
            if in_case_block:
                syntaxResult += f"syntax error at line {line + 1}: 'OMG' cannot appear inside an 'OMG' case\n"
                return syntaxResult, None
            elif omgwtf:
                syntaxResult += f"syntax error at line {line + 1}: 'OMGWTF' has to be the last case\n"
                return syntaxResult, None
            in_case_block = True
            omg = True
            continue

        # Check for OMGWTF case
        if is_omgwtf_case(lexeme):
            if default_case is not None:
                syntaxResult += f"syntax error at line {line + 1}: 'OMGWTF' can only appear once\n"
                return syntaxResult, None
            if in_case_block:
                syntaxResult += f"syntax error at line {line + 1}: 'OMGWTF' cannot appear inside an 'OMG' case\n"
                return syntaxResult, None
            in_case_block = True
            omgwtf = True
            # Handle the code block within OMGWTF
            # default_case = {'code': []}
            # syntaxResult = statement(lexeme, line, syntaxResult, symbol_table)
            # if syntaxResult.endswith("error"):  # Assuming statement appends "error" on failure
            #     return line, syntaxResult
            continue

        # Check for OIC closure
        if is_oic(lexeme):
            
            if not wtf_start_found:
                syntaxResult += f"syntax error at line {line + 1}: 'OIC' without a 'WTF?' block\n"
                return syntaxResult, None

            # Check if there is at least one OMG or OMGWTF case before ending
            if not omg and not omgwtf:
                syntaxResult += f"syntax error at line {line + 1}: 'WTF?' block must contain at least one 'OMG' or 'OMGWTF' case\n"
                return syntaxResult, None

            return syntaxResult, line-comment_line_count
        
        if is_gtfo(lexeme):
            if not in_case_block:
                syntaxResult += f"syntax error at line {line + 1}: Expected an 'OMG' or 'OMGWTF' before declaring 'GTFO'\n"
                return syntaxResult, None
            in_case_block = False
            continue
        
        if in_case_block:
            temp = syntaxResult
            syntaxResult = statement(lexeme, line, syntaxResult, symbol_table, function_table)
            if len(temp) < len(syntaxResult):  # Syntax error occurred
                return syntaxResult, None
            continue


        # Handle invalid lines within the switch-case block
        syntaxResult += f"syntax error at line {line + 1}: Unexpected syntax in 'WTF?' block\n"
        return syntaxResult, None

    # If we exit the loop without finding OIC
    syntaxResult += f"syntax error: 'OIC' not found to close 'WTF?' block\n"
    return syntaxResult, None
