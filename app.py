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

@app.route("/recipes_where")
def recipes_where():
    """
    """
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
    if num_val != None:
        not_num = False
        try:
            not_num = int(num_val)
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
    return render_template("recipes_edit.html")

@app.route("/stats")
def stats():
    """
    """
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