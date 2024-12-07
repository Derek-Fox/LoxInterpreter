from lox.LoxToken import LoxToken, TokenType as TT

class Scanner:
    keywords = {
        "and": TT.AND,
        "class": TT.CLASS,
        "else": TT.ELSE,
        "false": TT.FALSE,
        "for": TT.FOR,
        "fun": TT.FUN,
        "if": TT.IF,
        "nil": TT.NIL,
        "or": TT.OR,
        "print": TT.PRINT,
        "return": TT.RETURN,
        "super": TT.SUPER,
        "this": TT.THIS,
        "true": TT.TRUE,
        "var": TT.VAR,
        "while": TT.WHILE
    }

    def __init__(self, source: str):
        self.source = source
        self.source_len = len(source)
        self.tokens = list()  # list[TokenType]
        self.start = 0
        self.current = 0
        self.line = 1

    def scan(self) -> list[LoxToken]:
        """
        Scan the characters from source and form tokens.
        :return: List of tokens.
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(LoxToken(TT.EOF, '', None, self.line))
        return self.tokens

    def scan_token(self):
        """
        Find Token that corresponds to the character at curr and add to tokens.
        """
        c = self.advance()
        match c:
            case '(':
                self.add_token(TT.LEFT_PAREN)
            case ')':
                self.add_token(TT.RIGHT_PAREN)
            case '{':
                self.add_token(TT.LEFT_BRACE)
            case '}':
                self.add_token(TT.RIGHT_BRACE)
            case ',':
                self.add_token(TT.COMMA)
            case '.':
                self.add_token(TT.DOT)
            case '-':
                self.add_token(TT.MINUS)
            case '+':
                self.add_token(TT.PLUS)
            case ';':
                self.add_token(TT.SEMICOLON)
            case '*':
                self.add_token(TT.STAR)
            case '!':
                self.add_token(TT.BANG_EQUAL if self.match('=') else TT.BANG)
            case '=':
                self.add_token(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL)
            case '<':
                self.add_token(TT.LESS_EQUAL if self.match('=') else TT.LESS)
            case '>':
                self.add_token(TT.GREATER_EQUAL if self.match('=') else TT.GREATER)
            case '/':
                if self.match('/'):  # found a '//' (comment)
                    self.comment()
                elif self.match('*'):  # found a '/*' (block comment)
                    self.block_comment()
                else:
                    self.add_token(TT.SLASH)
            case ' ' | '\r' | '\t':  # ignore whitespace
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):  # number literal
                    self.number()
                elif self.is_alpha(c):  # identifier or keyword
                    self.identifier()
                else:
                    self.error(self.line, f'Unexpected character: {c}')

    def advance(self) -> str:
        """
        Consume and return a character, advancing to the next in self.source.
        :return: character at current
        """
        c = self.source[self.current]
        self.current += 1
        return c

    def add_token(self, t_type: TT, literal: object = None):
        """
        Add a token to the current list of tokens.
        :param t_type: TokenType of the token
        :param literal: literal value associated with Token
        """
        text = self.source[self.start:self.current]
        self.tokens.append(LoxToken(t_type, text, literal, self.line))

    def is_at_end(self) -> bool:
        """
        Check if scanner hit end of source.
        :return: True if current greater-equal than length of source
        """
        return self.current >= self.source_len

    def match(self, expected: str) -> bool:
        """
        Check if the next character matches expected. If so, consume it.
        :param expected: the character to check for
        :return: True if match found, False if not
        """
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False

        self.advance()
        return True

    def peek(self) -> str:
        """
        Peek at the current character in source. Do not advance/consume.
        :return:
        """
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        """
        Peek at the next character in source. Do not advance/consume.
        """
        if self.current + 1 >= self.source_len: return '\0'
        return self.source[self.current + 1]

    def string(self):
        """
        Consume a string from source
        """
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            self.error(self.line, "Unterminated string.")
            return

        self.advance()  # eat closing "

        string = self.source[self.start + 1: self.current - 1]
        self.add_token(TT.STRING, string)

    def number(self):
        """
        Consume a number literal from source.
        """
        while self.is_digit(self.peek()): self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()  # eat .

        while self.is_digit(self.peek()): self.advance()

        number = float(self.source[self.start:self.current])
        self.add_token(TT.NUMBER, number)

    def identifier(self):
        """
        Consume an identifier from source.
        :return:
        """
        while self.is_alpha_numeric(self.peek()): self.advance()

        text = self.source[self.start:self.current]
        self.add_token(self.keywords.get(text, TT.IDENTIFIER))

    def comment(self):
        """
        Consume a comment from source.
        """
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()

    def block_comment(self):
        """
        Consume a block comment from source
        """
        while (self.peek() != "*" and self.peek_next() != '/') and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            self.error(self.line, "Unterminated block comment.")
            return

        self.advance()
        self.advance()  # consume closing */

    @classmethod
    def is_digit(cls, c: str) -> bool:
        """
        Check if c is a digit (for our purposes)
        :param c: character to check
        :return: True or False
        """
        return ord('0') <= ord(c) <= ord('9')

    @classmethod
    def is_alpha(cls, c: str) -> bool:
        """
        Check if c is an alphabet character (for our purposes)
        :param c: character to check
        :return: True or False
        """
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    @classmethod
    def is_alpha_numeric(cls, c: str) -> bool:
        """
        Check if c is an alphanumeric character (for our purposes)
        :param c: character to check
        :return: True or False
        """
        return cls.is_alpha(c) or cls.is_digit(c)

    @classmethod
    def error(cls, line: int, message: str):
        from lox.Lox import Lox
        Lox.error_line(line, message)
