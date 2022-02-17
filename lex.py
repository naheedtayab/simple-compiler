class LexicalAnalysis:
    def __init__(self, src):
        self.source = src + '\n'
        self.curr_char = ''
        self.curr_pos = -1
        self.next_char()

    # Return the next token in the source code.
    def get_token(self):
        pass

    # Ignore whitespace when considering tokens, with the exception of new lines.
    def whitespace_omit(self):
        pass

    # Like above whitespace function, this ignores comments in source code.
    def comment_omit(self):
        pass

    # Report invalid tokens by returning an error message.
    def invalid(self, message):
        pass

    # Helper function to read in next character and increment position.
    def next_char(self):
        self.curr_pos += 1
        if self.curr_pos >= len(self.source): # We have reached end of the source code.
            self.curr_pos = '\0'
        else:
            self.curr_char = self.source[self.curr_pos]

    # Same as above function, except doesn't increment position (ie, just looks at the next character without doing anything).
    def peek(self):
        if self.curr_pos+1 >= len(self.source):
            return '\0'
        return self.source[self.curr_pos+1]

