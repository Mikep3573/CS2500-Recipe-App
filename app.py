"""
Description:
Authors:
Date:
"""

# Dependencies
from flask import Flask, render_template

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
    return render_template("stat_queries.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)