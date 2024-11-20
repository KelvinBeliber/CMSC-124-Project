import lexical
import os

def vardec(text, start, i, syntaxResult):
    for line in range(start, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[lexeme].lstrip().rstrip())
        if lexeme is not None:
            ## skips comments
            index = next((i for i, sublist in enumerate(lexeme) if 'Comment lexeme' in sublist), -1)
            if index != -1:
                continue
            if ['OBTW','Comment Delimiter'] in lexeme:
                return 
            if ['TLDR', 'Comment Delimiter'] in lexeme:
                tldr = 1                                                        # TLDR exists in the source code
                del lexeme[:lexeme.index(['TLDR', 'Comment Delimiter'])]
    return [line, i, syntaxResult]


def syntax(text):
    hai = 0
    kthxbye = 0
    wazzup = 0
    buhbye = 0
    obtw = -1
    tldr = -1
    syntaxResult = ''
    for line in range(0, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[lexeme].lstrip().rstrip())
        if lexeme is not None:
            # Remove 'BTW' comment lexemes
            index = next((i for i, sublist in enumerate(lexeme) if 'Comment lexeme' in sublist), -1)
            if index != -1:
                continue

            # Remove 'OBTW' & 'TLDR' multi-line comment lexemes
            if obtw==1:
                if ['TLDR','Comment Delimiter'] not in lexeme:
                    continue
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
                continue
            
            # checking code proper
            for i in range(0,len(lexeme)):
                # check for hai keyword
                if lexeme[i][0] == 'HAI' and hai == -1 and kthxbye == -1:
                # check for declaration keyword
                    if lexeme[i][0] == 'WAZZUP':
                        if wazzup != -1:
                            syntaxResult += f"syntax error at line {line}: WAZZUP has already been declared"
                        if buhbye != -1:
                            syntaxResult += f"syntax error at line {line}: WAZZUP cannot be declared after BUHBYE"
                        if wazzup == -1 and buhbye == -1:
                            vardecResult = vardec(text, line, i, syntaxResult)
                            i = vardecResult[0]
                            syntaxResult = vardecResult[1]
                            wazzup = 0
                    if lexeme[i][0] == 'BUHBYE':
                        if wazzup != 0:
                            syntaxResult += f"syntax error at line {line}: BUHBYE declared without a WAZZUP"
                        elif buhbye != -1:
                            syntaxResult += f"syntax error at line {line}: BUHBYE has already been declared"
                        else:
                            buhbye = 0
                    # check for variable declarations
                    # check for wazzup keyword
                # check for 


def main():
    filename = input("Enter the name of the .lol file: ")
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return
    with open(filename, 'r') as file:
        text = file.read()
    syntax(text)

# Execute main function
if __name__ == "__main__":
    main()
