from writer import *
from reader import *
from dfa import *


class Scanner:
    def __init__(self):
        self.dfa = DFA(Common.N_OF_STATES.value)
        self.dfa.define_dfa()
        self.reader = Reader()
        self.writer = Writer()
        self.line_num = 1
        self.end_of_file = False
        self.has_decreseaed = False
        self.has_error = False
        self.comment_opened = False
        self.one_line_comment = False

        self.start = True

    def get_next_token(self, curr_state, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids):
        while True:
            if not self.has_decreseaed and not self.start:
                next_ch, next_ch_type = self.reader.get_next_char()
            #print("-----", self.line_num, curr_state.id, next_ch, next_ch_type, next_ch == '\n', self.comment_opened)
            self.start = False
            self.has_decreseaed = False

            if next_ch == '':
                self.end_of_file = True
                next_ch = CharType.EOF
                next_ch_type = CharType.EOF
                break
            
            if next_ch_type == CharType.INVALID and not self.comment_opened:
                #print("1.???????")
                self.has_error = True
                found_token = self.reader.string_read
                token_type = ErrorType.INVALID_INPUT
                break

            if next_ch == '\n':
                #if curr_state.id == 14:
                #    print("-----------------")
                #    self.comment_opened = False

                self.line_num += 1

            next_state = curr_state.get_next_state(next_ch_type, next_ch)

            if next_state == Common.ERROR_DETECTED:
                #print("vaaaaaaaaa?")
                if not self.comment_opened:
                    if curr_state.id == 17:
                        self.has_error = True
                        found_token = self.reader.string_read
                        token_type = ErrorType.UNMATCHED_COMMENT
                    else:
                        # here we should handle error (using all_errors) => based on the current state
                        found_token = self.reader.string_read
                        self.has_error = True
                        #token_type = TokenType.ERROR
                        token_type = ErrorType.INVALID_NUMBER
                    break
            else:

                if curr_state.id == 14 and next_ch == '\n':
                    self.comment_opened = False

                if next_state.id == 11:
                    self.comment_opened = True

                if next_state.id == 13:
                    self.comment_opened = False

                if next_state.id == 14:
                    self.comment_opened = True

                if next_state.is_final:
                    if next_state.has_star:
                        self.reader.decrease_pointer()
                        self.has_decreseaed = True

                        found_token = self.reader.string_read[:-1]
                        token_type = next_state.token_type

                        if next_ch == '\n':
                            self.line_num -= 1

                        if next_state.id == 4:
                            all_keys_ids.append(found_token)
                        break
                    else:
                        found_token = self.reader.string_read
                        token_type = next_state.token_type

                        break
                else:
                    curr_state = next_state
        
        
        if next_ch == CharType.EOF:
            return 'found_token', 'token_type', 'next_ch', 'next_ch_type', all_tokens, all_errors, all_keys_ids

        if self.has_error and not self.comment_opened:
            all_errors.append((self.line_num, found_token, token_type.value))

        if token_type != TokenType.WHITESPACE and token_type != TokenType.COMMENT and not self.has_error and not self.comment_opened:
            all_tokens.append((self.line_num, token_type.value, found_token))

        self.has_error = False 

        return found_token, token_type, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids


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
        first_ch, first_ch_type = self.reader.get_next_char()
        self.reader.start_pointer = 0
        next_ch, next_ch_type = first_ch, first_ch_type

        all_tokens = []
        all_errors = []
        all_keys_ids = []

        file_context = reader.read_input_code()

        while True:
            curr_state = self.dfa.start_state
            next_token, next_token_type, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids = self.get_next_token(curr_state, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids)
            self.reader.reset_pointers(self.has_decreseaed)
            # print("^^^^^^^^^", all_tokens)
            #print("&&&&&&&&&&&", all_errors)
            #print("##########", all_keys_ids)

            if self.end_of_file:
                break
            #if next_ch_type == CharType.EOF:
            #    break

        tokens_dict = self.handle_all_tokens(all_tokens)
        errors_dict = self.handle_all_errors(all_errors)
        all_keys_ids = list(set(all_keys_ids))

        self.writer.write_tokens(tokens_dict)
        self.writer.write_errors(errors_dict)
        self.writer.write_symbols(all_keys_ids)

        

