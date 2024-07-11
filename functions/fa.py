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
            if (start, symbol) not in delta_dict:
                delta_dict[(start, symbol)] = set()
            delta_dict[(start, symbol)].add(end)
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

    def epsilonClosures(self, states):
        closure = states
        stack = list(states)

        while stack:
            current_state = stack.pop()
            if (current_state, "") in self.delta:
                for next_state in self.delta[(current_state, "")]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return frozenset(closure)

    def convertNFAtoDFA(self):
        if self.type != "NFA":
            raise ValueError("convertNFAtoDFA method is only applicable for NFA")


        initial_closure = self.epsilonClosures(self.q0)
        initial_state = frozenset(initial_closure)

        dfa_states = {initial_state}
        unprocessed_states = [initial_state]
        dfa_delta = {}
        dfa_start_state = initial_state
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
                        new_state.update(self.epsilonClosures(self.delta[(state, symbol)]))

                new_state = frozenset(new_state)

                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unprocessed_states.append(new_state)

                dfa_delta[(current, symbol)] = new_state

        # Convert states and transitions to the input format
        dfa_states_list = [self.state_to_string(state) for state in dfa_states]
        dfa_states_list.sort()
        print("DFA States List:", dfa_states_list)
        
        dfa_delta_list = [(self.state_to_string(state), symbol, self.state_to_string(target)) for (state, symbol), target in dfa_delta.items()]
        print("DFA Delta List:", dfa_delta_list)
        
        dfa_accept_states_list = [self.state_to_string(state) for state in dfa_accept_states]
        print("DFA Accept States List:", dfa_accept_states_list)
        
        dfa_start_state_str = self.state_to_string(dfa_start_state)
        print("DFA Start State:", dfa_start_state_str)

        return dfa_states_list, self.X, dfa_delta_list, dfa_start_state_str, dfa_accept_states_list



    def minimize(self):
        if self.type != "DFA":
            raise ValueError("minimize method is only applicable for DFA")

        # Step 1: Initialize partitions
        P = [set(self.F), set(self.Q) - set(self.F)]
        W = [set(self.F), set(self.Q) - set(self.F)]
        
        while W:
            A = W.pop()
            for c in self.X:
                X = {q for q in self.Q if (q, c) in self.delta and self.delta[(q, c)] in A}
                new_P = []
                for Y in P:
                    intersection = X & Y
                    difference = Y - X
                    if intersection and difference:
                        new_P.extend([intersection, difference])
                        if Y in W:
                            W.remove(Y)
                            W.extend([intersection, difference])
                        else:
                            W.append(intersection if len(intersection) <= len(difference) else difference)
                    else:
                        new_P.append(Y)
                P = new_P
        print(P)
        print(W)
        # Step 2: Create the new states
        state_mapping = {q: i for i, partition in enumerate(P) for q in partition}
        new_states = {i: partition for i, partition in enumerate(P)}
        new_F = {state_mapping[state] for state in self.F}
        new_q0 = state_mapping[self.q0]
        
        
        # Step 3: Create the new delta function
        new_delta = {}
        for (q, c), p in self.delta.items():
            new_delta[(state_mapping[q], c)] = state_mapping[p]

        # Convert to input format
        new_states_list = [self.state_to_string(state) for state in new_states.values()]
        new_states_list.sort()
        print("Minimized States List:", new_states_list)

        new_delta_list = [(self.state_to_string(start), symbol, self.state_to_string(end)) for (start, symbol), end in new_delta.items()]
        print("Minimized Delta List:", new_delta_list)
        
        new_accept_states_list = [self.state_to_string(state) for state in new_F]
        print("Minimized Accept States List:", new_accept_states_list)

        new_start_state_str = self.state_to_string(new_q0)
        print("Minimized Start State:", new_start_state_str)

        return new_states_list, self.X, new_delta_list, new_start_state_str, new_accept_states_list


    def complement(self):
        if self.type != "DFA":
            raise ValueError("complement method is only applicable for DFA")

        self.F = self.Q - self.F
        return self

    def testString(self, word):
        if self.type == "DFA":
            for i in self.q0:
                current_state = i
                  # Corrected start state initialization
            print(f"Initial state: {current_state}")
            for symbol in word:
                print(f"Processing symbol: {symbol}")
                if (current_state, symbol) in self.delta:
                    next_state = self.delta[(current_state, symbol)]
                    print(f"Transition: {current_state} --{symbol}--> {next_state}")
                    current_state = next_state
                else:
                    print(f"No transition found for {current_state} with symbol {symbol}. String rejected.")
                    return False
            if current_state not in self.F:
                print(f"Final state: {current_state}. String accepted.")
                return True
            else:
                print(f"Final state: {current_state}. String rejected.")
                return False
        elif self.type == "NFA":
            current_states = self.epsilonClosures(frozenset(self.q0) if isinstance(self.q0, list) else self.q0)
            print(f"Initial epsilon-closure: {current_states}")
            for symbol in word:
                print(f"Processing symbol: {symbol}")
                next_states = set()
                for state in current_states:
                    if (state, symbol) in self.delta:
                        transitions = self.delta[(state, symbol)]
                        print(f"Transition: {state} --{symbol}--> {transitions}")
                        next_states.update(transitions)
                current_states = set()
                for state in next_states:
                    closures = self.epsilonClosures(state)
                    print(f"Epsilon-closure of {state}: {closures}")
                    current_states.update(closures)
            if any(state in self.F for state in current_states):
                print(f"Final states: {current_states}. String accepted.")
                return True
            else:
                print(f"Final states: {current_states}. String rejected.")
                return False
        else:
            raise ValueError("testString method is only applicable for DFA and NFA")



    def wordGenerator(self, length):
        if self.type != "DFA":
            raise ValueError("wordGenerator method is only applicable for DFA")

        def generateWords(length: int, currentWord: str, currentState) -> list:
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

        # Handle initial state and transitions consistently
        initial_state = frozenset(self.q0) if isinstance(self.q0, set) else self.q0
        self.delta = {(frozenset(k[0]) if isinstance(k[0], set) else k[0], k[1]): frozenset(v) if isinstance(v, set) else v for k, v in self.delta.items()}
        self.q0 = initial_state
        self.F = {frozenset(state) if isinstance(state, set) else state for state in self.F}
        
        # Generate words of the given length
        words_of_given_length = generateWords(length, "", initial_state)
        
        return words_of_given_length




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

            for i in self.q0:
                if state == i:
                    state_marker = "→"
                else:
                    state_marker = " "

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
