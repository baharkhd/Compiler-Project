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
        self.invalid_char = False
        self.unclosed_comment = False
        self.start_comment_line = 1

        self.start = True

    def check_EOF(self):
        if self.reader.end_pointer >= len(self.text):
            return True
        else:
            return False

    def check_next_line(self, char):
        if char == '\n':
            self.line_num += 1

    def get_next_token(self):
        token_line_n = self.line_num
        token = ''
        token_type = ''

        errors = []
        tokens = []
        key_ids = []

        while True:
            #print("here?", self.reader.end_pointer, len(self.text))
            #print("?????", self.reader.end_pointer)
            if self.check_EOF():
                #print("%%%%%%", self.reader.start_pointer, self.reader.end_pointer)
                if self.reader.start_pointer != self.reader.end_pointer:
                    self.end_of_file = True
                    curr_char = '\n'
                    char_type = CharType.ENTER
                #else:
                #    break

                break
            else:
                
                #print("---", self.reader.end_pointer, self.text[self.reader.end_pointer])
                #print(self.reader.end_pointer)

                #if self.reader.end_pointer >= len(self.text):
                #    print("??????")
                #    self.unclosed_commend = True
                #    break
                curr_char = self.text[self.reader.end_pointer]
                
                
                char_type = self.reader.get_char_type(curr_char)
                #print(curr_char, self.reader.end_pointer)

            if char_type == CharType.INVALID:
                self.invalid_char = False
                #print("(()()()()()()()()", curr_char, self.curr_state.id)
                
                if self.curr_state.id == 14 or self.curr_state.id == 11 or self.curr_state.id == 12:
                    #print("vaaaaaa?", self.invalid_char)
                    self.reader.increase_end_pointer()
                    self.check_next_line(curr_char)
                    continue
                else:
                    #print("allaho akbar")
                    self.invalid_char = True
                    token = self.text[self.reader.start_pointer:self.reader.end_pointer + 1]
                    token_type = ErrorType.INVALID_INPUT
                    token_line_n = self.line_num
                    self.reader.start_pointer = self.reader.end_pointer
                    self.reader.increase_end_pointer()
                    self.reader.start_pointer += 1

                    errors.append((self.line_num, token, token_type.value))
                    self.has_error = True
                    #self.check_next_line(curr_char)
                    break
                

            next_state = self.curr_state.get_next_state(char_type)
            #if isinstance(next_state, State):
            #    print(curr_char, self.curr_state.id, next_state.id, char_type)
                #print("next_state.id:", next_state.id, curr_char)
            self.reader.increase_end_pointer()

            if isinstance(next_state, State):
                if self.curr_state.id == 10 and next_state.id == 11:
                    self.start_comment_line = self.line_num

            if (self.curr_state.id == 11 or self.curr_state.id == 12) and next_state.id != 13:
                #print("1.here", self.reader.end_pointer)
                #self.reader.increase_end_pointer()
                self.check_next_line(curr_char)
                self.curr_state = next_state
                #print("2.here", self.reader.end_pointer)
                continue

            if curr_char == '\n':
                self.line_num += 1

            if next_state == Common.ERROR_DETECTED:
                if self.curr_state.id == 17:
                    self.curr_state = self.dfa.start_state

                    # Here we handle Unmatched comment
                    token = self.text[self.reader.start_pointer:self.reader.end_pointer]
                    token_type = ErrorType.UNMATCHED_COMMENT

                    errors.append((self.line_num, token, token_type.value))

                    self.reader.start_pointer = self.reader.end_pointer
                    
                elif self.curr_state.id == 14 or self.curr_state.id == 11 or self.curr_state.id == 12:
                    self.check_next_line(curr_char)
                    pass
                else:
                    self.curr_state = self.dfa.start_state

                    # Here we handle Invalid Number
                    token = self.text[self.reader.start_pointer:self.reader.end_pointer]
                    token_type = ErrorType.INVALID_NUMBER

                    errors.append((self.line_num, token, token_type.value))
                    self.reader.start_pointer = self.reader.end_pointer

            else:
                
                #print("1.-----", next_state.id)
                if next_state.is_final:
                    #print("2.-----", next_state.id)
                    if next_state.has_star:
                        #print("3.-----")
                        if curr_char == '\n':
                            self.line_num -= 1

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
                        #print("-------------", next_state.id)
                        token = self.text[self.reader.start_pointer:self.reader.end_pointer]
                        token_type = next_state.token_type
                        token_line_n = self.line_num
                        self.reader.start_pointer = self.reader.end_pointer
                        break

                self.curr_state = next_state

        #if self.unclosed_commend:
        #    errors.append((self.line_num, self.text[self.reader.start_pointer:self.reader.end_pointer][:7] + '...', ErrorType.UNCLOSED_COMMENT.value))
        #    return None, errors, key_ids
        if self.check_EOF():
            #print("-----")
            if not next_state.id == 13 and (self.curr_state.id == 11 or self.curr_state.id == 12):
                #print("----")
                errors.append((self.start_comment_line, self.text[self.reader.start_pointer:self.reader.end_pointer][:7] + '...', ErrorType.UNCLOSED_COMMENT.value))
                return None, errors, key_ids

        if self.has_error:
            self.has_error = False
            return None, errors, key_ids
        else:
            if not token_type:
                if self.invalid_char:
                    self.invalid_char = False
                    return None, errors, key_ids
                self.invalid_char = False

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
        self.text = self.reader.read_input_code()

        all_tokens = []
        all_errors = []
        all_keys_ids = []

        
        while True:
            #print("====")
            self.curr_state = self.dfa.start_state
            token, errors, keys_ids = self.get_next_token()
            if token and token[1] != TokenType.WHITESPACE.value and token[1] != TokenType.COMMENT.value:
                all_tokens.append(token)

            all_errors.extend(errors)
            all_keys_ids.extend(keys_ids)

            #print("-----", self.reader.end_pointer, len(self.text))
            if self.check_EOF():
                break


        
        tokens_dict = self.handle_all_tokens(all_tokens)
        errors_dict = self.handle_all_errors(all_errors)
        all_keys_ids = list(set(all_keys_ids))

        self.writer.write_tokens(tokens_dict)
        self.writer.write_errors(errors_dict)
        self.writer.write_symbols(all_keys_ids)

        return all_tokens

        

        

