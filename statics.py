import enum
import re

INPUT_FILE_PATH = 'input.txt'
TOKENS_FILE_PATH = 'tokens.txt'
ERRORS_FILE_PATH = 'lexical_errors.txt'
SYMBOLS_FILE_PATH = 'symbol_table.txt'


class ActionType(enum.Enum):
    REDUCE = 'REDUCE'
    SHIFT = 'SHIfT'


class TokenType(enum.Enum):
    KEYWORD = 'KEYWORD'
    ID = 'ID'
    KEYWORD_ID = 'KEYWORD ID'
    NUM = 'NUM'
    SYMBOL = 'SYMBOL'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ERROR = 'ERROR'


class Common(enum.Enum):
    EOF = 'EOF'
    N_OF_STATES = 19
    FINAL_STATES = [2, 4, 5, 6, 8, 9, 13, 15, 16, 18]
    STAR_STATES = [2, 4, 9, 16, 18]
    ERROR_DETECTED = 'ERROR DETECTED'
    NO_ERROR = 'There is no lexical error.'


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
    WHITESPACE = '\s|\t|\f|\r|\v'
    WHITESPACE_EX_ENTER = '\s|\t|\f|\r|\v'
    EOF = 'EOF'
    EOF_ENTER = 'EOF|\n'
    ENTER = '\n'
    EQUAL = '='
    NEQUAL = '^='
    STAR = '*'
    NSTAR = '^*'
    SLASH = '/'
    NSLASH = '^/'
    NSTAR_NSLASH = '^/*'
    INVALID = 'INVALID'


class ErrorType(enum.Enum):
    INVALID_INPUT = 'Invalid input'
    INVALID_NUMBER = 'Invalid number'
    UNMATCHED_COMMENT = 'Unmatched comment'
    UNCLOSED_COMMENT = 'Unclosed comment'


tokens = {
    TokenType.KEYWORD: ['if', 'else', 'void', 'int', 'while', 'break', 'switch', 'default', 'case', 'return', 'endif'],
    TokenType.SYMBOL: [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '==', '/'],
    TokenType.COMMENT: {'/*': '*/', '//': ['\n', Common.EOF]},
    TokenType.WHITESPACE: ['', '\n', '\r', '\t', '\v', '\f']
}


def get_token_type(token):
    if token in tokens[TokenType.KEYWORD]:
        return TokenType.KEYWORD.value
    elif token in tokens[TokenType.SYMBOL]:
        return TokenType.SYMBOL.value
    elif re.match(r'[0-9]+', token):
        return TokenType.NUM.value
    else:
        return TokenType.ID.value


class ParserErrorType(enum.Enum):
    ILLEGAL_ERROR = 'ILLEGAL_ERROR'
    INPUT_DISCARDED = 'INPUT_DISCARDED'
    STACK_DISCARDED = 'STACK_DISCARDED'
    MISSING_ERROR = 'MISSING_ERROR'
    UNEXPECTED_EOF = 'UNEXPECTED_EOF'


def make_test_json_data():
    test_data = {
        'terminals': ['int', '*', '+', '(', ')', '$'],
        'non_terminals': ['T', 'E'],
        'first': {

        },

        'follow': {

        },

        'grammar': {
            '1': ['E', '->', 'T'],
            '2': ['E', '->', 'T', '+', 'E'],
            '3': ['T', '->', '(', 'E', ')'],
            '4': ['T', '->', 'int', '*', 'T'],
            '5': ['T', '->', 'int'],
        },

        'parse_table': {
            '0': {'int': 'shift_4', '(': 'shift_3', 'E': '1', 'T': '2'},
            '1': {'$': 'accept'},
            '2': {'+': 'shift_6', ')': 'reduce_1', '$': 'reduce_1'},
            '4': {'+': 'reduce_5', '*': 'shift_6', ')': 'reduce_5', '$': 'reduce_5'},
            '6': {'int': 'shift_4', '(': 'shift_3', 'T': '9'},
            '9': {'+': 'shift_4', ')': 'reduce_4', '$': 'reduce_4'},
        }

    }

    return test_data
