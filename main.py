import functions.fa as fa
import database.database as db
import dataStructure.state as state
<<<<<<< HEAD
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main():
    Q = {'q0', 'q1', 'q2'}
    X = {'a', 'b'}
    delta = {
        ('q0', 'a'): 'q1', ('q0', 'b'): 'q0',
        ('q1', 'a'): 'q1', ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q2', ('q2', 'b'): 'q2'
    }
    q0 = ('q0')
    F = {'q2'}

    FA1 = fa.FA(Q, X, delta, q0, F)
    
    print(FA1.isDFA())
    print(FA1.minimize)
    # print(FA1.wordGenerator(5))
    print(FA1.testString('ab'))
    print(FA1)  
    # Generate NFA
    
    Q = {'q0', 'q1', 'q2', 'q3'}
    X = {'a', 'b'}
    delta = {
        ('q0', 'a'): {'q1'}, ('q0', ''): {'q2'},
        ('q1', 'b'): {'q2'},
        ('q2', 'a'): {'q3'},
        ('q3', 'b'): {'q0'}
    }
    q0 = ('q0')
    F = {'q0'}

    FA2 = fa.FA(Q, X, delta, q0, F)

    # DFA2 = FA2.convertNFAtoDFA()
    print(DFA2.isDFA())
    print(DFA2)



=======

def main():
    # Create the database
    db.createDatabase()

    # Create the initial state
    initialState = state.State()

    # Create the genetic algorithm
    geneticAlgorithm = fa.FA(initialState)

    # Run the genetic algorithm
    geneticAlgorithm.run()

    # Close the database
    db.closeDatabase()
>>>>>>> 456b934c616ddd1be017a12bfde8e7e457c9e870
if __name__ == "__main__":
    main()
