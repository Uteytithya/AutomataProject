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
