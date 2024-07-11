from collections import deque

class FA:
    # Q = set of State objects, X = set of symbols, delta = transition dictionary { (State, symbol) : State }
    # q0 = start state (State object), F = set of final states (set of State objects)
    def __init__(self, Q, X, delta, q0, F):
        self.Q = Q
        self.X = X
        self.delta = self.convert_delta(delta)
        self.q0 = q0
        self.F = F
        if self.isDFA():
            self.type = "DFA"
        else:
            self.type = "NFA"

    def convert_delta(self, delta_list):
        delta_dict = {}
        for (start, symbol, end) in delta_list:
            start = frozenset(start) if isinstance(start, list) else start
            end = frozenset(end) if isinstance(end, list) else end
            delta_dict[(start, symbol)] = end
        return delta_dict

    def state_to_string(self, state):
        if isinstance(state, (frozenset, set, list, tuple)):
            return ",".join(sorted(map(str, state)))
        return str(state)

    def isDFA(self):
        transition_counts = {}
        for (state, symbol), targets in self.delta.items():
            if symbol == "":
                return False  # DFA should not have epsilon transitions
            if (state, symbol) in transition_counts:
                return False  # Multiple transitions for a single symbol
            transition_counts[(state, symbol)] = targets

        for state in self.Q:
            for symbol in self.X:
                if (state, symbol) not in self.delta:
                    return False  # DFA should have a transition for every symbol in its alphabet

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

        initialState = frozenset(self.epsilonClosures(self.q0))
        dfa_states = {initialState}
        unprocessed_states = [initialState]
        dfa_delta = {}
        dfa_start_state = initialState
        dfa_accept_states = set()

        while unprocessed_states:
            current = unprocessed_states.pop()
            if any(state in self.F for state in current):
                dfa_accept_states.add(current)
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
                dfa_delta[(tuple(current), symbol)] = new_state

        dfa_states_list = sorted({tuple(state) for state in dfa_states}, key=len)
        dfa_delta_list = sorted([(tuple(state), symbol, tuple(target)) for (state, symbol), target in dfa_delta.items()], key=lambda x: (len(x[0]), x[1], len(x[2])))
        dfa_accept_states_list = sorted({tuple(state) for state in dfa_accept_states}, key=len)

        return FA(dfa_states_list, self.X, dfa_delta_list, tuple(dfa_start_state), dfa_accept_states_list)

    def minimize(self):
        P = {frozenset(self.F), frozenset(self.Q - self.F)}
        W = [frozenset(self.F)] if len(frozenset(self.F)) <= len(frozenset(self.Q - self.F)) else [frozenset(self.Q - self.F)]

        while W:
            A = W.pop()
            for c in self.X:
                X = frozenset({q for q in self.Q if (q, c) in self.delta and self.delta[(q, c)] in A})
                new_P = set()
                for Y in P:
                    intersection = X & Y
                    difference = Y - X
                    if intersection and difference:
                        new_P.add(intersection)
                        new_P.add(difference)
                        if Y in W:
                            W.remove(Y)
                            W.append(intersection)
                            W.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                W.append(intersection)
                            else:
                                W.append(difference)
                    else:
                        new_P.add(Y)
                P = new_P

        # Create new state names with old states included
        new_states = {state: f"S{index}({','.join(map(str, state))})" for index, state in enumerate(P)}
        state_mapping = {q: new_states[state] for state in new_states for q in state}

        # Create new delta function
        new_delta = {}
        for (start, symbol), end in self.delta.items():
            new_start = state_mapping[start]
            new_end = state_mapping[end]
            new_delta[(new_start, symbol)] = new_end

        # Update initial state and final states
        new_q0 = state_mapping[self.q0] if self.q0 in state_mapping else None
        new_F = {state_mapping[f] for f in self.F if f in state_mapping}

        # Update DFA components
        self.Q = set(new_states.values())
        self.delta = new_delta
        self.q0 = new_q0
        self.F = new_F

    def complement(self):
        if self.type != "DFA":
            raise ValueError("complement method is only applicable for DFA")

        new_final_states = self.Q - self.F
        return FA(self.Q, self.X, self.delta, self.q0, new_final_states)

    def testString(self, word):
        if self.type == "DFA":
            q = self.q0
            for symbol in word:
                if (q, symbol) not in self.delta:
                    return False
                q = self.delta[(q, symbol)]
            return q in self.F
        elif self.type == "NFA":
            current_states = self.epsilonClosures(self.q0)
            for symbol in word:
                next_states = set()
                for state in current_states:
                    if (state, symbol) in self.delta:
                        next_states.update(self.delta[(state, symbol)])
                current_states = set()
                for state in next_states:
                    current_states.update(self.epsilonClosures(state))
            return any(state in self.F for state in current_states)
        else:
            raise ValueError("testString method is only applicable for DFA and NFA")

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

    def __repr__(self):
        if not self.delta:
            return "No transitions available."

        # Determine the longest state name for formatting
        state_width = max(len(str(state)) for state in self.Q) + 2

        # Determine the width for each transition column based on the longest transition
        transition_width = max(
            max(len(" ".join(str(s) for s in targets)) if isinstance(targets, set) else len(str(targets)) for targets in self.delta.values()),
            len("ε")  # ε symbol width
        ) + 2

        # Header
        header = f"{'':<{state_width}}  | " + " | ".join(f"{symbol:^{transition_width}}" for symbol in self.X) + f" | {'ε':^{transition_width}} |"
        divider = "=" * len(header)

        # Rows
        rows = []
        sorted_states = sorted(self.Q, key=lambda state: (state != self.q0, state))  # Sort with q0 first
        for state in sorted_states:
            state_str = " ".join(str(s) for s in state) if isinstance(state, frozenset) else str(state)
            
            # Debugging output
            print(f"Comparing state: {state} ({type(state)}) with start state: {self.q0} ({type(self.q0)})")
            print(f"Comparing state: {state} ({type(state)}) with final states: {self.F} ({type(self.F)})")
            
            state_marker = "→" if state == self.q0 else " "
            print(state_marker)
            state_marker = "*" + state_marker if state in self.F else " " + state_marker
            row = f"{state_marker} {state_str:^{state_width - 2}} |"
            
            for symbol in self.X:
                if (state, symbol) in self.delta:
                    target_states = " ".join(str(s) for s in self.delta[(state, symbol)])
                    row += f" {target_states:^{transition_width}} |"
                else:
                    row += f" {'-':^{transition_width}} |"
            if (state, '') in self.delta:
                target_states = " ".join(str(s) for s in self.delta[(state, '')])
                row += f" {target_states:^{transition_width}} |"
            else:
                row += f" {'-':^{transition_width}} |"
            rows.append(row)

        # FA type
        fa_type = f"FA Type: {self.type}"

        return f"Transition Table:\n{header}\n{divider}\n" + "\n".join(rows) + f"\n{fa_type}"




