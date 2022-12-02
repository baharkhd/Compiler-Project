from writer import *
from reader import *
from dfa import DFA

class Scanner:
    def __init__(self):
        self.dfa = DFA()
        self.dfa.define_dfa()
        self.reader = Reader()
        self.writer = Writer()

        self.line_num = 1

    def validate_char(self, char):
        pass

    def get_next_token(self, file, line_num):
        detemined_tok = ''

        next_char = file.read(1)
        self.validate_char(next_char)



    def run_scanner(self):
        first_ch = reader.get_next_char()
        reader.start_pointer = 0

        while True:
            next_ch = reader.get_next_char()
