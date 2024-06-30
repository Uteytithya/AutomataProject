import functions.fa as fa
import database.database as db
import dataStructure.state as state

def main():
    # # Create the database
    # db.createDatabase()

    # # Create the initial state
    # initialState = state.State()

    # # Create the genetic algorithm
    # geneticAlgorithm = fa.FA(initialState)

    # # Run the genetic algorithm
    # geneticAlgorithm.run()

    # # Close the database
    # db.closeDatabase()

    Q = {'q0', 'q1', 'q2'}
    X = {'a', 'b'}
    delta = {
        ('q0', 'a'): 'q1', ('q0', 'b'): 'q0',
        ('q1', 'a'): 'q1', ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q2', ('q2', 'b'): 'q2'
    }
    q0 = 'q0'
    F = {'q2'}

    FA1 = fa.FA(Q, X, delta, q0, F)
    print(FA1)

    print(FA1.wordGenerator(5))
    # print(FA1.testString('ab'))

if __name__ == "__main__":
    main()
