import lexical
from semantic_funcs.statement import evaluate_visible
from semantic_funcs.statement import evaluate_gimmeh
from semantic_funcs.statement import evaluate_function_call
from semantic_funcs.operators import evaluate_operator

literals = ['Void Literal', 'Type Literal', 'TROOF Literal', 'NUMBAR Literal', 'NUMBR Literal', 'YARN Literal']
operators = ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF',
        'BOTH OF', 'EITHER OF', 'WON OF', 'NOT', 'ALL OF', 'ANY OF',
        'BOTH SAEM', 'DIFFRINT',
        'SMOOSH']

def evaluate_ifelse(cases, symbol_table, function_table, errors):
    # Helper function to evaluate an operator
    def evaluate(text, symbol_table, errors):
        visible_output=''
        temp = errors
        for line in range(0, len(text.splitlines())):
            lexeme = lexical.lex(text.splitlines()[line].strip())
            if len(temp)<len(errors):
                return errors, None
            if lexeme[0][0] == 'GIMMEH':
                symbol_table[lexeme[1][0]] = evaluate_gimmeh()
                continue
            if lexeme[0][0] == 'VISIBLE':
                errors, result, _ = evaluate_visible(lexeme, line, symbol_table, 0, errors)
                if len(temp)<len(errors):
                    return errors, None
                if result:
                    visible_output+=result
                continue
            if lexeme[0][0] == 'I IZ':
                errors, result, temp_output = evaluate_function_call(lexeme, line, 0, function_table, symbol_table, errors)
                if len(temp)<len(errors):
                    return errors, None
                symbol_table['IT'] = result
                if temp_output:
                    visible_output+=temp_output
                continue
        return errors, visible_output
    try:
        text = cases[True if symbol_table['IT']=="WIN" else False]
    except:
        try:
            text = cases[bool(symbol_table['IT'])]
        except:
            return errors+f'semantic error: expression value cannot be compared to boolean values', None
    # Perform the operation
    errors, visible_output = evaluate(text, symbol_table, errors)
    return errors, visible_output
