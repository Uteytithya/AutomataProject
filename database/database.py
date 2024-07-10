import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="automata",
                port="8889"
            )
        except Error as e:
            print(f"Error: {e}")

    def insert_fa(self, type, description, start_state, final_state, states, symbols, transitions):
        try:
            cursor = self.conn.cursor()

            # Insert into `start_state` table and get the start state ID
            cursor.execute("INSERT INTO start_state (name) VALUES (%s)", (start_state,))
            start_state_id = cursor.lastrowid

            # Insert into `final_state` table and get the final state ID
            cursor.execute("INSERT INTO final_state (name) VALUES (%s)", (final_state,))
            final_state_id = cursor.lastrowid

            # Insert into `fa` table
            cursor.execute("""
                INSERT INTO fa (type, description, start_state_id, final_state_id)
                VALUES (%s, %s, %s, %s)
            """, (type, description, start_state_id, final_state_id))
            fa_id = cursor.lastrowid

            # Insert states into `state` and `state_list` tables
            state_ids = {}
            for state in states:
                cursor.execute("INSERT INTO state (name) VALUES (%s)", (state,))
                state_id = cursor.lastrowid
                state_ids[state] = state_id
                cursor.execute("INSERT INTO state_list (state_id, fa_id) VALUES (%s, %s)", (state_id, fa_id))

            # Insert symbols into `symbol_list` table
            for symbol in symbols:
                cursor.execute("INSERT INTO symbol_list (name, fa_id) VALUES (%s, %s)", (symbol, fa_id))

            # Insert transitions into `transition` and `transition_list` tables
            for transition in transitions:
                symbol, state_from, state_to = transition
                cursor.execute("INSERT INTO transition (symbol, state_from, state_to) VALUES (%s, %s, %s)", (symbol, state_from, state_to))
                transition_id = cursor.lastrowid
                cursor.execute("INSERT INTO transition_list (transition_id, fa_id) VALUES (%s, %s)", (transition_id, fa_id))

            # Commit the transaction
            self.conn.commit()

        except Error as e:
            print(f"Error: {e}")
            self.conn.rollback()

    def delete_fa(self, fa_id):
        try:
            cursor = self.conn.cursor()

            # Delete from `fa` table
            cursor.execute("DELETE FROM fa WHERE id = %s", (fa_id,))

            # Delete related entries from other tables (adjust according to your schema)
            cursor.execute("DELETE FROM state_list WHERE fa_id = %s", (fa_id,))
            cursor.execute("DELETE FROM symbol_list WHERE fa_id = %s", (fa_id,))
            cursor.execute("DELETE FROM transition_list WHERE fa_id = %s", (fa_id,))

            # Commit the transaction
            self.conn.commit()

        except Error as e:
            print(f"Error: {e}")
            self.conn.rollback()

    def update_fa(self, fa_id, type, description, start_state, final_state):
        try:
            cursor = self.conn.cursor()
            
            # # Get the ID of the start state
            # cursor.execute("SELECT id FROM start_state WHERE name = %s", (start_state,))
            # start_state_id = cursor.fetchone()[0]

            # # Get the ID of the final state
            # cursor.execute("SELECT id FROM final_state WHERE name = %s", (final_state,))
            # final_state_id = cursor.fetchone()[0]

            # Update `fa` table
            cursor.execute("""
                UPDATE fa
                SET type = %s, description = %s, start_state_id = %s, final_state_id = %s
                WHERE id = %s
            """, (type, description, start_state, final_state, fa_id))

            # Commit the transaction
            self.conn.commit()

        except Error as e:
            print(f"Error: {e}")
            self.conn.rollback()

    def getAllFA(self):
        try:
            query = "SELECT DISTINCT * FROM FA_VIEW"
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()

# Usage example
db = Database()

# Example parameters for insert_fa
type = "DFA"
description = "Example description"
start_state = "q0"
final_state = "q1"
states = ["q0", "q1", "q2"]
symbols = ["a", "b"]
transitions = [
    ("a", "q0", "q1"),
    ("b", "q1", "q2"),
    ("a", "q2", "q0")
]

# Insert a new FA record
# db.insert_fa(type, description, start_state, final_state, states, symbols, transitions)

# Select all FA records
# all_fa = db.getAllFA()
# for fa in all_fa:
#     print(fa)


# Update an existing FA record (replace fa_id with an existing FA ID)
fa_id = 5  # Replace with an existing FA ID
new_type = "NFA"
new_description = "Updated description"
new_start_state = "q1"
new_final_state = "q2"
db.update_fa(fa_id, new_type, new_description, new_start_state, new_final_state)

# Print updated FA record
print("\nUpdated FA Record:")
updated_fa = db.getAllFA()
for fa in updated_fa:
    print(fa)

# Delete an existing FA record (replace fa_id with an existing FA ID)
# db.delete_fa(6)
    
    
