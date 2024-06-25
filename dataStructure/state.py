class State():
    def __init__(self, name, transitions):
        self.name = name
        self.transitions = transitions # list of Transition objects
    def __repr__(self):
        return f"{self.name}: {self.transitions} "
class Transition:
    def __init__(self, symbol, to):
        self.symbol = symbol
        self.to = to
    def __repr__(self):
        return f"{self.symbol} -> {self.to}"

# q0 = State(0, [Transition("a", 1), Transition("b", 0)])
# # print(q0)