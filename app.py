"""
Description:
Authors:
Date:
"""

# Dependencies
from flask import Flask, render_template, request, session
from gen_funcs import *
import statistics
import random
import string

# Setup the Flask app
app = Flask(__name__)

# Setup the session secret key
rand_num = random.randint(16, 32)
chars = string.ascii_letters + string.digits
app.secret_key = ''.join(random.choice(chars) for _ in range(rand_num))

@app.route("/")
def index():
    """
    """
    return render_template("index.html")

@app.route("/recipes")
def recipes():
    """
    """
    return render_template("recipes.html")

@app.route("/recipes_authors")
def recipes_authors():
    """
    """
    scroll_text = recipe_authors_query()
    return render_template("recipes_authors.html", scroll_text=scroll_text)

@app.route("/recipes_ingreds")
def recipes_ingreds():
    """
    """
    scroll_text = recipe_ingreds_query()
    return render_template("recipes_ingreds.html", scroll_text=scroll_text)

@app.route("/recipes_full")
def recipes_full():
    """
    """
    scroll_text = recipes_full_query()
    return render_template("recipes_full.html", scroll_text=scroll_text)

@app.route("/recipes_where")
def recipes_where():
    """
    """

    # Get a list of all the columns available
    cols = [col[0] for col in get_all_cols()]
    return render_template("recipes_where.html", cols=cols)

@app.route("/where_query", methods=['POST', 'GET'])
def where_query():
    """
    """

    # Get selected column and setup the session
    selected_col = request.form.get('selected_column')
    selected_comp = request.form.get('selected_comp')
    selected_t_comp = request.form.get('selected_t_comp')
    text_val = request.form.get('text-val')
    num_val = request.form.get("num-val")

    # This is to store the user's values between calls to this function
    # Because all of these are local variables and because the form updates as the user inputs more
    # information, we call this function many times therefore losing the values in each iteration.
    # We thus store them in the session dictionary (as defined by Flask) to keep continuity
    if selected_col:
        session['selected_col'] = selected_col
    if selected_comp:
        session['selected_comp'] = selected_comp
    if selected_t_comp:
        session['selected_t_comp'] = selected_t_comp
    if text_val:
        session['text_val'] = text_val
    if num_val:
        session['num_val'] = num_val
    if 'cols' not in session.keys():
        session['cols'] = [col[0] for col in get_all_cols()]
    if 'comps' not in session.keys():
        session['comps'] = ['=', '!=', '>', '>=', '<', '<=']
    if 't_comps' not in session.keys():
        session['t_comps'] = ['=', '!=']

    # Check if the column is text or numeric
    if not selected_comp and not selected_t_comp:
        text_cols = [col[0] for col in get_text_cols()]
        session['text'] = selected_col in text_cols

    # Update the list of columns if the user selected a column
    if selected_col:
        cols = [col[0] for col in get_all_cols()]
        cols.remove(selected_col)
        cols = [selected_col] + cols

        # Save the updated list to session
        session['cols'] = cols
    
    # Update the list of comparison operators
    # if the user selected a numeric comparison operator
    if selected_comp:
        comps = ['=', '!=', '>', '>=', '<', '<=']
        comps.remove(selected_comp)
        comps = [selected_comp] + comps

        # Save the updated list to session
        session['comps'] = comps

    # Update the list of comparison operators
    # if the user selected a text comparison operator
    if selected_t_comp:
        t_comps = ['=', '!=']
        t_comps.remove(selected_t_comp)
        t_comps = [selected_t_comp] + t_comps

        # Save the updated list to session
        session['t_comps'] = t_comps

    # Check if num_val is numeric
    not_num = False
    if num_val is not None:
        not_num = False
        try:
            num_val = int(num_val)
        except ValueError:
            not_num = True

    # If the user gave a value for the where clause, run the query and return the results
    q_result = []
    if text_val or (num_val and not not_num):
        table = associated_table(session['selected_col'])
        assert table  # To check that the function picked a table and didn't return an empty string
        if text_val:  # Use the text operator and text value
            q_result = run_where_query(col=session['selected_col'], 
                                       table=table, 
                                       op=session['selected_t_comp'], 
                                       val=text_val)
        else:
            q_result = run_where_query(col=session['selected_col'], 
                                       table=table, 
                                       op=session['selected_comp'], 
                                       val=num_val)

    return render_template("recipes_where.html",
                           cols=session['cols'],
                           text=session['text'],
                           comps=session['comps'],
                           t_comps=session['t_comps'],
                           scroll_text=q_result,
                           not_num=not_num)

