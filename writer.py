from statics import *
from anytree import Node, RenderTree


class Writer:
    def write_tokens(self, tokens_table: dict):
        key_words = tokens[TokenType.KEYWORD]
        with open(TOKENS_FILE_PATH, 'w') as f:
            for token in tokens_table:
                f.write(f'{token}.\t')
                for t in tokens_table[token]:
                    if t[0] != TokenType.KEYWORD_ID.value:
                        f.write(f'({t[0]}, {t[1]}) ')
                    else:
                        if t[1] not in key_words:
                            f.write(f'({TokenType.ID.value}, {t[1]}) ')
                        else:
                            f.write(f'({TokenType.KEYWORD.value}, {t[1]}) ')
                f.write('\n')

    def write_errors(self, errors_table: dict):
        if not errors_table:
            with open(ERRORS_FILE_PATH, 'w') as f:
                f.write(f'{Common.NO_ERROR.value}')
        else:
            with open(ERRORS_FILE_PATH, 'w') as f:
                for error in errors_table:
                    f.write(f'{error}.\t')
                    for err in errors_table[error]:
                        f.write(f'({err[0]}, {err[1]}) ')
                    f.write('\n')

    def write_symbols(self, symbols_table: list):
        key_words = tokens[TokenType.KEYWORD]
        with open(SYMBOLS_FILE_PATH, 'w') as f:
            for k in key_words:
                f.writelines(f'{key_words.index(k) + 1}.\t{k}\n')
            symbols_table = [s for s in symbols_table if s not in key_words]
            for token in symbols_table:
                f.writelines(f'{symbols_table.index(token) + len(key_words) + 1}.\t{token}\n')

    def write_parse_tree(self, root_node):
        for pre, fill, node in RenderTree(root_node):
            print("%s%s" % (pre, node.name))

    def write_parse_tree(self, root_node, PATH='parse_tree.txt'):
        tree_lines = ''
        with open(PATH, "+w", encoding="utf-8") as file:
            for pre, fill, node in RenderTree(root_node):
                tree_lines += "%s%s" % (pre, node.name)
                if node.name != "$":
                    tree_lines += '\n'

            file.write(tree_lines)

    def write_errors(self, all_errors, PATH='syntax_errors.txt'):
        with open(PATH, "+w", encoding="utf-8") as file:
            for err in all_errors:
                file.write(err + "\n")
