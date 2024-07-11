import functions.fa as fa
import database.database as db
import dataStructure.state as state
import sys

sys.stdout.reconfigure(encoding='utf-8')

def sub_menu(db_menu, FA):
    while True:
        print(FA)
        print("\nSub Menu")
        print("1. Convert FA (NFA to DFA)")
        print("2. Minimize DFA")
        print("3. Complement DFA")
        print("4. Test String")
        print("5. Generate Word")
        print("6. Edit FA")
        print("7. Delete FA")
        print("8. Exit to main menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            NFA = FA.convertNFAtoDFA()
            print(NFA)
        elif choice == '2':
            DFA = FA
            DFA.minimizeDFA()
            print(DFA)
        elif choice == '3':
            FA.complementDFA()
            print(FA)
        elif choice == '4':
            FA.testString()
        elif choice == '5':
            FA.wordGenerator()
        elif choice == '6':
            db.updateFA(FA)
        elif choice == '7':
            db.deleteFA(FA)
            return
        elif choice == '8':
            return
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    db_menu = db.Database()
    while True:
        print("\nMain Menu")
        print("1. Create FA")
        print("2. Select FA")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Create FA
            Q = input("Enter states (comma separated): ").split(',')
            X = input("Enter input symbols (comma separated): ").split(',')
            delta = []
            print("Enter transitions (q, x, p) or 'done' to finish.")
            while True:
                transition = input("Enter transition or Press e to do empty transition: ")
                if transition[1] == 'e':
                    delta.append((transition[0], '', transition[3]))
                if transition == 'done':
                    break
                delta.append(tuple(transition.split(',')))
            q0 = input("Enter start state (comma seperated): ").split(',')
            F = input("Enter final states (comma separated): ").split(',')
            description = input("Enter description: ")
            FA = fa.FA(Q, X, delta, q0, F)
            db_menu.insertFA(FA.type, description, q0, F, Q, X, delta)
        elif choice == '2':
                FA_List = db_menu.getAllFa()
                print("Select FA")
                count = 1
                for i in FA_List:
                    print(f"{count}. {i['description']}")
                    count += 1
                choice = int(input("Enter your choice: "))
                fa_data = db_menu.get_fa(choice)
                if fa_data:
                    Q = fa_data["Q"]
                    X = fa_data["X"]
                    delta = fa_data["delta"]
                    q0 = fa_data["q0"]
                    F = fa_data["F"]

                    fa_object = fa.FA(Q, X, delta, q0, F)
                sub_menu(db_menu, fa_object)

        elif choice == '3': 
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    main_menu()
    # Q = {'q0', 'q1', 'q2'}
    # X = {'a', 'b'}
    # delta = [('q0', 'a', 'q1'), ('q0', 'b', 'q0'), ('q1', 'a', 'q1'), ('q1', 'b', 'q2'), ('q2', 'a', 'q2'), ('q2', 'b', 'q2')]
    # q0 = ('q0')
    # F = {'q2'}
    # description = "W that starts with 'a' and ends with 'b'"
    
    # type = "DFA"
    # description = "W that starts with 'a' and ends with 'b'"
    # start_state = "q0"
    # final_state = "q1"
    # states = ["q0", "q1", "q2"]
    # symbols = ["a", "b"]
    # transitions = [
    #     ("q0", "a", "q1"),
    #     ("q1", "b", "q2"),
    #     ("q2", "a", "q0"),
    #     ("q0", "b", "q0"),
    #     ("q2", "b", "q2"),
    #     ("q1", "a", "q1")
    # ]
    # dbx = db.Database()
    # # Insert a new FA record
    # # dbx.insert_fa(type, description, start_state, final_state, states, symbols, transitions)
    # # fa_data = dbx.get_fa(6)
    # # print(FA_get)
    # # if fa_data:
    # #     Q = fa_data["Q"]
    # #     X = fa_data["X"]
    # #     delta = fa_data["delta"]
    # #     q0 = fa_data["q0"]
    # #     F = fa_data["F"]

    # #     fa_object = fa.FA(Q, X, delta, q0, F)
    # #     print(fa_object)
    # # else:
    # #     print("No data found.")
    # fa_list = dbx.getAllFa()
    # if fa_list:
    #     count = 1
    #     for fa_data in fa_list:
    #         print(f"{count}. {fa_data['description']}")
    #         count += 1


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
    # Generate DFA
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
        ('q1', 'a', 'q6'), ('q1', 'b', 'q2'),
        ('q2', 'a', 'q0'), ('q2', 'b', 'q2'),
        ('q3', 'a', 'q2'), ('q3', 'b', 'q6'),
        ('q4', 'a', 'q7'), ('q4', 'b', 'q5'),
        ('q5', 'a', 'q2'), ('q5', 'b', 'q6'),
        ('q6', 'a', 'q6'), ('q6', 'b', 'q4'),
        ('q7', 'a', 'q6'), ('q7', 'b', 'q2')
    ]
    q0 = 'q0'
    F = {'q2'}

    # Create the DFA
    FA1 = fa.FA(Q, X, delta, q0, F)

    # Minimize the DFA
    FA1.minimize()

    # Print the minimized DFA
    print(FA1)



if __name__ == "__main__":
    main()
