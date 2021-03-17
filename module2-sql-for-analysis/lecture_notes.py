import psycopg2
from psycopg2.extras import execute_values
import json

# Connect to ElephantSQL-hosted PostgresSQL
# IMPORTANT: DO NOT COMMIT with credentials hard-coded
# NEED TO SPECIFY CREDENTIALS WITH ENVIRONMENT VARIABLES
# Example of what not to do in your .py:
# DB_NAME = 'kvpmgnub'
# DB_USER = 'kvpmgnub'
# DB_PASSWORD = 'zLm2fPBqZF-Do1OEUqTCU4rab8yfghCv'
# DB_HOST = 'queenie.db.elephantsql.com'



import os
from dotenv import load_dotenv

# Loads contents of the .env file into the script's environment
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# Helpful to check that your system knows what the variables are first
# before running additional commands - can be accomplished here:
# print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
# exit()

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION", conn)

# A "cursor", a structure to iterate over db records to perform queries
cur = conn.cursor()
print("CURSOR", cur)

# An example query
cur.execute('SELECT * from test_table;')

# Note: nothing happened yet! We need to *fetch* from cursor
# FETCH DATA
result = cur.fetchall()
print("RESULT: ", type(result))
print(result)

### If you see something like (1, 'A row name', None), congrats!
### You've interacted with your database from Python
### FYI: in sqlite: result = cur.execute('SELECT * from test_table;').fetchall()
### chaining commands like this doesn't work with psycopg

# INSERT DATA
# insertion_sql = """
# INSERT INTO test_table (name, data) VALUES -- filling values for the name and data columns (id auto generates)
# ('A row name', null), -- add the data as tuples (first value corresponds to order above (name) second to data)
# ('Another row, with JSON', '{"a": 1, "b": ["dog", "cat", 42], "c": true}'::JSONB -- :: converts/casts data types - in this case from a string to a JSON blob
# );
# """
# cur.execute(insertion_sql)

# Another method to inserting data without hardcoding python dictionaries, etc.
# (object-oriented approach)
my_dict = {"a": 1, "b": ["dog", "cat", 42], "c": True}
# insertion_query = "INSERT INTO test_table (name, data) VALUES (%s, %s)"
# cur.execute(insertion_query, ('A row name', 'null'))    # functional applied to object hence object-oriented
# cur.execute(insertion_query, ('Another row, with JSONNN', json.dumps(my_dict))

# Problem is that the above approach does one row at a time
# Passing multiple rows into a table (functional approach):
insertion_query = f"INSERT INTO test_table (name, data) VALUES %s"
execute_values(cur, insertion_query, [  # from psycopg2.extras import execute_values
    ('A rowwwww', 'null'),
    ('Another row, with JSONNNNNN', json.dumps(my_dict)),   # import json
    ('Third row', '3')
])  # data must be in a list of tuples!!!

# FYI: When we modify the contents of a table with a CREATE, DROP, INSERT, etc.
# statement, we need an additional step: commit/save results
# Otherwise, a primary key will be allocated to the rows but they won't actually
# appear in the table.
# Commit(Save) table modifications (in this case, inserting rows):
conn.commit()

# Good practice to all close the cursor and connection
cur.close()
conn.close()

