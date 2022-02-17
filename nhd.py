from lex import *

def main():
    src = "TEST TOKENS"
    lex = LexicalAnalysis(src)

    while lex.peek() != '\0':
        print(lex.curr_char)
        lex.next_char()

main()