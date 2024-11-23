"""
Description: Holds generic functions that handle things like checking for numbers to making queries. For use anywhere in the program.
Authors: Michael Piscione and Walter Clay
Date: 11/23/24
"""

# Dependencies
import sqlite3
import datetime

def get_numeric_cols() -> list:
    """
    Executes a query for the names of all the numeric columns in all three tables (ignoring the junction table)

    Arguments:
    n/a

    Return:
    list: a list of the numeric columns
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
    Executes a query for the names of all the text columns in all three tables (ignoring the junction table)

    Arguments:
    n/a

    Return:
    list: a list of the text columns
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
    Executes a query for the names of all the columns in all three tables (ignoring the junction table)

    Arguments:
    n/a

    Return:
    list: a list of all the columns
    """

    # Just return a concatenated list of numeric and text columns
    return get_numeric_cols() + get_text_cols()

def associated_table(col: str) -> str:
    """
    Gets the names of the all the columns and returns the name of the table associated with an input
    column.

    Arguments:
    col: a string representing a column to find the table for

    Return:
    str: the table the column belongs to
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
    Executes a query on a given table, for a given column, with a given where operation (>, <, <=, etc) and a value.

    Arguments:
    col: The column to query against
    tbale: The table the column is located in
    op: the inequality operation used in the where clause
    val: the value used in the inequality in the where clause

    Return:
    list: a list of the results of the query as strings, plus some information beyond just the requested column
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
    Executes a query resulting in recipes and their authors.

    Arguments:
    n/a

    Return:
    list: a list of strings representing the result of the query
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
    Executes a query resulting in recipes and their ingredients.

    Arguments:
    n/a

    Return:
    list: a list of strings representing the result of the query
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
    Executes a query resulting in recipes, their authors, and their ingredients.

    Arguments:
    n/a

    Return:
    list: a list of strings representing the result of the query
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

def get_next_ID(in_id: str, table: str) -> str:
    """
    Given a table, the name of the table's primary key column, returns the next available primary key for use.

    Arguments:
    in_id: a string representing a certain table's primary key column name
    table: a string representing a table name

    Return:
    str: the next available primary key for use
    """
    
    # Connect to database
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Setup query
    query = f"SELECT {in_id} FROM {table} ORDER BY {in_id}"

    # Run query
    rows = cur.execute(query)
    ids = []
    for row in rows:
        ids.append(int(row[0]))

    # Close the connection
    con.close()

    # Return highest *_ID + 1
    max_id = max(ids)
    return str(max_id + 1)

def get_date() -> str:
    """
    Takes today's date and converts it into the date format present in the database.

    Arguments:
    n/a

    Return:
    str: today's date in the correct format
    """
    # Get the current date
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return f"{month}/{day}/{year}"

def get_authors() -> list:
    """
    Executes a query on the database resulting in all author's ID, first name, and last name

    Arguments:
    n/a

    Return:
    list: a 2D list of lists of strings representing the above fields for each author
    """

    # Connect to database
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Setup query
    query = "SELECT A_ID, F_Name, L_Name FROM Authors"

    # Run query
    rows = cur.execute(query)
    authors = []
    for row in rows:
        authors.append([row[0], row[1], row[2]])

    # Close the connection
    con.close()

    return authors

def get_ingredients() -> list:
    """
    Executes a query on the database resulting in all ingredient's ID and name

    Arguments:
    n/a

    Return:
    list: a 2D list of lists of strings representing the above fields for each ingredient
    """

    # Connect to database
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()

    # Setup query
    query = "SELECT I_ID, Ingredient_Name FROM Ingredients"

    # Run query
    rows = cur.execute(query)
    ingreds = []
    for row in rows:
        ingreds.append([row[0], row[1]])

    # Close the connection
    con.close()

    return ingreds

def issue_error(subject: str) -> str:
    """
    Given a subject, returns a message indicating the user forgot the 'subject'.

    Arguments:
    subject: string representing the subject of the sentence

    Return:
    str: message indicating the user forgot the 'subject'
    """

    return f"Whoops! You forgot {subject}. Please submit again"
