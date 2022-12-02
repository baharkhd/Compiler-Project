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
        self.has_error = False
        self.comment_opened = False

    def get_next_token(self, curr_state, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids):
        #next_ch, next_ch_type = '&&&&&&', '&&&&&&'

        while True:
            #print("********* curr state *********", curr_state.id)
            if not self.has_decreseaed:
                next_ch, next_ch_type = self.reader.get_next_char()
            print("-----", self.line_num, next_ch, next_ch_type, next_ch == '\n', next_ch == " ")
            self.has_decreseaed = False

            if curr_state.id == 11:
                self.comment_opened = True

            if next_ch == '':
                self.end_of_file = True
                next_ch = CharType.EOF
                next_ch_type = CharType.EOF
                break

            if next_ch == '\n':
                print("hereeeeeeeee", self.line_num)
                self.line_num += 1

            #if next_ch_type == '':
            #    # it is the end of file
            #    self.end_of_file = True
            
            if next_ch_type == CharType.INVALID:
                # here we should raise INVALID error
                self.has_error = True

                found_token = self.reader.string_read
                #token_type = TokenType.ERROR
                token_type = ErrorType.INVALID_INPUT
                break

            next_state = curr_state.get_next_state(next_ch_type, next_ch)

            

            #if curr_state.id == 17 and next_state.id != 18:
            #    self.has_error = True
            #    found_token = self.reader.string_read
            #    token_type = ErrorType.UNMATCHED_COMMENT
            #    break

            

            if next_state == Common.ERROR_DETECTED:
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

            if next_state.id == 13:
                self.comment_opened = False

            #print("------", curr_state.id, next_ch_type, next_state.id)

            if next_state is None:
                # error state
                pass

            #if curr_state.id == 17 and next_state.id != 18:
            #    self.has_error = True
            #    found_token = self.reader.string_read
            #    token_type = ErrorType.UNMATCHED_COMMENT
            #    break

            #print("++++++++++ next state:", next_state.id)
            if next_state.is_final:
                #print("here", next_state.id)
                if next_state.has_star:
                    #print("decreasing", next_state.id)
                    self.reader.decrease_pointer()
                    self.has_decreseaed = True

                    found_token = self.reader.string_read[:-1]
                    token_type = next_state.token_type

                    if next_state.id == 4:
                        all_keys_ids.append(found_token)

                    break
                else:
                    #print("22222", next_state.id)
                    found_token = self.reader.string_read
                    token_type = next_state.token_type
                    break
            else:
                curr_state = next_state

            

        
        
        if next_ch == CharType.EOF:
            return 'found_token', 'token_type', 'next_ch', 'next_ch_type', all_tokens, all_errors, all_keys_ids

        #print("------------", found_token, token_type)

        #if token_type == TokenType.ERROR:
        #    all_errors.append((self.line_num, found_token, 'ERROR'))

        if self.has_error:
            all_errors.append((self.line_num, found_token, token_type.value))


         
#and curr_state.id != 1
        if token_type != TokenType.WHITESPACE and token_type != TokenType.COMMENT and not self.has_error:
        #token_type != TokenType.ERROR:
            all_tokens.append((self.line_num, token_type.value, found_token))

        self.has_error = False 

        #print("****", found_token, token_type)
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

        while True:
            curr_state = self.dfa.start_state
            next_token, next_token_type, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids = self.get_next_token(curr_state, next_ch, next_ch_type, all_tokens, all_errors, all_keys_ids)
            self.reader.reset_pointers(self.has_decreseaed)
            print("^^^^^^^^^", all_tokens)
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

        

