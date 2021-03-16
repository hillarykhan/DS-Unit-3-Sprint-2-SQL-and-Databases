import sqlite3

# STEP 1: Import library
import sqlite3
from queries import TOTAL_SUBCLASS


# STEP 2: Create a function to create the connection
def connect_to_db(db_name="rpg_db.sqlite3"):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


# STEP 3: Execute and return query results
if __name__ == "__main__":
    # Connect to DB
    conn = connect_to_db()
    # Create Cursor
    curs = conn.cursor()
    # Execute query
    results = execute_query(curs, TOTAL_SUBCLASS)
    print(results)
