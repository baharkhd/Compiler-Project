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
        if action in self.transitions.keys():
            return self.transitions[action]
        else:
            return Common.ERROR_DETECTED


class DFA:
    def __init__(self, n):
        self.states = []
        for i in range(n):
            if i in Common.FINAL_STATES.value:
                if i in Common.STAR_STATES.value:
                    self.states.append(State(i, is_final=True, has_star=True))
                else:
                    self.states.append(State(i, is_final=True))
            else:
                self.states.append(State(i))
        self.start_state = self.states[0]

        # Todo: Check if separating ENTER and WHITESPACE makes any problems
        self.states[2].token_type = TokenType.NUM
        self.states[4].token_type = TokenType.KEYWORD_ID
        self.states[5].token_type = TokenType.WHITESPACE
        self.states[6].token_type = TokenType.SYMBOL
        self.states[8].token_type = TokenType.SYMBOL
        self.states[9].token_type = TokenType.SYMBOL
        self.states[13].token_type = TokenType.COMMENT
        self.states[15].token_type = TokenType.COMMENT
        self.states[16].token_type = TokenType.SYMBOL
        self.states[18].token_type = TokenType.SYMBOL

    def define_dfa(self):
        self.start_state.add_transition(CharType.DIGIT, self.states[1])
        self.start_state.add_transition(CharType.LETTER, self.states[3])
        self.start_state.add_transition(CharType.WHITESPACE, self.states[5])
        self.start_state.add_transition(CharType.ENTER, self.states[5])
        self.start_state.add_transition(CharType.SINGLE_SYMBOL, self.states[6])
        self.start_state.add_transition(CharType.EQUAL, self.states[7])
        self.start_state.add_transition(CharType.SLASH, self.states[10])
        self.start_state.add_transition(CharType.STAR, self.states[17])

        # state1
        self.states[1].add_transition(CharType.DIGIT, self.states[1])
        self.states[1].add_transition(CharType.WHITESPACE, self.states[2])
        self.states[1].add_transition(CharType.ENTER, self.states[2])
        self.states[1].add_transition(CharType.SINGLE_SYMBOL, self.states[2])
        self.states[1].add_transition(CharType.EQUAL, self.states[2])
        self.states[1].add_transition(CharType.SLASH, self.states[2])
        self.states[1].add_transition(CharType.STAR, self.states[2])
        self.states[1].add_transition(CharType.EOF, self.states[2])

        # state3
        self.states[3].add_transition(CharType.LETTER, self.states[3])
        self.states[3].add_transition(CharType.DIGIT, self.states[3])
        self.states[3].add_transition(CharType.WHITESPACE, self.states[4])
        self.states[3].add_transition(CharType.ENTER, self.states[4])
        self.states[3].add_transition(CharType.SINGLE_SYMBOL, self.states[4])
        self.states[3].add_transition(CharType.EQUAL, self.states[4])
        self.states[3].add_transition(CharType.SLASH, self.states[4])
        self.states[3].add_transition(CharType.STAR, self.states[4])
        self.states[3].add_transition(CharType.EOF, self.states[4])

        # state7
        self.states[7].add_transition(CharType.EQUAL, self.states[8])
        self.states[7].add_transition(CharType.LETTER, self.states[9])
        self.states[7].add_transition(CharType.DIGIT, self.states[9])
        self.states[7].add_transition(CharType.WHITESPACE, self.states[9])
        self.states[7].add_transition(CharType.ENTER, self.states[9])
        self.states[7].add_transition(CharType.SINGLE_SYMBOL, self.states[9])
        self.states[7].add_transition(CharType.SLASH, self.states[9])
        self.states[7].add_transition(CharType.STAR, self.states[9])

        # state10
        self.states[10].add_transition(CharType.STAR, self.states[11])
        self.states[10].add_transition(CharType.SLASH, self.states[14])
        self.states[10].add_transition(CharType.EQUAL, self.states[16])
        self.states[10].add_transition(CharType.LETTER, self.states[16])
        self.states[10].add_transition(CharType.DIGIT, self.states[16])
        self.states[10].add_transition(CharType.WHITESPACE, self.states[16])
        self.states[10].add_transition(CharType.ENTER, self.states[16])
        self.states[10].add_transition(CharType.SINGLE_SYMBOL, self.states[16])

        # state11
        self.states[11].add_transition(CharType.EQUAL, self.states[11])
        self.states[11].add_transition(CharType.LETTER, self.states[11])
        self.states[11].add_transition(CharType.DIGIT, self.states[11])
        self.states[11].add_transition(CharType.WHITESPACE, self.states[11])
        self.states[11].add_transition(CharType.ENTER, self.states[11])
        self.states[11].add_transition(CharType.SINGLE_SYMBOL, self.states[11])
        self.states[11].add_transition(CharType.SLASH, self.states[11])
        self.states[11].add_transition(CharType.STAR, self.states[12])

        # state12
        self.states[12].add_transition(CharType.EQUAL, self.states[11])
        self.states[12].add_transition(CharType.LETTER, self.states[11])
        self.states[12].add_transition(CharType.DIGIT, self.states[11])
        self.states[12].add_transition(CharType.ENTER, self.states[11])
        self.states[12].add_transition(CharType.WHITESPACE, self.states[11])
        self.states[12].add_transition(CharType.SINGLE_SYMBOL, self.states[11])
        self.states[12].add_transition(CharType.STAR, self.states[12])
        self.states[12].add_transition(CharType.SLASH, self.states[13])

        # state14
        self.states[14].add_transition(CharType.EOF, self.states[15])
        self.states[14].add_transition(CharType.ENTER, self.states[15])

        self.states[14].add_transition(CharType.LETTER, self.states[14])
        self.states[14].add_transition(CharType.DIGIT, self.states[14])
        self.states[14].add_transition(CharType.WHITESPACE, self.states[14])
        self.states[14].add_transition(CharType.SINGLE_SYMBOL, self.states[14])
        self.states[14].add_transition(CharType.STAR, self.states[14])
        self.states[14].add_transition(CharType.SLASH, self.states[14])
        self.states[14].add_transition(CharType.EQUAL, self.states[14])

        # state17
        self.states[17].add_transition(CharType.EQUAL, self.states[18])
        self.states[17].add_transition(CharType.LETTER, self.states[18])
        self.states[17].add_transition(CharType.DIGIT, self.states[18])
        self.states[17].add_transition(CharType.ENTER, self.states[18])
        self.states[17].add_transition(CharType.WHITESPACE, self.states[18])
        self.states[17].add_transition(CharType.SINGLE_SYMBOL, self.states[18])
        self.states[17].add_transition(CharType.STAR, self.states[18])