@app.route("/recipes_edit")
def edit_recipes():
    """
    """
    # TODO: Just Removing a row (give them a dropdown list for names of recipe, author, or ingredient)
            # Make sure to remove ingredient id from RecipeIngredients
            # If removing Author, make sure to remove all recipes the author wrote (maybe issue a message this will happen)
    # TODO: Modifying anything should be fine, they just can't modify an _ID column (just give them the same drop down like in Filter Recipes)
    return render_template("recipes_edit.html")

@app.route("/add_recipe")
def add_recipe():
    """
    """
    # Get the columns, author, and ingredients list to display to the user
    cols = ["Name", "Description", "Average Cost", "Rating (1-5)", "Difficulty (1-5)", "Calories"]
    authors = get_authors()
    ingreds = get_ingredients()

    return render_template("add_recipe.html", cols=cols, authors=authors, ingreds=ingreds)

@app.route("/add_rec_submission", methods=["Post"])
def add_rec_submission():
    """
    """

    # Get the user's input
    forgot = False
    message = ""
    # Author ID
    a_id = request.form.get("author")

    # Column values
    name = request.form.get("Name")
    if not name:
        message = issue_error("name")
        forgot = True
    desc = request.form.get("Description")
    if not desc:
        message = issue_error("description")
        forgot = True
    avg_cost = request.form.get("Average Cost")
    if not avg_cost:
        message = issue_error("average cost")
        forgot = True
    rating = request.form.get("Rating (1-5)")
    if not rating:
        message = issue_error("rating")
        forgot = True
    diff = request.form.get("Difficulty (1-5)")
    if not diff:
        message = issue_error("difficulty")
        forgot = True
    cal = request.form.get("Calories")
    if not cal:
        message = issue_error("calories")
        forgot = True

    # Ingredients
    ingred_ids = request.form.getlist("ingreds")
    if not ingred_ids:
        message = issue_error("ingredients")
        forgot = True

    # If nothing was forgotten, create the query
    if not forgot:
        # Get the next available R_ID
        r_id = get_next_ID("R_ID", "Recipes")

        # Get today's date
        created = get_date()
        q_rec = "INSERT INTO Recipes (R_ID, A_ID, Recipe_Name, Recipe_Description, Created, Recipe_Avg_Cost, Rating, Difficulty, Calories) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Get the RecipeIngredients query
        q_rec_ing = "INSERT INTO RecipeIngredients ('R_ID', 'I_ID') VALUES (?, ?)"

        # Open connection to database
        con = sqlite3.connect("recipe_app.db")
        cur = con.cursor()

        # Insert values into the Recipes table
        cur.execute(q_rec, (r_id, a_id, name, desc, created, avg_cost, rating, diff, cal))

        # Insert values into the junction table
        for ingred_id in ingred_ids:
            cur.execute(q_rec_ing, (r_id, ingred_id))

        # Commit and close connection to database
        con.commit()
        con.close()

    return render_template("index.html", forgot=forgot, error_message=message)

@app.route("/add_author")
def add_author():
    """
    """
    # Get the columns to change
    cols = ["First Name", "Last Name", "City", "Age"]
    return render_template("add_author.html", cols=cols)

@app.route("/add_auth_submission", methods=["Post"])
def add_auth_submission():
    """
    """
    # Get the user's inputs
    forgot = False
    message = ""
    f_name = request.form.get("First Name")
    if not f_name:
        message = issue_error("first name")
        forgot = True
    l_name = request.form.get("Last Name")
    if not l_name:
        message = issue_error("last name")
        forgot = True
    city = request.form.get("City")
    if not city:
        message = issue_error("city")
        forgot = True
    age = request.form.get("Age")
    if not age:
        message = issue_error("age")
        forgot = True

    # If nothing was forgotten, create the query
    if not forgot:
        # Get the next available A_ID
        a_id = get_next_ID("A_ID", "Authors")

        # Open the connection
        con = sqlite3.connect("recipe_app.db", isolation_level=None)
        cur = con.cursor()

        # Make the Authors query
        a_query = "INSERT INTO Authors (A_ID, F_Name, L_Name, City, Age) VALUES (?, ?, ?, ?, ?)"
        cur.execute(a_query, (a_id, f_name, l_name, city, age))

        # Close the connection
        con.commit()
        con.close()

    # Issue a message
    return render_template("index.html", forgot=forgot, error_message=message)

