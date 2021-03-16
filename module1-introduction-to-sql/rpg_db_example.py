"""SQL WORKFLOW EXAMPLE"""
# STEP 1: Import library
import sqlite3


# STEP 2: Create a function to create the connection
def connect_to_db(db_name="rpg_db.sqlite3"):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


# STEP 3: Create Queries
# TOTAL_CHARACTERS: How many total Characters are there?
TOTAL_CHARACTERS = """ 
    SELECT COUNT(*)
    FROM charactercreator_character;
"""

# TOTAL_SUBCLASS: How many of each specific subclass?
TOTAL_SUBCLASS = """
WITH character_class AS (
SELECT 
  DISTINCT
  character.character_id,
  CASE 
    WHEN cleric.character_ptr_id IS NOT NULL THEN "cleric"
	WHEN fighter.character_ptr_id IS NOT NULL THEN "fighter"
	WHEN mage.character_ptr_id IS NOT NULL AND necromancer.mage_ptr_id IS NULL THEN "mage"
	WHEN necromancer.mage_ptr_id IS NOT NULL THEN "necromancer"
	WHEN thief.character_ptr_id IS NOT NULL THEN "thief"
  END AS subclass
FROM charactercreator_character character
  LEFT OUTER JOIN charactercreator_cleric cleric
    ON character.character_id = cleric.character_ptr_id
  LEFT OUTER JOIN charactercreator_fighter fighter
    ON character.character_id = fighter.character_ptr_id
  LEFT OUTER JOIN charactercreator_mage mage
    ON character.character_id = mage.character_ptr_id
  LEFT OUTER JOIN charactercreator_necromancer necromancer
    ON mage.character_ptr_id = necromancer.mage_ptr_id
  LEFT OUTER JOIN charactercreator_thief thief
    ON thief.character_ptr_id = thief.character_ptr_id
)
SELECT
  subclass,
  COUNT(*) AS subclass_count
FROM character_class
GROUP BY subclass;
"""

# TOTAL_ITEMS: How many total Items?
TOTAL_ITEMS = """
SELECT COUNT(*) AS item_count
FROM armory_item;
"""

# WEAPONS: How many of the Items are weapons?
WEAPONS = """
SELECT COUNT(*) AS weapon_count
FROM armory_weapon;
"""

# NON_WEAPONS: How many of the items are not weapons?
NON_WEAPONS = """
SELECT COUNT(*)
FROM armory_item item
LEFT JOIN armory_weapon weapon
ON item.item_id = weapon.item_ptr_id
WHERE weapon.item_ptr_id IS NULL;
"""

# CHARACTER_ITEMS: How many Items does each character have?
# (Return first 20 rows)

CHARACTER_ITEMS = """
SELECT 
  charactercreator_character_inventory.character_id,
  COUNT(*) AS item_count
FROM charactercreator_character_inventory
GROUP BY character_id
LIMIT 20;
"""

# CHARACTER_WEAPONS: How many Weapons does each character have?
# (Return first 20 rows)

CHARACTER_WEAPONS = """
SELECT 
  inventory.character_id,
  COUNT(*) AS weapon_count
FROM charactercreator_character_inventory inventory
INNER JOIN armory_weapon weapon
ON inventory.item_id = weapon.item_ptr_id
GROUP BY inventory.character_id
LIMIT 20;
"""

# AVG_CHARACTER_ITEMS: On average, how many Items does each Character have?
AVG_CHARACTER_ITEMS = """
WITH character_items AS (
SELECT 
  charactercreator_character_inventory.character_id,
  COUNT(*) AS item_count
FROM charactercreator_character_inventory
GROUP BY character_id
)
SELECT AVG(item_count) AS items_avg
FROM character_items;
"""

# AVG_CHARACTER_WEAPONS: On average, how many Weapons does each character have?
AVG_CHARACTER_WEAPONS = """
SELECT 
CAST(SUM(CASE WHEN weapons.item_ptr_id IS NULL THEN 0 ELSE 1 END) AS FLOAT)/COUNT(DISTINCT(characters.character_id)) AS weapon_avg
FROM charactercreator_character characters
LEFT OUTER JOIN charactercreator_character_inventory inventory
ON characters.character_id = inventory.character_id
LEFT OUTER JOIN armory_weapon weapons
ON inventory.item_id = weapons.item_ptr_id;
"""

# STEP 4: Execute and return query results
queries_dict = {'TOTAL_CHARACTERS': TOTAL_CHARACTERS,
                'TOTAL_SUBCLASS': TOTAL_SUBCLASS,
                'TOTAL_ITEMS': TOTAL_ITEMS,
                'WEAPONS' : WEAPONS,
                'NON_WEAPONS' : NON_WEAPONS,
                'CHARACTER_ITEMS' : CHARACTER_ITEMS,
                'CHARACTER_WEAPONS' : CHARACTER_WEAPONS,
                'AVG_CHARACTER_ITEMS' : AVG_CHARACTER_ITEMS,
                'AVG_CHARACTER_WEAPONS' : AVG_CHARACTER_WEAPONS
                }
if __name__ == "__main__":
    # Connect to DB
    conn = connect_to_db()
    # Create Cursor
    curs = conn.cursor()
    # Execute query
    for key in queries_dict.keys():
        print(key, execute_query(curs, queries_dict[key]))
