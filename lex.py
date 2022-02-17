import enum
from lib2to3.pgen2 import token
import sys

from pyparsing import string_start
class LexicalAnalysis:
    def __init__(self, src):
        self.source = src + '\n'
        self.curr_char = ''
        self.curr_pos = -1
        self.next_char()

    # Return the next token in the source code.
    def get_token(self):
        self.whitespace_omit()
        self.comment_omit()
        token = None
        if self.curr_char == '+':
            token = Token(self.curr_char, TokenType.PLUS)
        elif self.curr_char == '-':
            token = Token(self.curr_char, TokenType.MINUS)
        elif self.curr_char == '*':
            token = Token(self.curr_char, TokenType.ASTERISK)
        elif self.curr_char == '/':
            token = Token(self.curr_char, TokenType.SLASH)
        elif self.curr_char == '=':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.EQEQ)
            else:
                token = Token(self.curr_char, TokenType.EQ)
        elif self.curr_char == '>':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.GTEQ)
            else:
                token = Token(self.curr_char, TokenType.GT)
        elif self.curr_char == '<':
                if self.peek() == '=':
                    last_char = self.curr_char
                    self.next_char()
                    token = Token(last_char + self.curr_char, TokenType.LTEQ)
                else:
                    token = Token(self.curr_char, TokenType.LT)
        elif self.curr_char == '!':
            if self.peek() == '=':
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.NOTEQ)
            else:
                self.invalid("!" + self.peek() +  "isn't a valid operator, did you mean !=")
        elif self.curr_char == '\"':
            self.next_char()
            string_start_pos = self.curr_pos
            while self.curr_char != '\"':
                if self.curr_char in ['\r','\n','\t','\\','%']:
                    self.invalid("String contains illegal characters.")
                self.next_char()
            string_text = self.source[string_start_pos:self.curr_pos]
            token = Token(string_text, TokenType.STRING)
        elif self.curr_char.isdigit():
            number_start_pos = self.curr_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()
                if not self.peek().isdigit():
                    self.invalid("No numbers after decimal point")
                while self.peek().isdigit():
                    self.next_char()
            number = self.source[number_start_pos:self.curr_pos+1]
            token = Token(number, TokenType.NUMBER)
        elif self.curr_char.isalpha():
            ident_start_pos = self.curr_pos
            while self.peek().isalnum():
                self.next_char()
            text = self.source[ident_start_pos:self.curr_pos+1]
            keyword = Token.check_keyword(text)
            if keyword == None:
                token = Token(text, TokenType.IDENT)
            else:
                token = Token(text, keyword)

                            
        elif self.curr_char == '\n':
            token = Token(self.curr_char, TokenType.NEWLINE)
        elif self.curr_char == '\0':
            token = Token('', TokenType.EOF)
        else:
            self.invalid("Unknown token: " + self.curr_char)
        self.next_char()
        return token

    # Ignore whitespace when considering tokens, with the exception of new lines.
    def whitespace_omit(self):
        while self.curr_char == ' ' or self.curr_char == '\t' or self.curr_char == '\r':
            self.next_char()

    # Like above whitespace function, this ignores comments in source code.
    def comment_omit(self):
        if self.curr_char == "$":
            while self.curr_char != '\n':
                self.next_char()

    # Report invalid tokens by returning an error message.
    def invalid(self, message):
        print("ERROR: " + message)
        sys.exit()

    # Helper function to read in next character and increment position.
    def next_char(self):
        self.curr_pos += 1
        if self.curr_pos >= len(self.source): # We have reached end of the source code.
            self.curr_char = '\0'
        else:
            self.curr_char = self.source[self.curr_pos]

    # Same as above function, except doesn't increment position (ie, just looks at the next character without doing anything).
    def peek(self):
        if self.curr_pos+1 >= len(self.source):
            return '\0'
        return self.source[self.curr_pos+1]

# Records token text and type of token.
class Token:
    def __init__(self, token_text, token_type):
        self.text = token_text
        self.type = token_type
    
    @staticmethod
    def check_keyword(text):
        for type in TokenType:
            if type.name == text and (100 <= type.value < 200):
                return type
        return None


# Enum class for each possible token type (extends enum class)
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords.
	VARIABLE = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	SET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211