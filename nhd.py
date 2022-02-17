from lex import *

def main():
    src = "IF+-123 foo*THEN/"
    lex = LexicalAnalysis(src)
    
    token = lex.get_token()
    while token.type != TokenType.EOF:
        print(token.type)
        token = lex.get_token()

main()