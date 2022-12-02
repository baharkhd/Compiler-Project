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