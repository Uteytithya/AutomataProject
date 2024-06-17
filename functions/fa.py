class FA:
    def __init__(self, Q, X, delta, q0, F):
        self.Q = Q 
        self.X = X
        self.delta = delta 
        self.q0 = q0
        self.F = F
        self.type = None
        if self.isDFA():
            self.type = "DFA"
        else:
            self.type = "NFA"
    def isDFA(self):
        seenTransitions = set()
        for q in self.Q:
            for x in self.X:
                if (q,x) not in self.delta:
                    return False
                elif self.delta[(q,x)] not in self.Q:
                    return False
                elif (q,x) in seenTransitions:
                    return False
                else:
                    seenTransitions.add((q,x))
        return True
    def testString(self, word):
        if type == "DFA":
            q = self.q0
        while word!="":
            q = self.delta[(q,word[0])]
            word = word[1:] # performing string slicing accepting index from 1 to the last index
        return q in self.f
    def convertNFAtoDFA(self):
        if self.type == "NFA":
            pass
        else:
            return "This is not a NFA"
        
    def minimize(self):
        pass
    def __repr__(self):
        return f"DFA:\n- State Set : {self.Q},\n- Alphabet: {self.X},\n- Transition function: {self.delta}.\n- Start State: {self.q0},\n- Final State: {self.F},\n- FA Type: {self.type})"
    
DFA0 = FA({0,1,2},
           {"a","b"}, 
            {(0,"a"):0, (0,"b"):1, 
             (1,"a"):2, 
             (2,"a"):2, (2,"b"):2 },
            {0},
            {0,1})
print(DFA0)
# a = {(0,1): 4, (2,3): 5}
# for value in a.values():
#     print(value)