import sqlite3
import pandas as pd


buddymovie = pd.read_csv("./buddymove_holidayiq.csv")
print(buddymovie.head())


# Open a connection to a new (blank) database file buddymove_holidayiq.sqlite3
conn = sqlite3.connect("buddymove_holidayiq.sqlite3")
curs = conn.cursor()


# Use df.to_sql (documentation) to insert the data into a new table
# Review in the SQLite3 database
buddymovie.to_sql("buddymove_holidayiq", con=conn)


# Count how many rows you have - it should be 249!
query1 = """
SELECT COUNT(*)
FROM buddymove_holidayiq;
"""

curs.execute(query1)
print(curs.fetchall())


# How many users who reviewed at least 100 Nature in the category also
# reviewed at least 100 in the Shopping category?
query2 = """
SELECT COUNT(DISTINCT(`User ID`))
FROM buddymove_holidayiq
WHERE Nature >= 100 AND Shopping >= 100;
"""

curs.execute(query2)
print(curs.fetchall())


# (Stretch) What are the average number of reviews for each category?
query3 = """
SELECT 
  AVG(Sports),
  AVG(Religious),
  AVG(Nature),
  AVG(Theatre),
  AVG(Shopping),
  AVG(Picnic)
FROM buddymove_holidayiq;
"""

curs.execute(query3)
print(curs.fetchall())
