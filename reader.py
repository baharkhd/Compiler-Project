from statics import *
import re
import json


class Reader:
    def __init__(self):
        self.input_file = open(INPUT_FILE_PATH)

        self.start_pointer = 0
        self.end_pointer = 0

        self.string_read = ''

    def decrease_pointer(self):
        self.end_pointer -= 1

    def increase_end_pointer(self):
        self.end_pointer += 1

    def decrease_end_pointer(self):
        self.end_pointer -= 1

    def reset_pointers(self, has_decreased=False):
        self.start_pointer = self.end_pointer
        if has_decreased:
            self.string_read = self.string_read[-1]
        else:
            self.string_read = ''

    def get_char_type(self, char):
        if re.match(CharType.DIGIT.value, char):
            return CharType.DIGIT
        elif re.match(CharType.LETTER.value, char):
            return CharType.LETTER
        elif char == '\n':
            return CharType.ENTER
        elif re.match(CharType.WHITESPACE.value, char):
            return CharType.WHITESPACE
        elif re.match(CharType.SINGLE_SYMBOL.value, char):
            return CharType.SINGLE_SYMBOL
        elif char == '=':
            return CharType.EQUAL
        elif char == '*':
            return CharType.STAR
        elif char == '/':
            return CharType.SLASH
        else:
            return CharType.INVALID

    def get_next_char(self):
        ch = self.input_file.read(1)
        self.end_pointer += 1
        self.string_read += ch
        return ch, self.get_char_type(ch)

    def read_input_code(self):
        f = open(INPUT_FILE_PATH, "r")
        return f.read()

    def read_input_file(self):
        with open(INPUT_FILE_PATH) as file:
            while True:
                next_char = file.read(1)
                if not next_char:
                    break
                self.string_read += next_char

    def read_json(path='table.json'):
        f = open('table.json')
        data = json.load(f)
        f.close()
        return data