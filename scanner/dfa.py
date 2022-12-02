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
    def __init__(self, n):
        self.states = []
        for i in range(n):
            if i in Common.FINAL_STATES:
                self.states.append(State(i, is_final=True))
            else:
                self.states.append(State(i))
        self.start_state = self.states[0]

    def define_dfa(self):
        # subgraph for defining KEYWORD
        self.start_state.add_transition(Transitions.DIGIT, self.states[1])
        self.start_state.add_transition(Transitions.LETTER, self.states[3])
        self.start_state.add_transition(Transitions.LETTER, self.states[3])


if __name__ == "__main__":
    dfa = DFA(Common.N_OF_STATES)
    dfa.define_dfa()
