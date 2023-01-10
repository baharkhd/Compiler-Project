from anytree import Node, RenderTree
import json
import re
from statics import *

#udo = Node("Udo")
#marc = Node("Marc", parent=udo)
#lian = Node("Lian", parent=marc)
#dan = Node("Dan", parent=udo)
#jet = Node("Jet", parent=dan)
#jan = Node("Jan", parent=dan)
#joe = Node("Joe", parent=dan)

# TODO: transfer this function to Writer class
def write_parse_tree(root_node, PATH='parse_tree.txt'):

    tree_lines = ''
    with open(PATH, "+w", encoding="utf-8") as file:
        for pre, fill, node in RenderTree(root_node):
            tree_lines += "%s%s" % (pre, node.name)
            if node.name != "$":
                tree_lines += '\n'

        file.write(tree_lines)

# TODO: transfer this function to Writer class
def write_errors(all_errors, PATH='syntax_errors.txt'):
    with open(PATH, "+w", encoding="utf-8") as file:
        for err in all_errors:
            file.write(err + "\n") 

class Parser:
    def __init__(self, json_data):
        self.parse_table = json_data['parse_table']
        self.grammar = json_data['grammar']
        self.first = json_data['first']
        self.follow = json_data['follow']
        self.terminals = json_data['terminals']
        self.non_terminals = json_data['non_terminals']
        self.token_pointer = 0
        self.stack = ['0']
        self.node_stack = []
        self.root_node = None
        self.line_num = 0
        self.all_tokens = []
        self.unexpected_EOF = False

        self.current_node = None
        self.all_errors = []


    def return_action(self, action):
        action_type = ActionType.REDUCE
        state = '0'

        if re.match(r'reduce_[0-9]+', action):
            action_type = ActionType.REDUCE
            state = action.split('_')[1]
        elif re.match(r'shift_[0-9]+', action):
            action_type = ActionType.SHIFT
            state = action.split('_')[1]

        return action_type, state


    def is_terminal(self, token):
        if token in self.terminals:
            return True
        return False

    def is_non_terminal(self, token):
        if token in self.non_terminals:
            return True
        return False

    def add_error(self, token, error_type: ParserErrorType):
        # TODO: here we should have a tuple as token
        print("----- adding error {} for {}".format(error_type.value, token))
        error = ''
        if error_type == ParserErrorType.ILLEGAL_ERROR:
            error = '#{} : syntax error, illegal {}'.format(self.line_num, token)
        elif error_type == ParserErrorType.INPUT_DISCARDED:
            error = '#{} : syntax error, discarded {} from input'.format(self.line_num, token)
        elif error_type == ParserErrorType.STACK_DISCARDED:
            error = 'syntax error, discarded {} from stack'.format(token)
        elif error_type == ParserErrorType.MISSING_ERROR:
            error = '#{} : syntax error, missing {}'.format(self.line_num, token)
        elif error_type == ParserErrorType.UNEXPECTED_EOF:
            error = '#{} : syntax error, Unexpected EOF'.format(self.line_num)
        
        self.all_errors.append(error)

    def has_goto(self, state):
        actions = self.parse_table[state].values()
        for action in actions:
            if re.match(r'goto_[0-9]+', action):
                return True

        return False

    def get_closest_valid_state(self):
        while len(self.stack):
            #print("???")
            curr_state = self.stack[-1]
            curr_token = self.stack[-2]

            #print("+++++" ,curr_token, curr_state)

            if self.has_goto(curr_state):
                self.choose_next_token(curr_state)
                break
            else:
                token_type = get_token_type(curr_token)
                self.add_error("({}, {})".format(token_type, curr_token), ParserErrorType.STACK_DISCARDED)
                self.stack.pop()
                self.stack.pop()

    def choose_next_token(self, state):
        goto_nonterms = []
        for k, v in self.parse_table[state].items():
            if re.match(r'goto_[0-9]+', v):
                goto_nonterms.append((k, v))
        
        # sorting non-terminals
        goto_nonterms = sorted(goto_nonterms, key=lambda tup: tup[0])

        while True:
            self.token_pointer += 1
            next_token_tuple = self.all_tokens[self.token_pointer]
            next_token_type = next_token_tuple[1]
            next_token = next_token_tuple[2]
            if next_token != '$':
                self.line_num = next_token_tuple[0]
            else:
                self.line_num += 1


            if next_token_type == TokenType.KEYWORD_ID.value and not next_token in tokens[TokenType.KEYWORD]:
                next_token = TokenType.ID.value
            elif next_token_type == TokenType.KEYWORD_ID.value:
                next_token_type = TokenType.KEYWORD.value
            elif next_token_type == TokenType.NUM.value:
                next_token = TokenType.NUM.value
                next_token_type = TokenType.NUM.value

            found_nt = False
            for (nt, goto) in goto_nonterms:
                if next_token in self.follow[nt]:
                    self.stack += [nt, goto.split('_')[1]]
                    self.add_error(nt, ParserErrorType.MISSING_ERROR)
                    found_nt = True
                    break

            if found_nt:
                break
            else:
                if next_token == '$':
                    self.add_error('$', ParserErrorType.UNEXPECTED_EOF)
                    self.unexpected_EOF = True
                    break
                else:
                    self.add_error(next_token_tuple[2], ParserErrorType.INPUT_DISCARDED)
            



    def create_parse_tree(self, all_tokens):
        self.all_tokens = all_tokens
        # tokens: (#: line_num, TOKEN_TYPE, token)
        while True:
            if self.unexpected_EOF:
                write_errors(self.all_errors)
                break
            print("****", self.stack)
            token_tuple = all_tokens[self.token_pointer]
            self.line_num = token_tuple[0]
            token_type = token_tuple[1]
            token = token_tuple[2]
            

            if token_type == TokenType.KEYWORD_ID.value and token in tokens[TokenType.KEYWORD]:
                token_type = TokenType.KEYWORD.value
            elif token_type == TokenType.KEYWORD_ID.value:
                token = TokenType.ID.value
                token_type = TokenType.ID.value
            elif token_type == TokenType.NUM.value:
                token = TokenType.NUM.value
                token_type = TokenType.NUM.value

            latest_state = self.stack[-1]
                
            print(token_tuple, token_type, token)

            if not token in self.parse_table[latest_state].keys():
                # illegal error
                self.add_error(token, ParserErrorType.ILLEGAL_ERROR)
                self.get_closest_valid_state()
                continue

            action = self.parse_table[latest_state][token]
            
            if action == 'accept':
                print("!!!!!!!!accepted\n\n")
                self.stack.pop()
                root_node = self.stack.pop()

                self.root_node = self.node_stack[0]
                self.node_stack[2].parent = self.root_node

                #print(self.root_node, self.node_stack[2])

                for pre, fill, node in RenderTree(self.root_node):
                    #print("+++", node)
                    print("%s%s" % (pre, node.name))

                if len(self.all_errors) != 0:
                    write_errors(self.all_errors)
                else:
                    write_errors(['There is no syntax error.'])

                write_parse_tree(self.root_node)
                break

            action_type, next_state = self.return_action(action)
            
            if action_type == ActionType.SHIFT:
                self.stack += [token, next_state]
                if token_tuple[2] != '$':
                    self.node_stack += [Node('({}, {})'.format(token_type, token_tuple[2])), '']
                else:
                    self.node_stack += [Node('$'), '']
                if not token == '$':
                    self.token_pointer += 1

            else:
                grammar_id = self.parse_table[latest_state][token].split('_')[1] # since it is goto_#
                next_gram = self.grammar[grammar_id]
                parent_token = next_gram[0]
                parent_node = Node(parent_token)

                is_epsilon = next_gram[2] == 'epsilon'

                if not is_epsilon:
                    right_tokens_num = len(next_gram) - 2
                else:
                    right_tokens_num = 0
                    epsilon_node = Node('epsilon', parent=parent_node)

                    print("Children:", right_tokens_num)
                    print('epsilon')

                print("Parent:", parent_token)
                print("Children:", right_tokens_num)

                
                popped_nodes = []
                for i in range(2 * right_tokens_num):
                    popped = self.stack.pop()
                    popped_node = self.node_stack.pop()
                    if i % 2 != 0:
                        print(popped)
                        popped_nodes.append(popped_node)
                print()

                popped_nodes.reverse()
                for pn in popped_nodes:
                    pn.parent = parent_node

                latest_state = self.stack[-1]
                print("++++", latest_state, parent_token)
                next_goto = self.parse_table[latest_state][parent_token].split("_")[1]
                self.stack += [parent_token, next_goto]
                self.node_stack += [parent_node, '']

                

def read_json(path='table.json'):
    f = open('table.json')
    data = json.load(f)
    f.close()

    return data


if __name__ == "__main__":



    test_json_data = make_test_json_data()
    json_data = read_json('table.json')
    parser = Parser(test_json_data)
    

    tokens = ['int', '*', 'int', '$']
    parser.create_parse_tree(tokens)

    #for k, v in parser.grammar.items():
    #    print(k, ":", v)

    #print()
    
    #for k, v in parser.parse_table.items():
    #    print(k, ":", v)


