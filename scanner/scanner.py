from .writer import *
from .reader import *
from .dfa import *


class Scanner:
    def __init__(self):
        self.dfa = DFA(Common.N_OF_STATES.value)
        self.dfa.define_dfa()
        self.reader = Reader()
        self.writer = Writer()
        self.line_num = 1

    def get_next_token(self, curr_state):
        while True:
            next_ch, next_ch_type = self.reader.get_next_char()
            print("-----", next_ch, next_ch_type)
            if next_ch_type == CharType.INVALID:
                # here we should raise INVALID error
                pass

            next_state = curr_state.get_next_state(next_ch_type)

            if next_state is None:
                # error state
                pass

            if next_state.is_final:
                if next_state.has_star:
                    self.reader.decrease_pointer()
                    found_token = self.reader.string_read
                    token_type = next_state.token_type
                    break
                else:
                    found_token = self.reader.string_read
                    token_type = next_state.token_type
                    break
            else:
                continue

        return found_token, token_type

    def run_scanner(self):
        first_ch, first_ch_type = self.reader.get_next_char()
        self.reader.start_pointer = 0
        curr_state = self.dfa.start_state

        while True:
            next_token, next_token_type = self.get_next_token(curr_state)
            self.reader.reset_pointers()
            print(next_token)

        

