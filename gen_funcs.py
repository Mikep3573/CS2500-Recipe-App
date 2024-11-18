"""
Description:
Authors:
Date:
"""

# Dependencies
import sqlite3

def get_numeric_cols() -> list:
    """
    """
    # Connect to the databse
    con = sqlite3.connect(database="recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Run the queries
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
    
    # Close connection and return results
    con.close()
    return numeric_cols

def get_text_cols() -> list:
    """
    """
    # Connect to the database
    con = sqlite3.connect(database="recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Run the queries
    # Can just check for TEXT since we know all required columns have this affinity
    rows_auth = cur.execute("SELECT name" \
                " FROM pragma_table_info('Authors')" \
                " WHERE type LIKE 'TEXT'")  
    cur = con.cursor()
    rows_ing = cur.execute("SELECT name" \
                " FROM pragma_table_info('Ingredients')" \
                " WHERE type LIKE 'TEXT'")  
    cur = con.cursor()
    rows_rec = cur.execute("SELECT name" \
                " FROM pragma_table_info('Recipes')" \
                " WHERE type LIKE 'TEXT'")
    
    # Create a list of possible text columns to query on (exlcuding any repeat columns)
    text_cols = [(row[0], "Authors") for row in rows_auth]
    text_cols = set(text_cols).union(set([(row[0], "Ingredients") for row in rows_ing]))
    text_cols = set(text_cols).union(set([(row[0], "Recipes") for row in rows_rec]))
    text_cols = list(text_cols)

    # Close connection and return results
    con.close()
    return text_cols


def get_all_cols() -> list:
    """
    """
    # Just return a concatenated list of numeric and text columns
    return get_numeric_cols() + get_text_cols()

def associated_table(col: str) -> str:
    """
    """
    # Find all the columns and their associated tables
    # Return the associated table
    all_cols = get_all_cols()
    for tup in all_cols:
        if tup[0] == col:
            return tup[1]
    return ""

def run_where_query(col: str, table: str, op: str, val: str) -> list:
    """
    """

    # Create a dictionary of additional column information to return alongside the user's request
    additional_cols = {}
    additional_cols['Authors'] = ['F_Name', 'L_Name']
    additional_cols['Recipes'] = ['Recipe_Name', 'Recipe_Description']
    additional_cols['Ingredients'] = ['Ingredient_Name', 'Ingredient_Description']

    # Compile a list of columns to return
    q_cols = []
    if col in additional_cols[table]:
        additional_cols[table].remove(col)
        q_cols = [col] + additional_cols[table]
    else:
        q_cols = additional_cols[table] + [col]

    # Connect to the database
    con = sqlite3.connect(database="recipe_app.db", isolation_level=None)
    cur = con.cursor()
    
    # Setup the query with some additional columns for more information
    query = f"SELECT "
    first_str = ""
    for q_col in q_cols:
        first_str += f"{q_col}, "
        query += f"{q_col}, "
    first_str = first_str[:-2]
    query = query[:-2]  # Removing the final ,
    query += f" FROM {table} WHERE {col} {op} ?"

    # Run the query and get the results
    cur.execute(query, (val,))
    rows = cur.fetchall()
    results = [first_str]
    for row in rows:
        row_str = ""
        for i in range(len(row)):
            row_str += f"{row[i]}, "
        row_str = row_str[:-2]
        results.append(row_str)

    # Close connection
    con.close()

    # Return the results
    return results

def recipe_authors_query() -> list:
    """
    """

    # Create connection
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Create a list of column names to use
    cols = ["Recipe_Name", "Recipe_Description", "Created", "Recipe_Avg_Cost", "Rating",
            "Difficulty", "Calories", "F_Name", "L_Name", "City", "Age"]

    # Create query
    query = "SELECT"
    col_str = ""  # For the return list later on
    for col in cols:
        query += f" {col},"
        col_str += f"{col}, "
    query = query[:-1]
    col_str = col_str[:-2]
    query += " FROM Recipes NATURAL JOIN Authors" 

    # Run query
    cur.execute(query)
    rows = cur.fetchall()

    # Create a list of strings to return
    results = [col_str]
    for row in rows:
        row_str = ""
        for i in range(len(row)):
            row_str += f"{row[i]}, "
        row_str = row_str[:-2]
        results.append(row_str)
    
    # Close connection
    con.close()

    # Return the list of results
    return results

def recipe_ingreds_query() -> list:
    """
    """

    # Create connection
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Create a list of column names to use
    cols = ["Recipe_Name", "Recipe_Description", "Created", "Recipe_Avg_Cost", "Rating",
            "Difficulty", "Calories", "Ingredient_Name", "Ingredient_Description",
            "Ingredient_Avg_Cost", "Ingredient_Shelf_Life"]

    # Create query
    query = "SELECT"
    col_str = ""  # For the return list later on
    for col in cols:
        query += f" {col},"
        col_str += f"{col}, "
    query = query[:-1]
    col_str = col_str[:-2]
    query += " FROM Recipes NATURAL JOIN RecipeIngredients NATURAL JOIN Ingredients" 

    # Run query
    cur.execute(query)
    rows = cur.fetchall()

    # Create a list of strings to return
    results = [col_str]
    for row in rows:
        row_str = ""
        for i in range(len(row)):
            row_str += f"{row[i]}, "
        row_str = row_str[:-2]
        results.append(row_str)
    
    # Close connection
    con.close()

    # Return the list of results
    return results

def recipes_full_query() -> list:
    """
    """

    # Create connection
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Create a list of column names to use
    cols = ["Recipe_Name", "Recipe_Description", "Created", "Recipe_Avg_Cost", "Rating",
            "Difficulty", "Calories", "F_Name", "L_Name", "City", "Age",
            "Ingredient_Name", "Ingredient_Description",
            "Ingredient_Avg_Cost", "Ingredient_Shelf_Life"]

    # Create query
    query = "SELECT"
    col_str = ""  # For the return list later on
    for col in cols:
        query += f" {col},"
        col_str += f"{col}, "
    query = query[:-1]
    col_str = col_str[:-2]
    query += " FROM Recipes" \
            " NATURAL JOIN Authors" \
            " NATURAL JOIN RecipeIngredients" \
            " NATURAL JOIN Ingredients"

    # Run query
    cur.execute(query)
    rows = cur.fetchall()

    # Create a list of strings to return
    results = [col_str]
    for row in rows:
        row_str = ""
        for i in range(len(row)):
            row_str += f"{row[i]}, "
        row_str = row_str[:-2]
        results.append(row_str)
    
    # Close connection
    con.close()

    # Return the list of results
    return results
