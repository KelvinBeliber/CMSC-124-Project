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

def evaluate_loop(text, symbol_table, function_table, errors, loop_condition, loop_operation, loop_variable, condition_type):
    # Helper function to evaluate an operator
    def evaluate(text, symbol_table, errors):
        visible_output=''
        temp = errors
        alive = True
        while True:
            errors, temp_alive, _ = evaluate_operator(loop_condition, 0, symbol_table, 0, errors)
            alive = True if temp_alive=="WIN" else False if temp_alive in ("FAIL","NOOB") else bool(temp_alive)
            if condition_type=='WILE' and not alive:
                break
            if condition_type=='TIL' and alive:
                break
            for line in range(0, len(text.splitlines())):
                lexeme = lexical.lex(text.splitlines()[line].strip())
                if len(temp)<len(errors):
                    return errors, None
                if lexeme[0][0] == 'GIMMEH':
                    symbol_table[lexeme[1][0]] = evaluate_gimmeh()
                    continue
                if lexeme[0][0] == 'VISIBLE':
                    errors, result, _ = evaluate_visible(lexeme, line, symbol_table, 0, errors)
                    if result:
                        visible_output+=result
                    continue
                if lexeme[0][0] == 'I IZ':
                    errors, result, visible_output = evaluate_function_call(lexeme, line, 0, function_table, symbol_table, errors)
                    if len(temp)==len(errors):
                        symbol_table['IT'] = result
                        continue
                    return errors, None
            if loop_operation=='UPPIN':
                symbol_table[loop_variable] = symbol_table[loop_variable] + 1
            elif loop_operation=='NERFIN':
                symbol_table[loop_variable] = symbol_table[loop_variable] - 1
        return errors, visible_output
    # Perform the operation
    errors, visible_output = evaluate(text, symbol_table, errors)
    return errors, visible_output