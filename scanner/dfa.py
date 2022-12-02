from statics import *


class State:
    def __init__(self, id, is_final=False, has_star=False):
        super(State)
        self.id = id
        self.is_final = is_final
        self.has_star = has_star
        self.transitions = {}

        # if this is a final state, self.token is the token it represents, else it is None
        self.token_type = None

    def add_transition(self, action, dest_s):
        self.transitions[action] = dest_s

    def get_next_state(self, action):
        return self.transitions[action]


class DFA:
    def __init__(self, n):
        self.states = []
        for i in range(n):
            if i in Common.FINAL_STATES:
                if i in Common.STAR_STATES:
                    self.states.append(State(i, is_final=True, has_star=True))
                else:
                    self.states.append(State(i, is_final=True))
            else:
                self.states.append(State(i))
        self.start_state = self.states[0]

    def define_dfa(self):
        # subgraph for defining KEYWORD

        #state0
        self.start_state.add_transition(CharType.DIGIT, self.states[1])
        self.start_state.add_transition(CharType.LETTER, self.states[3])
        self.start_state.add_transition(CharType.WHITESPACE, self.states[5])
        self.start_state.add_transition(CharType.SINGLE_SYMBOL, self.states[6])
        self.start_state.add_transition(CharType.EQUAL, self.states[7])
        self.start_state.add_transition(CharType.SLASH, self.states[10])
        self.start_state.add_transition(CharType.STAR, self.states[17])

        #state1
        self.states[1].add_transition(CharType.DIGIT, self.states[1])
        self.states[1].add_transition(CharType.NOT_DIGIT_LETTER, self.states[2])

        #state3
        self.states[3].add_transition(CharType.LETTER, self.states[3])
        self.states[3].add_transition(CharType.DIGIT, self.states[3])
        self.states[3].add_transition(CharType.NOT_DIGIT_LETTER, self.states[4])

        #state7
        self.states[7].add_transition(CharType.EQUAL, self.states[8])
        self.states[7].add_transition(CharType.NEQUAL, self.states[9])

        #state10
        self.states[10].add_transition(CharType.STAR, self.states[11])
        self.states[10].add_transition(CharType.SLASH, self.states[14])
        self.states[10].add_transition(CharType.NSTAR_NSLASH, self.states[16])

        #state11
        self.states[11].add_transition(CharType.NSTAR, self.states[11])
        self.states[11].add_transition(CharType.STAR, self.states[12])

        #state12
        self.states[12].add_transition(CharType.NSTAR_NSLASH, self.states[11])
        self.states[12].add_transition(CharType.STAR, self.states[12])
        self.states[12].add_transition(CharType.SLASH, self.states[13])

        #state14
        self.states[14].add_transition(CharType.EOF_ENTER, self.states[15])

        #state17
        self.states[17].add_transition(CharType.NSLASH, self.states[18])



if __name__ == "__main__":
    dfa = DFA(Common.N_OF_STATES)
    dfa.define_dfa()
