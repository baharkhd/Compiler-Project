from parser_module import Parser
import json
from writer import *
from reader import *

'''
NAME: Bahar Khodabakhshian
ID: 97105906
'''


def run_compiler():
    reader = Reader()
    writer = Writer()
    
    json_data = reader.read_json('table.json')
    parser = Parser(json_data, reader, writer)
    parser.run_parser()


if __name__ == "__main__":
    run_compiler()
