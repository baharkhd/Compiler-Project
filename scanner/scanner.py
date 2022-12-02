from writer import *
from reader import *

def validate_char(char):
    pass

def get_next_token(file, line_num):
    detemined_tok = ''

    next_char = file.read(1)
    validate_char(next_char)



def run_scanner():
    line_num = 1

    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as file:

        while True:
            token = get_next_token(file, line_num)
            print(token)

            if not token:
                print('Reached end of file')
                break