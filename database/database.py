import mysql.connector
from mysql.connector import Error
from functions import fa as fa
import json

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="automata",
                port="3306"
            )
        except Error as e:
            print(f"Error: {e}")

    def insert_fa(self, type, description, start_state, final_state, states, symbols, transitions):
        try:
            cursor = self.conn.cursor()

            # Serialize lists to JSON strings
            states_json = json.dumps(states)
            symbols_json = json.dumps(symbols)
            transitions_json = json.dumps(transitions)
            start_state_json = json.dumps(start_state)
            final_state_json = json.dumps(final_state)  

            cursor.execute(
                """
                INSERT INTO fa_backup (type, description, start_state, final_state, state, symbol, transition)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (type, description, start_state_json, final_state_json, states_json, symbols_json, transitions_json)
            )

            # Commit the transaction
            self.conn.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            self.conn.rollback()
        except ValueError as ve:
            print(f"Validation Error: {ve}")

    def delete_fa(self, fa_id):
        try:
            cursor = self.conn.cursor()

            # Execute the delete query with fa_id as a parameter
            cursor.execute("DELETE FROM fa_backup WHERE id = %s", (fa_id,))

            # Commit the transaction
            self.conn.commit()

            print(f"FA configuration with ID {fa_id} deleted successfully.")

        except mysql.connector.Error as e:
            print(f"Error deleting FA configuration: {e}")
            self.conn.rollback()

        finally:
            cursor.close()

    def update_fa(self, fa_id, type, description, start_state, final_state):
        try:
            cursor = self.conn.cursor()

            # Construct the SQL update query
            update_query = """
                UPDATE fa_backup
                SET type = %s, description = %s, start_state = %s, final_state = %s
                WHERE id = %s
            """

            # Execute the update query with parameters
            cursor.execute(update_query, (type, description, json.dumps(start_state), json.dumps(final_state), fa_id))

            # Commit the transaction
            self.conn.commit()

            print(f"FA configuration with ID {fa_id} updated successfully.")

        except mysql.connector.Error as e:
            print(f"Error updating FA configuration: {e}")
            self.conn.rollback()

        finally:
            cursor.close()


    def get_fa(self, fa_id):
        try:
            # Ensure fa_id is an integer
            if not isinstance(fa_id, int):
                raise ValueError("fa_id must be an integer")

            cursor = self.conn.cursor()
            # Execute the query with fa_id as a parameter
            cursor.execute("SELECT type, description, start_state, final_state, state, symbol, transition FROM fa_backup WHERE id = %s", (fa_id,))
            result = cursor.fetchone()

            if result:
                type, description, start_state_json, final_state_json, states_json, symbols_json, transitions_json = result
                states = json.loads(states_json)
                symbols = json.loads(symbols_json)
                transitions = json.loads(transitions_json)
                start_state = json.loads(start_state_json)
                final_state = json.loads(final_state_json)

                # Convert transitions to the expected format
                delta = []
                for transition in transitions:
                    delta.append(tuple(transition))

                # Format the data as requested
                Q = set(states)
                X = set(symbols)
                q0 = set(start_state)
                F = set(final_state if isinstance(final_state, list) else [final_state])

                formatted_data = {
                    "Q": Q,
                    "X": X,
                    "delta": delta,
                    "q0": q0,
                    "F": F
                }

                return formatted_data
            else:
                print(f"No FA found with ID {fa_id}.")
                return None

        except ValueError as ve:
            print(f"Error: {ve}")
            return None

        except mysql.connector.Error as e:
            print(f"Error fetching FA configuration: {e}")
            return None


    def getAllFa(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT type, description, start_state, final_state, state, symbol, transition FROM fa_backup")
            results = cursor.fetchall()

            fa_data_list = []

            for result in results:
                type, description, start_state_json, final_state_json, states_json, symbols_json, transitions_json = result
                states = json.loads(states_json)
                symbols = json.loads(symbols_json)
                transitions = json.loads(transitions_json)
                start_state = json.loads(start_state_json)
                final_state = json.loads(final_state_json)

                fa_data = {
                    'type': type,
                    'description': description,
                    'states': states,
                    'symbols': symbols,
                    'transitions': transitions,
                    'start_state': start_state,
                    'final_state': final_state
                }

                fa_data_list.append(fa_data)

            return fa_data_list

        except Exception as e:
            print(f"Error fetching FA configurations: {e}")
            return []

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()

# Usage example
# db = Database()

# # Example parameters for insert_fa
# type = "DFA"
# description = "W that starts with 'a' and ends with 'b'"
# start_state = "q0"
# final_state = "q1"
# states = ["q0", "q1", "q2"]
# symbols = ["a", "b"]
# transitions = [
#     ("q0", "a", "q1"),
#     ("q1", "b", "q2"),
#     ("q2", "a", "q0")
# ]

# # Insert a new FA record
# db.insert_fa(type, description, start_state, final_state, states, symbols, transitions)
# FA_get = db.get_fa(1)
# # print(FA_get)
# Q = FA_get[0]

# print(Q)
# Select all FA records
# all_fa = db.getAllFA()
# for fa in all_fa:
#     print(fa)


# # Update an existing FA record (replace fa_id with an existing FA ID)
# fa_id = 5  # Replace with an existing FA ID
# new_type = "NFA"
# new_description = "Updated description"
# new_start_state = "q1"
# new_final_state = "q2"
# db.update_fa(fa_id, new_type, new_description, new_start_state, new_final_state)

# # Print updated FA record
# print("\nUpdated FA Record:")
# updated_fa = db.getAllFA()
# for fa in updated_fa:
#     print(fa)

# Delete an existing FA record (replace fa_id with an existing FA ID)
# db.delete_fa(6)