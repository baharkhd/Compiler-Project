from statics import *


class Writer:
    def write_tokens(self, tokens_table: dict):
        with open(TOKENS_FILE_PATH, 'w') as f:
            for token in tokens_table:
                f.writelines(f'{token}: {[t for t in tokens_table[token]]}\n')

    def write_errors(self, errors_table: dict):
        with open(ERRORS_FILE_PATH, 'w') as f:
            for token in errors_table:
                f.writelines(f'{token}: {[t for t in errors_table[token]]}\n')

    def write_symbols(self, symbols_table: list):
        key_words = tokens[TokenType.KEYWORD]
        with open(SYMBOLS_FILE_PATH, 'w') as f:
            for k in key_words:
                f.writelines(f'{key_words.index(k) + 1}: {k}\n')
            for token in symbols_table:
                if token not in key_words:
                    f.writelines(f'{symbols_table.index(token) + len(key_words) + 1}: {token}\n')


# if __name__ == "__main__":
#     # tokens = {1: [('KEYWORD', 'void'), ('ID', 'main'), ('SYMBOL', '('), ('KEYWORD', 'void'), ('SYMBOL', ')'),
#     #               ('SYMBOL', '{')],
#     #           2: [('KEYWORD', 'int'), ('ID', 'a'), ('SYMBOL', '='), ('NUM', '0'), ('SYMBOL', ';')]}
#
#     symbols = ['a', 'b', 'cde', 'if']
#     writer = Writer()
#     # writer.write_tokens(tokens)
#     writer.write_symbols(symbols)
