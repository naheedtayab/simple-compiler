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

    def check_token(self, type):
        return type == self.curr_token.type

    def check_peek(self, type):
        return type == self.peek_token.type

    def match(self, type):
        if not self.check_token(type):
            self.invalid("Expected: " + type.name + ", got: " + self.curr_token.type.name)
        self.next_token()

    def next_token(self):
        self.curr_token == self.peek_token
        self.peek_token == self.lexer.get_token()

    def invalid(self, message):
        sys.exit("ERROR: " + message)

    # Grammar rules
    def program(self):
        print("PROGRAM")

        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        #Check first token for statement type

        # "PRINT" (expression or string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        
        # New line at end of function call.
        self.nl()

    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()