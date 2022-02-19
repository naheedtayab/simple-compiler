from lex import *
from parser import *
from emit import *

def main():
    print("NHD Version 1.0.0 - 2022")

    if len(sys.argv) != 2 or not sys.argv[1].endswith(".nhd"):
        sys.exit("ERROR: You have not provided a valid .nhd file to be compiled.")
    with open(sys.argv[1], 'r') as src_file:
        src = src_file.read()
    
    lex = LexicalAnalysis(src)
    emitter = Emitter("out.c")
    parser = Parser(lex, emitter)


    parser.program()
    emitter.write_file()
    print("Compile successful.")
main()