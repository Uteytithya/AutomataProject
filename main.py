import functions.fa as fa
import database.database as db
import dataStructure.state as state

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
if __name__ == "__main__":
    main()
