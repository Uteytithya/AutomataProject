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
        if self.isDFA():
            self.type = "DFA"
        else:
            self.type = "NFA"

    def isDFA(self):
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
        return frozenset(closure)

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
                
                new_state = frozenset(new_state)
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unprocessed_states.append(new_state)
                
                dfa_delta[(current, symbol)] = new_state

        return FA(dfa_states, self.X, dfa_delta, dfa_start_state, dfa_accept_states)

    def minimize(self):
        if self.type != "DFA":
            raise ValueError("minimize method is only applicable for DFA")

        # Step 1: Split the states into two groups: final and non-final
        final_states = set()
        non_final_states = set()
        for state in self.Q:
            if state in self.F:
                final_states.add(state)
            else:
                non_final_states.add(state)

        # Step 2: Split the states into groups based on distinguishability
        distinguishable = True
        while distinguishable:
            distinguishable = False
            new_groups = []
            for group in [final_states, non_final_states]:
                if len(group) == 1:
                    new_groups.append(group)
                    continue

                new_group = set()
                for state in group:
                    if len(new_group) == 0:
                        new_group.add(state)
                    else:
                        for existing_state in new_group:
                            if self.areStatesDistinguishable(state, existing_state, final_states, non_final_states):
                                distinguishable = True
                                new_groups.append({state})
                                break
                        else:
                            new_group.add(state)
                new_groups.append(new_group)

            final_states = new_groups[0]
            non_final_states = new_groups[1]

        # Step 3: Create the new DFA
        new_states = final_states.union(non_final_states)
        new_delta = {}
        for state in new_states:
            for symbol in self.X:
                new_delta[(state, symbol)] = self.delta[(state, symbol)]

        new_start_state = None
        for state in new_states:
            if self.q0 in state:
                new_start_state = state
                break

        new_final_states = set()
        for state in new_states:
            if state & self.F:
                new_final_states.add(state)

        return FA(new_states, self.X, new_delta, new_start_state, new_final_states)
    
    def __repr__(self):
        states_str = ", ".join(str(state) for state in self.Q)
        transitions_str = ", ".join(f"{key[0]}, {key[1]} -> {value}" for key, value in self.delta.items())
        final_states_str = ", ".join(str(state) for state in self.F)
        return (f"FA:\n- State Set: ({states_str})\n"
                f"- Alphabet: ({', '.join(self.X)})\n"
                f"- Transition function: ({transitions_str})\n"
                f"- Start State: ({self.q0})\n"
                f"- Final State: ({final_states_str})\n"
                f"- FA Type: {self.type}")