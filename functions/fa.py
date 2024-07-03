from dataStructure import state

class FA:
    # Q = set of State objects, X = set of symbols, delta = transition dictionary { (State, symbol) : State }
    # q0 = start state (State object), F = set of final states (set of State objects)
    def __init__(self, Q, X, delta, q0, F):
        self.Q = Q 
        self.X = X
        self.delta = delta 
        self.q0 = q0
        self.F = F
        self.type = None
        # Check condition if FA is DFA or NFA
        if self.isDFA():
            self.type = "DFA"
        # False = FA type = NFA
        else:
            self.type = "NFA"
    
    # Check if the FA is a DFA
    def isDFA(self):
        # Check if the FA contains only one start state
        count = 0
        for q in self.Q:
            if q == self.q0:
                count += 1
        if count != 1:
            return False
        # Check if the transition function is total
        seenTransitions = set()
        for q in self.Q:
            for x in self.X:
                if (q, x) not in self.delta:
                    return False
                elif self.delta[(q, x)] not in self.Q:
                    return False
                elif (q, x) in seenTransitions:
                    return False
                else:
                    seenTransitions.add((q, x))
        return True
    
    # Epsilon Closure functions using for converting NFA to DFA
    def epsilonClosures(self, state):
        if self.type != "NFA":
            raise ValueError("epsilonClosures method is only applicable for NFA")

        closure = set() 
        unprocessedStates = [state]
        while unprocessedStates:
            current = unprocessedStates.pop()
            closure.add(current)
            if (current, "") in self.delta:
                for q in self.delta[(current, "")]:
                    if q not in closure:
                        unprocessedStates.append(q)
        return closure

    def convertNFAtoDFA(self):
        if self.type != "NFA":
            raise ValueError("convertNFAtoDFA method is only applicable for NFA")

        # Start with the epsilon closure of the NFA's start state
        initialState = self.epsilonClosures(self.q0)
        dfa_states = {initialState}
        unprocessed_states = [initialState]
        dfa_delta = {}
        dfa_start_state = initialState
        dfa_accept_states = set()

        while unprocessed_states:
            current = unprocessed_states.pop()
            
            # If any NFA state in the current DFA state is an accept state, mark this DFA state as an accept state
            if any(state in self.F for state in current):
                dfa_accept_states.add(current)

            # Process each input symbol (excluding epsilon)
            for symbol in self.X:
                if symbol == "":
                    continue
                
                new_state = set()
                for state in current:
                    if (state, symbol) in self.delta:
                        for target in self.delta[(state, symbol)]:
                            new_state.update(self.epsilonClosures(target))
                
                new_state = new_state
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unprocessed_states.append(new_state)
                
                dfa_delta[(tuple(current), symbol)] = new_state

        return FA(dfa_states, self.X, dfa_delta, dfa_start_state, dfa_accept_states)

    def minimize(self):
        if self.type != "DFA":
            raise ValueError("minimize method is only applicable for DFA")

        # Step 1: Initialize the partitions
        P = {self.F, self.Q - self.F}
        W = {self.F} if len(self.F) < len(self.Q - self.F) else {self.Q - self.F}

        # Step 2: Process the partitions in W
        while W:
            A = W.pop()
            for c in self.X:
                # Find the set of states that transitions on c into A
                X = set()
                for q in self.Q:
                    if self.delta.get((q, c)) in A:
                        X.add(q)
                
                # Split each set in P based on its intersection with X
                new_P = set()
                for Y in P:
                    Y1 = Y.intersection(X)
                    Y2 = Y - X
                    if Y1 and Y2:
                        new_P.add(Y1)
                        new_P.add(Y2)
                        if Y in W:
                            W.remove(Y)
                            W.add(Y1)
                            W.add(Y2)
                        else:
                            if len(Y1) <= len(Y2):
                                W.add(Y1)
                            else:
                                W.add(Y2)
                    else:
                        new_P.add(Y)
                P = new_P
        
        # Step 3: Create the new DFA
        new_states = {tuple(Y) for Y in P}
        state_map = {state: tuple(state) for state in self.Q}

        new_delta = {}
        for state in new_states:
            representative = next(iter(state))
            for symbol in self.X:
                target_state = self.delta.get((representative, symbol))
                if target_state is not None:
                    new_delta[(state, symbol)] = state_map[target_state]

        new_start_state = next(s for s in new_states if self.q0 in s)
        new_final_states = {state for state in new_states if set(state) & self.F}

        return FA(new_states, self.X, new_delta, new_start_state, new_final_states)
    
    def complement(self):
        if self.type != "DFA":
            raise ValueError("complement method is only applicable for DFA")

        new_final_states = self.Q - self.F
        return FA(self.Q, self.X, self.delta, self.q0, new_final_states)
    
    def testString(self, word):
        if self.type == "DFA":
            q = self.q0
            while word != "":
                if (q, word[0]) not in self.delta:
                    return False
                q = self.delta[(q, word[0])]
                word = word[1:]  # performing string slicing accepting index from 1 to the last index
            return q in self.F
        else:
            raise ValueError("testString method is only applicable for DFA")
            
    def union(self, fa2):
        # Union of two FA
        if self.X != fa2.X:
            raise ValueError("Alphabets of the two FAs are not the same")
        new_states = self.Q.union(fa2.Q)
        new_delta = self.delta.copy()
        new_delta.update(fa2.delta)
        new_start_state = state("q0")
        new_final_states = self.F.union(fa2.F)
        return FA(new_states, self.X, new_delta, new_start_state, new_final_states)
    
    def intersection(self, fa2):
        # Intersection of two FA
        if self.X != fa2.X:
            raise ValueError("Alphabets of the two FAs are not the same")
        new_states = self.Q.intersection(fa2.Q)
        new_delta = {key: value for key, value in self.delta.items() if key in new_states}
        new_delta.update({key: value for key, value in fa2.delta.items() if key in new_states})
        new_start_state = state("q0")
        new_final_states = self.F.intersection(fa2.F)
        return FA(new_states, self.X, new_delta, new_start_state, new_final_states)
    
    def wordGenerator(self, length):
        if self.type == "DFA":
            def generateWords(length, currentWord, currentState):
                if length == 0:
                    if currentState in self.F:
                        return [currentWord]
                    else:
                        return []
                words = []
                for symbol in self.X:
                    if (currentState, symbol) in self.delta:
                        nextState = self.delta[(currentState, symbol)]
                        words.extend(generateWords(length - 1, currentWord + symbol, nextState))
                return words

            return generateWords(length, "", self.q0)
        else:
            raise ValueError("wordGenerator method is only applicable for DFA")
    
    # Make it into a table    
    def __repr__(self):
        # Determine the width of the columns
        max_state_len = max(len(str(state)) for state in self.Q)
        max_symbol_len = max(len(symbol) for symbol in self.X)
        cell_width = max(max_state_len, max_symbol_len) + 2
        
        # Create the header row
        header = " " * (cell_width + 5) + " | ".join(f"{symbol:^{cell_width}}" for symbol in self.X)
        
        # Sort the states for orderly output
        sorted_states = sorted(self.Q, key=lambda s: str(s))

        # Create the rows for the state transitions
        rows = []
        for state in sorted_states:
            if state == self.q0:
                state_indicator = "→"
            elif state in self.F:
                state_indicator = "*"
            else:
                state_indicator = " "
            row = f"{state_indicator} {state:^{cell_width}}"
            for symbol in self.X:
                next_state = self.delta.get((state, symbol), "-")
                row += f" | {next_state:^{cell_width}}"
            rows.append(row)
        
        # Join the header and rows
        table = header + "\n" + "\n".join(rows)
        
        return f"Transition Table:\n{table}\nFA Type: {self.type}"