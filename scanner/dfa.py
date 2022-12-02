from statics import *

class State:
    def __init__(self, id, is_final=False, has_star=False):
        self.id = id
        self.final = is_final
        self.transitions = {}

        # if this is a final state, self.token is the token it represents, else it is None
        self.token = None

    def add_transition(self, action, dest_s):
        self.transitions[action] = dest_s

    def give_next_state(self, action):
        return self.transitions[action]

class DFA:
    def __init__(self):
        self.states = []
        self.start_state = State(0)

    

    def define_dfa(self):

        #subgraph for defining KEYWORD
        self.start_state.add_transition(Transitions.DIGIT, ...)
        

if __name__ == "__main__":
    dfa = DFA()
    dfa.define_dfa()