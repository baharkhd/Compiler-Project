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
        self.end_of_file = False
        self.has_decreseaed = False

    def get_next_token(self, curr_state, next_ch, next_ch_type):
        #next_ch, next_ch_type = '&&&&&&', '&&&&&&'

        while True:
            #print(self.has_decreseaed)
            if not self.has_decreseaed:
                next_ch, next_ch_type = self.reader.get_next_char()
            print("-----", next_ch, next_ch_type)
            self.has_decreseaed = False

            if next_ch_type == '':
                # it is the end of file
                self.end_of_file = True
            
            if next_ch_type == CharType.INVALID:
                # here we should raise INVALID error
                pass

            print("next ch type?", next_ch_type)
            next_state = curr_state.get_next_state(next_ch_type)
            print("+++++", next_state.id)

            if next_state is None:
                # error state
                pass

            if next_state.is_final:
                #print("here", next_state.id)
                if next_state.has_star:
                    print("decreasing")
                    self.reader.decrease_pointer()
                    self.has_decreseaed = True
                    found_token = self.reader.string_read
                    token_type = next_state.token_type
                    break
                else:
                    found_token = self.reader.string_read
                    token_type = next_state.token_type
                    break
            else:
                curr_state = next_state

            

        #print("****", found_token, token_type)
        return found_token, token_type, next_ch, next_ch_type

    def run_scanner(self):
        first_ch, first_ch_type = self.reader.get_next_char()
        self.reader.start_pointer = 0
        next_ch, next_ch_type = first_ch, first_ch_type

        while True:
            curr_state = self.dfa.start_state
            next_token, next_token_type, next_ch, next_ch_type = self.get_next_token(curr_state, next_ch, next_ch_type)
            self.reader.reset_pointers()
            print(next_token)

        

