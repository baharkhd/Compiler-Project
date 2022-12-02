from statics import *


class Reader:
    def __init__(self):
        self.input_file = open(INPUT_FILE_PATH)

        self.start_pointer = 0
        self.end_pointer = 0

        self.read_string = ''

    def get_next_char(self):
        ch = self.input_file.read(1)
        self.end_pointer += 1
        self.read_string += ch
        return self.input_file.read(1)

    def read_input_file(self):
        with open(INPUT_FILE_PATH) as file:
            while True:
                next_char = file.read(1)
                if not next_char:
                    break
                self.read_string += next_char

            print(self.read_string)


if __name__ == "__main__":
    reader = Reader()
    reader.read_input_file()
