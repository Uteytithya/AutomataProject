class DFA:
    
    # q = set of state, x = set of symbols, delta is transition function where theta(q, x) = new q, q0 = start state, f is final state
    def __init__(self, q, x, delta, q0, f):
        self.q =q 
        self.x =x 
        self.delta = delta 
        self.q0 = q0
        self.f = f 
    def __repr__(self):
        return f"DFA({self.q},\n\t{self.x},\n\t{self.delta}.\n\t{self.q0},\n\t{self.f})"
    def run(self,word):
        q = self.q0
        while word!="":
            q = self.delta[(q,word[0])]
            word = word[1:] # performing string slicing accepting index from 1 to the last index
        return q in self.f


DFA0 = DFA({0,1,2},
           {"a","b"}, 
            {(0,"a"):0, (0,"b"):1, 
             (1,"a"):2, (1,"b"):1, 
             (2,"a"):2, (2,"b"):2 },
            0,
            {0,1})
print(DFA0.run("ba"))

# print(repr(DFA0))