@app.route("/add_ingredient")
def add_ingredient():
    """
    """
    # Get the columns to change
    cols = ["Name", "Description", "Average Cost", "Shelf Life"]
    return render_template("add_ingredient.html", cols=cols)

@app.route("/add_ingred_submission", methods=["Post"])
def add_ingred_submission():
    """
    """
    # Get the user's inputs
    forgot = False
    message = ""
    name = request.form.get("Name")
    if not name:
        message = issue_error("name")
        forgot = True
    desc = request.form.get("Description")
    if not desc:
        message = issue_error("description")
        forgot = True
    avg_cost = request.form.get("Average Cost")
    if not avg_cost:
        message = issue_error("average cost")
        forgot = True
    shelf_life = request.form.get("Shelf Life")
    if not shelf_life:
        message = issue_error("shelf life")
        forgot = True

    # If nothing was forgotten, create the query
    if not forgot:
        # Get the next available A_ID
        i_id = get_next_ID("I_ID", "Ingredients")

        # Open the connection
        con = sqlite3.connect("recipe_app.db", isolation_level=None)
        cur = con.cursor()

        # Make the Authors query
        a_query = "INSERT INTO Ingredients (I_ID, Ingredient_Name, Ingredient_Description, Ingredient_Avg_Cost, Ingredient_Shelf_Life) VALUES (?, ?, ?, ?, ?)"
        cur.execute(a_query, (i_id, name, desc, avg_cost, shelf_life))

        # Close the connection
        con.commit()
        con.close()

    # Issue a message
    return render_template("index.html", forgot=forgot, error_message=message)

@app.route("/stats")
def stats():
    """
    """
    # TODO: Author vs. Average Recipe Rating should be a scatterplot
    # TODO: Recipe Rating Distribution should be a bar chart (rating is technically a categorical variable)
    # TODO: Calories by Difficulty Level should be box plots (one for each difficulty level)
    return render_template("stats.html")

@app.route("/stat_queries")
def stat_queries():
    """
    """
    # Get the numerical columns in the data
    cols = [tup[0] for tup in get_numeric_cols()]
    
    return render_template("stat_queries.html", cols=cols, result='null')

@app.route("/stat_choice", methods=['POST'])
def stat_choice():
    """
    """

    # Get the selected column and aggregate function
    selected_col = request.form.get('selected_column')
    selected_agg = request.form.get('selected_agg')
    
    # Get the possible columns and table pairs
    tups = get_numeric_cols()

    # Get the table of the selected column
    # Result shouldn't need to be checked since we know the set of all possible choices from the user
    table = ""
    for i in range(len(tups)):
        if tups[i][0] == selected_col:
            table = tups[i][1]

    # Get the result of their query
    con = sqlite3.connect("recipe_app.db", isolation_level=None)
    cur = con.cursor()
    if selected_agg not in ("STD_DEV", "MEDIAN"):
        # For MAX, MIN, and AVG
        cur.execute(
                f"SELECT {selected_agg}({selected_col})" \
                f" FROM {table}"
            )
        result = round(cur.fetchone()[0], 2)  # Round to 2 decimal places
    elif selected_agg == "MEDIAN":
        # For Median
        rows = cur.execute(f"SELECT {selected_col}" \
                           f" FROM {table}")
        nums = [row[0] for row in rows]
        result = statistics.median(nums)
        result = round(result, 2)  # Round to 2 decimal places
    else:
        # For Standard Deviation
        rows = cur.execute(f"SELECT {selected_col}" \
                           f" FROM {table}")
        nums = [row[0] for row in rows]
        result = statistics.stdev(nums)
        result = round(result, 2)  # Round to 2 decimal places
    
    # Update the list of columns
    cols = [col[0] for col in get_numeric_cols()]
    cols.remove(selected_col)
    cols = [selected_col] + cols
    
    return render_template("stat_queries.html", cols=cols, result=result)

# Run the app
if __name__ == "__main__":
    # Start the app
    app.run(debug=True)