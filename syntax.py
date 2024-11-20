import lexical
import os

def syntax(text):
    hai = 0
    kthxbye = 0
    wazzup = 0
    buhbye = 0
    obtw = -1
    tldr = -1
    syntaxResult = ''
    for line in range(0, len(text.splitlines())):
        lexeme = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if lexeme is not None:
            # Remove 'BTW' comment lexemes
            if ['BTW', 'Comment Delimiter'] in lexeme:
                lexeme.pop(lexeme.index(['BTW', 'Comment Delimiter'])+1)
                lexeme.pop(lexeme.index(['BTW', 'Comment Delimiter']))
            if ['OBTW','Comment Delimiter'] in lexeme:
                obtw = 1
                del lexeme[lexeme.index(['OBTW', 'Comment Delimiter']):]
                continue
            if obtw==1:
                if ['TLDR','Identifier'] not in lexeme:
                    lexeme.clear()
                    continue
                else:
                    obtw = 0
                    tldr = 0
                    del lexeme[:lexeme.index(['TLDR','Comment Delimiter'])]
            if ['TLDR', 'Comment Delimiter'] in lexeme:
                tldr = 1
                lexeme.pop(lexeme.index(['TLDR', 'Comment Delimiter']))
            print(f'{lexeme}\n')

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
