from parser_module import Parser
import json

'''
NAME: DORNA DEHGHANI
ID: 97105939
'''


# TODO: put this in Reader class
def read_json(path='table.json'):
    f = open('table.json')
    data = json.load(f)
    f.close()
    return data


def run_compiler():
    json_data = read_json('table.json')
    parser = Parser(json_data)
    parser.run_parser()


if __name__ == "__main__":
    run_compiler()
