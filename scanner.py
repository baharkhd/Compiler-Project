from writer import *
from reader import *
from dfa import *


class Scanner:
    def __init__(self):
        self.dfa = DFA(Common.N_OF_STATES.value)
        self.dfa.define_dfa()
        self.reader = Reader()
        self.writer = Writer()

        self.text = ''
        self.curr_state = None

        self.line_num = 1
        self.end_of_file = False
        self.has_decreseaed = False
        self.has_error = False
        self.comment_opened = False
        self.one_line_comment = False

        self.start = True

    def check_EOF(self):
        if self.reader.end_pointer == len(self.text):
            return True
        else:
            return False

    def get_next_token(self):
        token_line_n = self.line_num
        token = ''
        token_type = ''

        errors = []
        tokens = []
        key_ids = []

        while True:
            if self.check_EOF():
                break

            #print(self.reader.end_pointer)
            curr_char = self.text[self.reader.end_pointer]
            char_type = self.reader.get_char_type(curr_char)

            if char_type == CharType.INVALID:
                token = self.text[self.reader.start_pointer:self.reader.end_pointer + 1]
                token_type = ErrorType.INVALID_INPUT
                token_line_n = self.line_num
                self.reader.start_pointer = self.reader.end_pointer
                self.reader.increase_end_pointer()
                self.reader.start_pointer += 1

                errors.append((self.line_num, token, token_type.value))
                self.has_error = True
                break

            next_state = self.curr_state.get_next_state(char_type)
            self.reader.increase_end_pointer()
            print("!!!!!!", curr_char, self.curr_state.id, curr_char == '\n')

            if curr_char == '\n':
                #print("^^^^^^^^^^^^^^^^^")
                self.line_num += 1

            if next_state == Common.ERROR_DETECTED:
                #print("????")
                if self.curr_state == 14 or self.curr_state == 11 or self.curr_state == 12:
                    pass
                else:
                    self.curr_state = self.dfa.start_state

                    # Here we handle Invalid Number
                    token = self.text[self.reader.start_pointer:self.reader.end_pointer]
                    token_type = ErrorType.INVALID_NUMBER

                    errors.append((self.line_num, token, token_type.value))

            else:
                
                #print("1.-----", next_state.id)
                if next_state.is_final:
                    #print("2.-----")
                    if next_state.has_star:
                        #print("3.-----")
                        token = self.text[self.reader.start_pointer:self.reader.end_pointer - 1]
                        token_type = next_state.token_type
                        token_line_n = self.line_num
                        self.reader.start_pointer = self.reader.end_pointer - 1
                        self.reader.decrease_end_pointer()

                        if next_state.id == 4:
                            key_ids.append(token)
                        break
                    else:
                        #print("4.-----")
                        token = self.text[self.reader.start_pointer:self.reader.end_pointer]
                        token_type = next_state.token_type
                        token_line_n = self.line_num
                        self.reader.start_pointer = self.reader.end_pointer
                        break
                #else:
                    #if next_state.id == 14:

                self.curr_state = next_state

        if self.has_error:
            self.has_error = False
            return None, errors, key_ids
        else:
            return (token_line_n, token_type.value, token), errors, key_ids




    def handle_all_tokens(self, all_tokens):
        tokens_dict = {}

        for token in all_tokens:
            if token[0] in tokens_dict.keys():
                tokens_dict[token[0]].append((token[1], token[2]))
            else:
                tokens_dict[token[0]] = [(token[1], token[2])]

        return tokens_dict

    def handle_all_errors(self, all_errors):
        errors_dict = {}

        for error in all_errors:
            if error[0] in errors_dict.keys():
                errors_dict[error[0]].append((error[1], error[2]))
            else:
                errors_dict[error[0]] = [(error[1], error[2])]

        return errors_dict

    def run_scanner(self):
        #first_ch, first_ch_type = self.reader.get_next_char()
        #self.reader.start_pointer = 0
        #next_ch, next_ch_type = first_ch, first_ch_type

        self.text = self.reader.read_input_code()

        all_tokens = []
        all_errors = []
        all_keys_ids = []

        
        while True:
            self.curr_state = self.dfa.start_state
            token, errors, keys_ids = self.get_next_token()
            if token and token[1] != TokenType.WHITESPACE.value and token[1] != TokenType.COMMENT.value:
                all_tokens.append(token)

            print("++++++", all_tokens)

            all_errors.extend(errors)
            all_keys_ids.extend(keys_ids)

            #print("-------")
            if self.check_EOF():
                print("==========", self.curr_state.id)
                if self.curr_state.id == 11 or self.curr_state.id == 12:
                    print("^^^^^^^^^^^^^^^^^ . vagheannnnnnnn?", self.text[self.reader.start_pointer:self.reader.end_pointer])
                break

            
            #self.reader.reset_pointers(self.has_decreseaed)
            # print("^^^^^^^^^", all_tokens)
            #print("&&&&&&&&&&&", all_errors)
            #print("##########", all_keys_ids)

            #if self.end_of_file:
            #    break
            #if next_ch_type == CharType.EOF:
            #    break

        print("---------")
        for (ln, t_type, t) in all_tokens:
            print(ln, t, t_type)

        print("********")

        for e in all_errors:
            print(e)

        tokens_dict = self.handle_all_tokens(all_tokens)
        errors_dict = self.handle_all_errors(all_errors)
        all_keys_ids = list(set(all_keys_ids))

        self.writer.write_tokens(tokens_dict)
        self.writer.write_errors(errors_dict)
        self.writer.write_symbols(all_keys_ids)

        

