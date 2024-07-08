import functions.fa as fa
import database.database as db
import dataStructure.state as state
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    # Q = {'q0', 'q1', 'q2'}
    # X = {'a', 'b'}
    # delta = [('q0', 'a', 'q1'), ('q0', 'b', 'q0'), ('q1', 'a', 'q1'), ('q1', 'b', 'q2'), ('q2', 'a', 'q2'), ('q2', 'b', 'q2')]
    # q0 = ('q0')
    # F = {'q2'}

    # FA1 = fa.FA(Q, X, delta, q0, F)
    
    # print(FA1.isDFA())
    # # print(FA1.wordGenerator(5))
    # # print(FA1.testString('ab'))
    # print(FA1)  
    # # Generate NFA
    
    # Q = {'q0', 'q1', 'q2', 'q3'}
    # X = {'a', 'b'}
    # delta = [('q0', 'a', 'q1'), ('q0', 'b', 'q0'), ('q1', 'a', 'q1'), ('q1', 'b', 'q2'), ('q2', 'a', 'q2'), ('q2', 'b', 'q2'), ('q2', '', 'q3'), ('q3', 'a', 'q3'), ('q3', 'b', 'q3')]
    # q0 = ('q0')
    # F = {'q0'}

    # FA2 = fa.FA(Q, X, delta, q0, F)
    # # print(FA2.epsilonClosures('q0'))
    # DFA2 = FA2.convertNFAtoDFA()
    # print(DFA2.q0)
    # print(DFA2.isDFA())
    # print(DFA2.delta)
    # print(DFA2.F)
    # print(DFA2.Q)

    # Q = {'q0', 'q1', 'q2', 'q3'}
    # X = {'a', 'b'}
    # delta = [('q0', 'a', 'q0'), ('q0', 'b', 'q0'), ('q0', 'b', 'q1'), ('q1', 'a', 'q2'), ('q1', 'b', 'q2'), ('q1', '', 'q2'), ('q2', 'a', 'q3'), ('q2', 'b', 'q3')]
    # q0 = ('q0')
    # F = {'q3'}

    # FA3 = fa.FA(Q, X, delta, q0, F)
    # print(FA3.isDFA())
    # # Generate DFA
    # DFA3 = FA3.convertNFAtoDFA()
    # print(DFA3.isDFA())
    # print("\n")
    # print(DFA3.Q)
    # print("\n")
    # print(DFA3.X)
    # print("\n")
    # print(DFA3.delta)
    # print("\n")
    # print(DFA3.q0)
    # print("\n")
    # print(DFA3.F)
    # print("\n")
    # print(DFA3)

    # Define the DFA
    Q = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'}
    X = {'a', 'b'}
    delta = [
        ('q0', 'a', 'q1'), ('q0', 'b', 'q5'),
        ('q1', 'a', 'q2'), ('q1', 'b', 'q0'),
        ('q2', 'a', 'q6'), ('q2', 'b', 'q6'),
        ('q3', 'a', 'q2'), ('q3', 'b', 'q7'),
        ('q4', 'a', 'q4'), ('q4', 'b', 'q5'),
        ('q5', 'a', 'q0'), ('q5', 'b', 'q4'),
        ('q6', 'a', 'q6'), ('q6', 'b', 'q2'),
        ('q7', 'a', 'q6'), ('q7', 'b', 'q5')
    ]
    q0 = 'q0'
    F = {'q2'}

    # Create the DFA
    FA1 = fa.FA(Q, X, delta, q0, F)

    # Minimize the DFA
    min_dfa = FA1.minimizeDFA()

    # Print the minimized DFA
    print(min_dfa)



if __name__ == "__main__":
    main()
