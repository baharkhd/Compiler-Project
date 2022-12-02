from statics import *


class Writer:
    def __init__(self):
        self.token_table = []
        self.token_table = []
        self.token_table = []

    def write_tokens(self, tokens: dict):
        lines = list(tokens.keys())
        with open(TOKENS_FILE_PATH, 'w') as f:
            for l in lines:
                f.writelines(f'{l}: {[t for t in tokens[l]]}\n')

    def write_errors(self, errors: dict):
        lines = list(tokens.keys())
        with open(ERRORS_FILE_PATH, 'w') as f:
            for l in lines:
                f.writelines(f'{l}: {[t for t in errors[l]]}\n')

    def write_symbols(self, symbols: dict):
        lines = list(tokens.keys())
        with open(TOKENS_FILE_PATH, 'w') as f:
            for l in lines:
                f.writelines(f'{l}: {[t for t in symbols[l]]}\n')

# if __name__ == "__main__":
#     tokens = {1: [('KEYWORD', 'void'), ('ID', 'main'), ('SYMBOL', '('), ('KEYWORD', 'void'), ('SYMBOL', ')'),
#                   ('SYMBOL', '{')],
#               2: [('KEYWORD', 'int'), ('ID', 'a'), ('SYMBOL', '='), ('NUM', '0'), ('SYMBOL', ';')]}
#     writer = Writer()
#     writer.write_token(tokens)
