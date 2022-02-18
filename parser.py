import sys
from lex import *

# Track current token and check if code is consistent with NHD grammar.
class Parser:
    def __init__(self, lex):
        self.lexer = lex

        self.curr_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

        # Sets responsible for tracking symbols and labels declared to check that source code doesn't try to access undeclared, or initialise already declared variables.
        self.symbols = set()
        self.labels_declared = set()
        self.labels_goto = set()

    def check_token(self, type):
        return type == self.curr_token.type

    def check_peek(self, type):
        return type == self.peek_token.type

    def match(self, type):
        if not self.check_token(type):
            self.invalid("Expected: " + type.name + ", got: " + self.curr_token.type.name)
        self.next_token()

    def next_token(self):
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def invalid(self, message):
        sys.exit("ERROR: " + message)

    # Grammar rules
    def program(self):
        print("PROGRAM")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()
        
        # Check that labels in GOTO statements have already been declared... so they can be GOTO'd.
        for label in self.labels_goto:
            if label not in self.labels_declared:
                self.invalid("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        #Check first token for statement type

        # PRINT
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()

        # IF 
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)

        # WHILE 
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
        
        # LABEL
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()

            if self.curr_token.text in self.labels_declared:
                self.invalid("Label already exists: " + self.curr_token.text)
            self.labels_declared.add(self.curr_token.text)
            self.match(TokenType.IDENT)
        
        # GOTO
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.labels_goto.add(self.curr_token.text)
            self.match(TokenType.IDENT)
        
        # SET
        elif self.check_token(TokenType.SET):
            print("STATEMENT-SET")
            self.next_token()
            if self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        
        # INPUT
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()

            if self.curr_token not in self.symbols:
                self.symbols.add(self.curr_token.text)

            self.match(TokenType.IDENT)
        
        # Statement isn't valid (token is none of the above types)
        else:
            self.invalid("INVALID STATEMENT: " + self.curr_token.text)
        
        # New line at end of function call.
        self.nl()

    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    # For comparison operations, eg: 5 >= 3, x == 5
    def comparison(self):
        print("COMPARISON")

        self.expression()
        if self.isComparison():
            self.next_token()
            self.expression()
        else:
            self.invalid("Expected comparison operator at: " + self.curr_token.text)
        
        while self.isComparison():
            self.next_token()
            self.expression()
    
    def isComparison(self):
        # Checks that the current token is one of the comparison operators (listed in the array below)
        ComparisonOperators = [TokenType.GT, TokenType.GTEQ, TokenType.LT, TokenType.LTEQ, TokenType.EQEQ, TokenType.NOTEQ]
        for x in ComparisonOperators:
            if self.check_token(x):
                return True
        return False

    # EXPRESSION: + or -
    def expression(self):
        print("EXPRESSION")
        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()
    
    # TERM: * or / (higher precedent than expression, BIDMAS follows)
    def term(self):
        print("TERM")
        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.next_token()
            self.unary()

    # UNARY: + or - (whether a term is positive or negative)
    def unary(self):
        print("UNARY")
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()        
        self.primary()

    # PRIMARY: What is being compared, an IDENT (eg: x, y) or a NUMBER (1, 5)
    def primary(self):
        print("PRIMARY (" + self.curr_token.text + ")")

        if self.check_token(TokenType.NUMBER): 
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            # Check that the variable exists (in symbols set) otherwise error.
            if self.curr_token.text not in self.symbols:
                self.invalid("Variable: \'" + self.curr_token.text + "\' referenced before assignment")
            self.next_token()
        else:
            self.invalid("Unexpected token: " + self.curr_token.text)