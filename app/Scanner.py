from app.Token import Token
from app.TokenType import TokenType as TT
import app.Lox as Lox


def isDigit(c: str) -> bool:
    """
    Check if c is a digit (for our purposes)
    :param c: character to check
    :return: True or False
    """
    return ord('0') <= ord(c) <= ord('9')


def isAlpha(c: str) -> bool:
    """
    Check if c is an alphabet character (for our purposes)
    :param c: character to check
    :return: True or False
    """
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'


def isAlphaNumeric(c: str) -> bool:
    """
    Check if c is an alphanumeric character (for our purposes)
    :param c: character to check
    :return: True or False
    """
    return isAlpha(c) or isDigit(c)


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


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.source_len = len(source)
        self.tokens = list()  # list[TokenType]
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TT.EOF, '', None, self.line))
        return self.tokens

    def isAtEnd(self) -> bool:
        return self.current >= self.source_len

    def scanToken(self):
        c = self.advance()
        match c:
            case '(':
                self.addToken(TT.LEFT_PAREN)
            case ')':
                self.addToken(TT.RIGHT_PAREN)
            case '{':
                self.addToken(TT.LEFT_BRACE)
            case '}':
                self.addToken(TT.RIGHT_BRACE)
            case ',':
                self.addToken(TT.COMMA)
            case '.':
                self.addToken(TT.DOT)
            case '-':
                self.addToken(TT.MINUS)
            case '+':
                self.addToken(TT.PLUS)
            case ';':
                self.addToken(TT.SEMICOLON)
            case '*':
                self.addToken(TT.STAR)
            case '!':
                self.addToken(TT.BANG_EQUAL if self.match('=') else TT.BANG)
            case '=':
                self.addToken(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL)
            case '<':
                self.addToken(TT.LESS_EQUAL if self.match('=') else TT.LESS)
            case '>':
                self.addToken(TT.GREATER_EQUAL if self.match('=') else TT.GREATER)
            case '/':
                if self.match('/'):  # found a '//' (comment)
                    self.comment()
                elif self.match('*'):  # found a '/*' (block comment)
                    self.blockComment()
                else:
                    self.addToken(TT.SLASH)
            case ' ' | '\r' | '\t':  # ignore whitespace
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if isDigit(c):  # number literal
                    self.number()
                elif isAlpha(c):  # identifier or keyword
                    self.identifier()
                else:
                    Lox.error(self.line, f'Unexpected character: {c}')

    def advance(self) -> str:
        """
        Consume and return a character, advancing to the next in self.source.
        :return: character currently at self.current
        """
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, t_type: TT, literal: object = None):
        """
        Add a token to the current list of tokens.
        :param t_type: TokenType of the token
        :param literal: ??????
        """
        text = self.source[self.start:self.current]
        self.tokens.append(Token(t_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        """
        Check if the next character matches expected. If so, consume it.
        :param expected: the character to check for
        :return: True if match found, False if not
        """
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.advance()
        return True

    def peek(self) -> str:
        """
        Peek at the current character in source. Do not advance/consume.
        :return:
        """
        if self.isAtEnd(): return '\0'
        return self.source[self.current]

    def peekNext(self) -> str:
        """Peek at the next character in source. Do not advance/consume."""
        if self.current + 1 >= self.source_len: return '\0'
        return self.source[self.current + 1]

    def string(self):
        """
        Consume a string from source
        """
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.isAtEnd():
            Lox.error(self.line, "Unterminated string.")
            return

        self.advance()  # eat closing "

        string = self.source[self.start + 1: self.current - 1]
        self.addToken(TT.STRING, string)

    def number(self):
        """
        Consume a number literal from source.
        """
        while isDigit(self.peek()): self.advance()

        if self.peek() == '.' and isDigit(self.peekNext()):
            self.advance()  # eat .

        while isDigit(self.peek()): self.advance()

        number = float(self.source[self.start:self.current])
        self.addToken(TT.NUMBER, number)

    def identifier(self):
        while isAlphaNumeric(self.peek()): self.advance()

        text = self.source[self.start:self.current]
        self.addToken(keywords.get(text, TT.IDENTIFIER))

    def comment(self):
        """
        Consume a comment from source.
        """
        while self.peek() != '\n' and not self.isAtEnd(): self.advance()

    def blockComment(self):
        """
        Consume a block comment from source
        """
        while (self.peek() != "*" and self.peekNext() != '/') and not self.isAtEnd():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.isAtEnd():
            Lox.error(self.line, "Unterminated block comment.")
            return

        self.advance()
        self.advance()  # consume closing */
