from statics import *


class Writer:
    def __init__(self):
        self.token_table = []

    def write_token(token_type, token, next_line=False):
        token_file = open(TOKENS_FILE_PATH, "w")

        if next_line:
            token_file.write('\n')
        token_file.write('({}, {}) '.format(token_type, token))
        token_file.close()
