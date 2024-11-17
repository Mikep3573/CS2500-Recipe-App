"""
Description:
Authors:
Date:
"""

# Dependencies
import sqlite3

def get_numeric_cols() -> list:
    con = sqlite3.connect(database="recipe_app.db", isolation_level=None)
    cur = con.cursor()
    rows_auth = cur.execute("SELECT name" \
                " FROM pragma_table_info('Authors')" \
                " WHERE (type LIKE '%INT%' OR type LIKE '%REAL%')" \
                " AND name NOT LIKE '%_ID'")
    cur = con.cursor()
    rows_ing = cur.execute("SELECT name" \
                " FROM pragma_table_info('Ingredients')" \
                " WHERE (type LIKE '%INT%' OR type LIKE '%REAL%')" \
                " AND name NOT LIKE '%_ID'")
    cur = con.cursor()
    rows_rec = cur.execute("SELECT name" \
                " FROM pragma_table_info('Recipes')" \
                " WHERE (type LIKE '%INT%' OR type LIKE '%REAL%')" \
                " AND name NOT LIKE '%_ID'")
    
    # Create a list of possible numerical columns to query on (exlcuding any repeat columns)
    numeric_cols = [(row[0], "Authors") for row in rows_auth]
    numeric_cols = set(numeric_cols).union(set([(row[0], "Ingredients") for row in rows_ing]))
    numeric_cols = set(numeric_cols).union(set([(row[0], "Recipes") for row in rows_rec]))
    numeric_cols = list(numeric_cols)
    
    # Create a list of options to give to stat_queries
    cols = [col for col in numeric_cols]
    return cols