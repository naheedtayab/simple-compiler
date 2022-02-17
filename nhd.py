from lex import *
from parser import *

def main():
    print("NHD Version 1.0.0 - 2022")

    if len(sys.argv) != 2:
        sys.exit("ERROR: No source file provided for compile")
    with open(sys.argv[1], 'r') as src_file:
        src = src_file.read()
    
    lex = LexicalAnalysis(src)
    parser = Parser(lex)

    parser.program()
    print("Parsing completed.")
main()