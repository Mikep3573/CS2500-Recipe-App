"""
Description:
Authors:
Date:
"""

# Dependencies
from flask import Flask, render_template, request
from gen_funcs import *
import statistics

# Setup the Flask app
app = Flask(__name__)

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
                f"FROM {table}"
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
    
    
    return render_template("stat_queries.html", cols=[tup[0] for tup in tups], result=result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)