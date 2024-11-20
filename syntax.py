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
        line = lexical.lex(text.splitlines()[line].lstrip().rstrip())
        if line is not None:
            # Remove 'BTW' comment lexemes
            index = next((i for i, sublist in enumerate(line) if 'Comment Line' in sublist), -1)
            if index != -1:
                continue
            if obtw==1:
                if ['TLDR','Comment Delimiter'] not in line:
                    continue
                else:                                                           # OBTW and TLDR has been paired
                    obtw = 0                                                    
                    tldr = 0
                    del line[:line.index(['TLDR','Comment Delimiter'])]
            if ['OBTW','Comment Delimiter'] in line:
                obtw = 1                                                        # OBTW exists in the source code
                del line[line.index(['OBTW', 'Comment Delimiter']):]
            if ['TLDR', 'Comment Delimiter'] in line:
                tldr = 1                                                        # TLDR exists in the source code
                del line[:line.index(['TLDR', 'Comment Delimiter'])]
            if len(line)==0:
                continue
            # for lexeme in range(0,len(line)): <--- code unfinished 
                # check for hai


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
