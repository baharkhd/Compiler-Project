import enum

INPUT_FILE_PATH = 'inputs/input.txt'
TOKENS_FILE_PATH = 'tokens.txt'
ERRORS_FILE_PATH = 'lexical_errors.txt'
SYMBOLS_FILE_PATH = 'symbol_table.txt'


class TokenType(enum.Enum):
    KEYWORD = 'KEYWORD'
    ID = 'ID'
    KEYWORD_ID = 'KEYWORD ID'
    NUM = 'NUM'
    SYMBOL = 'SYMBOL'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'


class Common(enum.Enum):
    EOF = 'EOF'
    N_OF_STATES = 19
    FINAL_STATES = [2, 4, 5, 6, 8, 9, 13, 15, 16, 18]
    STAR_STATES = [2, 4, 9, 16, 18]


class Transitions(enum.Enum):
    DIGIT = '0-9'
    NOT_DIGIT = '~(0-9)'
    LETTER = 'a-zA-Z'
    NOT_LETTER = '~(a-zA-Z)'


class CharType(enum.Enum):
    DIGIT = '[0-9]'
    NOT_DIGIT = '[^0-9]'
    LETTER = '[a-zA-Z]'
    NOT_LETTER = '[^a-zA-Z]'
    DIGIT_LETTER = '[a-zA-Z0-9]'
    NOT_DIGIT_LETTER = '[^a-zA-Z0-9]'
    SYMBOL_NEQUAL_NSTAR = 'SYMBOL_NEQUAL_NSTAR'
    SINGLE_SYMBOL = ';|:|,|\[|\]|\(|\)|{|}|\+|-|<'
    WHITESPACE = '\s|\n|\t|\f|\r|\v'
    EOF = 'EOF'
    EOF_ENTER = 'EOF|\n'
    EQUAL = '='
    NEQUAL = '^='
    STAR = '*'
    NSTAR = '^*'
    SLASH = '/'
    NSLASH = '^/'
    NSTAR_NSLASH = '^/*'
    INVALID = 'INVALID'


tokens = {
    TokenType.KEYWORD: ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif'],
    TokenType.SYMBOL: [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==', '/'],
    TokenType.COMMENT: {'/*': '*/', '//': ['\n', Common.EOF]},
    TokenType.WHITESPACE: ['', '\n', '\r', '\t', '\v', '\f']
}
