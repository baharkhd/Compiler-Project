from statics import *


class Writer:
    def write_tokens(self, tokens_table: dict):
        key_words = tokens[TokenType.KEYWORD]
        with open(TOKENS_FILE_PATH, 'w') as f:
            for token in tokens_table:
                f.write(f'{token}: ')
                for t in tokens_table[token]:
                    if t[0] != TokenType.KEYWORD_ID:
                        print(t)
                        f.write(f'({t[0]}, {t[1]}) ')
                    else:
                        if t[1] not in key_words:
                            f.write(f'({TokenType.ID.value}, {t[1]}) ')
                        else:
                            f.write(f'({TokenType.KEYWORD.value}, {t[1]}) ')
                f.write('\n')

    def write_errors(self, errors_table: dict):
        with open(ERRORS_FILE_PATH, 'w') as f:
            for error in errors_table:
                f.write(f'{error}: ')
                for err in errors_table[error]:
                    f.write(f'({err[0]}, {err[1]}) ')
                f.write('\n')
                # f.writelines(f'{token}: {[t for t in errors_table[token]]}\n')

    def write_symbols(self, symbols_table: list):
        key_words = tokens[TokenType.KEYWORD]
        with open(SYMBOLS_FILE_PATH, 'w') as f:
            for k in key_words:
                f.writelines(f'{key_words.index(k) + 1}: {k}\n')
            for token in symbols_table:
                if token not in key_words:
                    f.writelines(f'{symbols_table.index(token) + len(key_words) + 1}: {token}\n')


if __name__ == "__main__":
    ttt = {1: [('KEYWORD', 'void'), ('ID', 'main'), ('SYMBOL', '('), ('KEYWORD', 'void'), ('SYMBOL', ')'),
               ('SYMBOL', '{')],
           2: [('KEYWORD', 'int'), ('ID', 'a'), ('SYMBOL', '='), ('NUM', '0'), ('SYMBOL', ';')]}

    symbols = ['a', 'b', 'cde', 'if']

    errors = {7: [('3d', 'Invalid number')], 9: [('cd!', 'Invalid input')]}
    writer = Writer()
    # writer.write_tokens(ttt)
    writer.write_errors(errors)
