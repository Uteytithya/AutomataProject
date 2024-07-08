from dataStructure import state

class FA:
    # Q = set of State objects, X = set of symbols, delta = transition dictionary { (State, symbol) : State }
    # q0 = start state (State object), F = set of final states (set of State objects)
    def __init__(self, Q, X, delta, q0, F):
        self.Q = Q 
        self.X = X
        self.delta = self.convert_delta(delta)
        self.q0 = q0
        self.F = F
        self.type = "DFA" if self.isDFA() else "NFA"
    

    def convert_delta(self, delta_list):
        delta_dict = {}
        for (start, symbol, end) in delta_list:
            if (start, symbol) not in delta_dict:
                delta_dict[(start, symbol)] = {end}
            else:
                delta_dict[(start, symbol)].add(end)
        return delta_dict

    def isDFA(self):
        for state in self.Q:
            for symbol in self.X:
                # Check if there's no transition for a symbol from a state
                if (state, symbol) not in self.delta:
                    continue
                # Check if there's more than one transition for a symbol from a state
                if len(self.delta[(state, symbol)]) > 1:
                    return False
        # Check for epsilon transitions
        for (state, symbol) in self.delta:
            if symbol == "":
                return False
        return True
    
    def epsilonClosures(self, state):
        # Initialize the closure with the state itself
        closure = set([state])
        stack = [state]

        while stack:
            current_state = stack.pop()
            # If there are epsilon transitions from the current state
            if (current_state, "") in self.delta:
                for next_state in self.delta[(current_state, "")]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def convertNFAtoDFA(self):
        if self.type != "NFA":
            raise ValueError("convertNFAtoDFA method is only applicable for NFA")

        # Start with the epsilon closure of the NFA's start state
        initialState = frozenset(self.epsilonClosures(self.q0))
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
                
                new_state = frozenset(new_state)  # Convert the new state to a frozenset
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unprocessed_states.append(new_state)
                
                dfa_delta[(tuple(current), symbol)] = new_state

        # Convert DFA components to the required format
        dfa_states_list = sorted({tuple(state) for state in dfa_states}, key=len)
        dfa_delta_list = sorted([(tuple(state), symbol, tuple(target)) for (state, symbol), target in dfa_delta.items()], key=lambda x: (len(x[0]), x[1], len(x[2])))
        dfa_accept_states_list = sorted({tuple(state) for state in dfa_accept_states}, key=len)

        return FA(dfa_states_list, self.X, dfa_delta_list, tuple(dfa_start_state), dfa_accept_states_list)

    def minimizeDFA(self):
        if self.type != "DFA":
            raise ValueError("minimizeDFA method is only applicable for DFA")

        # Step 1: Remove non-accessible states
        accessible_states = set()
        stack = [self.q0]
        while stack:
            state = stack.pop()
            if state not in accessible_states:
                accessible_states.add(state)
                for symbol in self.X:
                    if (state, symbol) in self.delta:
                        stack.extend(self.delta[(state, symbol)])
        accessible_states &= self.Q

        # Step 2: Mark distinguishable pairs of states
        distinguishable = set()
        for p in accessible_states:
            for q in accessible_states:
                if (p in self.F and q not in self.F) or (p not in self.F and q in self.F):
                    distinguishable.add((p, q))
                    distinguishable.add((q, p))

        while True:
            new_distinguishable = set()
            for p in accessible_states:
                for q in accessible_states:
                    if (p, q) not in distinguishable:
                        for symbol in self.X:
                            if (self.delta.get((p, symbol), {None}) - self.delta.get((q, symbol), {None})) or (self.delta.get((q, symbol), {None}) - self.delta.get((p, symbol), {None})):
                                if (self.delta.get((p, symbol), {None}).pop(), self.delta.get((q, symbol), {None}).pop()) in distinguishable or (self.delta.get((q, symbol), {None}).pop(), self.delta.get((p, symbol), {None}).pop()) in distinguishable:
                                    new_distinguishable.add((p, q))
                                    new_distinguishable.add((q, p))
            if not new_distinguishable:
                break
            distinguishable |= new_distinguishable

        # Step 3: Construct the minimized DFA
        equivalence_classes = {}
        for state in accessible_states:
            for cls in equivalence_classes.values():
                if all((state, other) not in distinguishable and (other, state) not in distinguishable for other in cls):
                    cls.add(state)
                    break
            else:
                equivalence_classes[state] = {state}

        minimized_states = set(frozenset(cls) for cls in equivalence_classes.values())
        minimized_start_state = next(cls for cls in minimized_states if self.q0 in cls)
        minimized_final_states = {cls for cls in minimized_states if cls & self.F}
        minimized_delta = {}

        for cls in minimized_states:
            representative = next(iter(cls))
            for symbol in self.X:
                if (representative, symbol) in self.delta:
                    target = next(iter(self.delta[(representative, symbol)]))
                    for target_cls in minimized_states:
                        if target in target_cls:
                            minimized_delta[(cls, symbol)] = target_cls
                            break

        # Convert minimized DFA components to the required format
        minimized_states_list = sorted({tuple(state) for state in minimized_states}, key=len)
        minimized_delta_list = sorted([(tuple(state), symbol, tuple(target)) for (state, symbol), target in minimized_delta.items()], key=lambda x: (len(x[0]), x[1], len(x[2])))
        minimized_final_states_list = sorted({tuple(state) for state in minimized_final_states}, key=len)

        return FA(minimized_states_list, self.X, minimized_delta_list, tuple(minimized_start_state), minimized_final_states_list)


    
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
        if not self.delta:
            return "No transitions available."

        # Determine the longest state name for formatting
        state_width = max(len(str(state)) for state in self.Q) + 2

        # Determine the width for each transition column based on the longest transition
        transition_width = max(
            (len(" ".join(str(s) for s in targets)) for targets in self.delta.values()),
            default=0  # Handle empty delta
        ) + 2

        # Header
        header = f"{'':<{state_width}} | " + " | ".join(f"{symbol:^{transition_width}}" for symbol in self.X) + " |"
        divider = "=" * len(header)

        # Rows
        rows = []
        for state in self.Q:
            state_str = " ".join(str(s) for s in state) if isinstance(state, tuple) else str(state)
            state_marker = "→" if state == self.q0 else " "
            state_marker = "*" + state_marker if state in self.F else " " + state_marker
            row = f"{state_marker} {state_str:^{state_width - 2}} |"
            for symbol in self.X:
                if (state, symbol) in self.delta:
                    target_states = " ".join(str(s) for s in self.delta[(state, symbol)])
                    row += f" {target_states:^{transition_width}} |"
                else:
                    row += f" {'-':^{transition_width}} |"
            rows.append(row)

        # FA type
        fa_type = f"FA Type: {self.type}"

        return f"Transition Table:\n{header}\n{divider}\n" + "\n".join(rows) + f"\n{fa_type}"





