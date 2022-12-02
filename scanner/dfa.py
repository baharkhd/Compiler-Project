class State:
    def __init__(self, id):
        self.id = id
        self.final = False

class DFA:
    def __init__(self):
        self.states = []
        self.transitions = {}

    def add_transition(self, source_s, action, dest_s):
        if self.transitions[source_s]:
            self.transitions[source_s][action] = dest_s
        else:
            self.transitions[source_s] = {action: dest_s}

    def define_dfa(self):
        pass

if __name__ == "__main__":
    dfa = DFA()
    dfa.define_dfa()