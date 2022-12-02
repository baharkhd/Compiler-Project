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
        pass

    def run_scanner(self):
        first_ch, first_ch_type = self.reader.get_next_char()
        self.reader.start_pointer = 0

        curr_state = self.dfa.start_state

        while True:
            next_ch, next_ch_type = self.reader.get_next_char()
            next_state = curr_state.get_next_state(next_ch_type)

            if next_state.is_final:
                pass
