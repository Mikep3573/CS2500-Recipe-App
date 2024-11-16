from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import pandas as pd
import json
import plotly
from plotly import data
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64
import sqlite3
from sqlite3 import IntegrityError

"""
Similar to setting up a main in Python, this is how we initialize our app.py or our routing page in Flask!
"""
app = Flask(__name__)

"""
Route 1: Landing page 
This route is designated as the landing page route using @app.route("/"). In Flask, the @app.route() is used 
to map URLs to Python functions, and "/" represents the root URL, which is basically the landing/home page of a web application.

Uncomment the code below, then run the the python like you normally do or run 'python app.py' in terminal. 
Ensure that your terminal is in the same directory as app.py

Click the returned link in the terminal, and view the web page
"""
@app.route("/")
def index():
    # HTML files, which contain the structure and content of webpages,
    # are usually stored within a folder named 'templates' in Flask.
    # This separation helps Flask locate and render HTML templates when requested by routes.
    return render_template("landing.html")


"""
Route 2: Hello Jackie page
This route is created with @app.route('/hello-jackie') 
By defining a unique URL path like /hello-jackie, we can create targeted pages 
for specific content or actions within our web application!

Uncomment the code below, then run 'python app.py'
Add to the page address '/hello-jackie' and you should be navigated to the new webpage
"""
@app.route('/hello-jackie')
def hello_jackie():
    return "<p>Hello, Jackie!</p>"


"""
Route 3: Calculate and display sum of range(1, 10)
This route is set up with @app.route('/hello-sum') to calculate and display the sum of numbers in a specified range.

With this, you can see how Flask can perform computations and return results. This can be through predefined logic
such as below, or based on user interactions.

Uncomment the code below, then run 'python app.py'
Add to the page address '/hello-sum' and you should be navigated to the new webpage
"""
@app.route('/hello-sum')
def hello_sum():
    my_sum = sum(range(1, 10))  # Calculate sum
    return f"<p>My Sum is {my_sum}</p>"


"""
Route 4: Pass variables to template
This route, defined as @app.route("/index-with-sum"), illustrates passing variables from Python code to an HTML template.

By rendering a template ("sum.html") and passing the calculated sum (my_sum) as a variable, 
we can dynamically display data on the webpage! Pretty cool!

If you check 'sum.html' in the templates folder, you can see where the variable my_sum is being referenced from.

Uncomment the code below, then run 'python app.py'
Add to the page address '/index-with-sum' and you should be navigated to the new webpage
"""
@app.route("/index-with-sum")
def index_with_sum():
    my_sum = sum(range(1, 10))  # Calculate sum
    return render_template("sum.html", my_sum=my_sum)


"""
Route 5: Form handling (GET and POST)
This route handles both GET and POST requests using @app.route('/', methods=['GET', 'POST']), 
allowing users to interact with a form on the webpage.

When users submit the form, the route processes the form data (e.g., strings and integers) <-- GET
and generates a formatted response, showcasing form handling in Flask. <-- POST

Uncomment the code below, then run 'python app.py'
Add to the page address '/form' and you should be navigated to the new webpage
"""
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        form_str = request.form.get("form_str", None)
        form_int = request.form.get("form_int", None)

        # Process form data
        my_formatted_data = f"Concatenated String: {form_str}, Square of Integer: {int(form_int) ** 2}"
        return f"<p>{my_formatted_data}</p>"
        
        # Example: You can also pass in requested values to another page
        #return render_template("name_num.html", name=form_str, int=form_int, sqr=(int(form_int) ** 2))

    return render_template('form.html')


"""
Route 5: Plotting data with MatPlotLib
This route, designated as @app.route('/plot-data-mpl'), is responsible for generating and displaying a plot using MatPlotLib.

Here's a Flask integration using MatPlotLib to create graphs instead.

Uncomment the code below, then run 'python app.py'
Add to the page address '/plot-data-mpl' and you should be navigated to the new webpage
"""
# Route 5: Plot Data using Matplotlib
@app.route('/graph')
def graph():
    return render_template('plt.html')

# This will dynamically generate a graph for the graph page
@app.route('/graph_image')
def graph_image():
    # Generate data for plotting (these are just random numbers)
    data = {'Year': [2020, 2021, 2022, 2023, 2024],
            'Grade Avg': [100, 90, 95, 20, 80]}
    
    df = pd.DataFrame(data)

    # Create a simple line plot using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(df['Year'], df['Grade Avg'], marker='o')
    plt.xlabel('Year')
    plt.ylabel('Grade Avg')
    plt.title('Mish Grade Avg Over the Years')

    # Convert the graph to a base64 encoded string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image as a response with a type of image/png
    return make_response(img.read()), 200, {'Content-Type': 'image/png'}

"""
Alternate Method (Maybe don't use this): 
Personally I use the one above for rendering a graph that doesn't change very often. The browser is able the cache the 
image response above, so if you refresh the page it won't have to reload the graph.
"""
# Route 5: Plot Data using Matplotlib
@app.route('/graph_alt')
def graph_alt():
    # Generate data for plotting (these are just random numbers)
    data = {'Year': [2020, 2021, 2022, 2023, 2024],
            'Grade Avg': [100, 90, 95, 20, 80]}
    
    df = pd.DataFrame(data)

    # Create a simple line plot using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(df['Year'], df['Grade Avg'], marker='o')
    plt.xlabel('Year')
    plt.ylabel('Grade Avg')
    plt.title('Mish Grade Avg Over the Years')

    # Convert the graph to a base64 encoded string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image as a response with a type of image/png
    return render_template('plt.html', graph_image=img.read())


if __name__ == "__main__":
    app.run(debug=True)
