from scanner_module import Scanner
from parser_module import Parser
import json 
# TODO: correct the imports in this file if wrong


# put this in Reader class
def read_json(path='table.json'):
    f = open('table.json')
    data = json.load(f)
    f.close()
    return data


def run_compiler():
    scanner = Scanner()
    all_tokens = scanner.run_scanner()
    
    #for t in all_tokens:
    #    print(t)

    json_data = read_json('table.json')
    parser = Parser(json_data)

    for k, v in parser.parse_table.items():
        print(k, ":", v)

    print("1.======================================================")

    for k, v in parser.grammar.items():
        print(k, ":", v)

    print("2.======================================================")   

    for tok in all_tokens:
        print(tok)

    print("3.======================================================") 

    
    parser.create_parse_tree(all_tokens)


if __name__ == "__main__":
    run_compiler()