import functions.fa as fa
import database.database as db
import dataStructure.state as state
import sys

sys.stdout.reconfigure(encoding='utf-8')

def sub_menu(db_menu, FA, fa_id):
    while True:
        print(FA)
        print(FA.Q)
        print(FA.X)
        print(FA.delta)
        print(FA.q0)
        print(FA.F)
        print("\nSub Menu")
        print("1. Convert FA (NFA to DFA)")
        print("2. Minimize DFA")
        print("3. Complement DFA")
        print("4. Test String")
        print("5. Generate Word")
        print("6. Edit FA")
        print("7. Exit to main menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            NFA = FA.convertNFAtoDFA()
            print(NFA)
        elif choice == '2':
            DFA = FA
            DFA.minimize()
            print(DFA)
        elif choice == '3':
            FA.complement()
            print(FA)
        elif choice == '4':
            print("Enter string to test: ")
            input_string = input()
            if FA.testString(input_string):
                print(f"'{input_string}' is accepted.")
            else:
                print(f"'{input_string}' is rejected.")
        elif choice == '5':
            FA.wordGenerator()
        elif choice == '6':
            print("Edit FA")
            print("1. Add transition")
            print("2. Add start state")
            print("3. Add final state")
            print("4. Update FA")
            print("5. Delete FA")
            print("6. Exit to Sub menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                delta_list = []
                print("Enter transitions (q, x, p)\n")
                transitions = input("Enter transition or leave the second character empty for empty transition: ")
                FA.delta.append(tuple(fa.convert_delta(transitions.split(','))))
            elif choice == '2':
                start_state = input("Enter start state: ")
                FA.q0.append(start_state)
            elif choice == '3':
                FA.F.append(input("Enter final state: "))
            elif choice == '4':
                print("Update FA")
                print("Enter transitions (q, x, p)\n")
                transitions = input("Enter transition or leave the second character empty for empty transition: ")
                FA.delta.append(tuple(fa.convert_delta(transitions.split(','))))
                start_state = input("Enter start state: ")
                FA.q0.append(start_state)
                FA.F.append(input("Enter final state: "))
            elif choice == '5':
                db_menu.delete_fa(fa_id)
                return
            elif choice == '6':
                continue
            else:
                print("Invalid choice. Please try again.")
            db_menu.update_fa(FA, fa_id)
        elif choice == '7':
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
            print(Q)
            X = input("Enter input symbols (comma separated): ").split(',')
            print(X)
            delta = []
            print("Enter transitions (q, x, p) or 'done' to finish.")
            while True:
                transition = input("Enter transition or leave the second character empty for empty transition: ")
                if transition == 'done':
                    break
                delta.append(tuple(transition.split(',')))
            print(delta)
            q0 = input("Enter start state (comma seperated): ").split(',')
            print(q0)
            F = input("Enter final states (comma separated): ").split(',')
            print(F)
            description = input("Enter description: ")
            print(description)
            FA = fa.FA(Q, X, delta, q0, F)
            print(FA)
            db_menu.insert_fa(FA.type, description, q0, F, Q, X, delta)
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
                sub_menu(db_menu, fa_object, fa_data["id"])

        elif choice == '3': 
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    main_menu()
    
if __name__ == "__main__":
    main()
