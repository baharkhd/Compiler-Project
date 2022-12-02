import enum

INPUT_FILE_PATH = 'inputs/input.txt'
TOKENS_FILE_PATH = 'tokens.txt'
ERRORS_FILE_PATH = 'lexical_errors.txt'
SYMBOLS_FILE_PATH = 'symbol_table.txt'


class TokenType(enum.Enum):
    KEYWORD = 'KEYWORD'
    ID = 'ID'
    NUM = 'NUM'
    SYMBOL = 'SYMBOL'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'


class Common(enum.Enum):
    EOF = 'EOF'


class Transitions(enum.Enum):
    DIGIT = '0-9'
    NOT_DIGIT = '~(0-9)'
    LETTER = 'a-zA-Z'
    NOT_LETTER = '~(a-zA-Z)'


tokens = {
    TokenType.KEYWORD: ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif'],
    TokenType.SYMBOL: [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==', '/'],
    TokenType.COMMENT: {'/*': '*/', '//': ['\n', Common.EOF]},
    TokenType.WHITESPACE: ['', '\n', '\r', '\t', '\v', '\f']
}
