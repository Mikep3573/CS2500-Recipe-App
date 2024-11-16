# Intro To Flask!

## Objective:
The objective of this lab assignment is to gain hands-on experience with Flask by creating
web pages that display athelete information from the Olympics database ('olympics.db'). You will
learn to:
- create HTML templates
- create links between web pages
- execute SQL queries to retrieve data
- display data in tables and graphs using Flask

## Getting Started:
* (Optional but recommended) Create a new venv, activate it and install the requirements into it using the commands below:
    * `python3 -m venv venv`
    * linux/mac -> `source venv/bin/activate`, windows -> `venv\Scripts\activate`
* Install the required dependencies:
    * `pip install -r requirements.txt`

## Moving on:
(If this is an Alt Timeline where I gave you a personal walk through of the code- just move on)

Before we start the lab, we'll be taking a self guided approach to learning how flask works. You were given a file called 'app.py' inside here
is commented out code, outlining different functionality that can done with flask. Take a moment to read through the comments and
experiment with the code. Afterwards, you'll follow through with the rest of the lab to display few web pages.


## Lab Assignment:
Based on what you've learnt so far:

### 0) Mini Step
We're going to need the olympic.db for this assignment. If you already have it, go ahead and put it in this folder. If not, run 'olympic.py' which will create olympic.db with a table named 'olympic'

### 1) Create a New HTML Page (table.html)
* Using the provided HTML template below, create a new HTML page called table.html within the templates folder.
* Replace [Name Here] in the title block with an appropriate title for your page.
* We will add the necessary HTML code in the designated block in a later step

```
{% extends 'base.html' %}

{% block title %}[Name Here]{% endblock %}

<!-- Block Begins -->
{% block content %}

<div class= "container">

    <!-- HTML here -->

</div>

{% endblock %}
<!-- Block Ends -->
```

### 2) Modify landing.html
* Update the landing.html file to include links to the newly created table.html and another page called graph.html.
* Hint: Follow HTML syntax to create hyperlinks (`<a>` tags) with text and URL

### 3) Display Athlete Information in Table
#### Step 1: Retrieve Information from Database
In `app.py`, you'll first write a SQL query function to retrieve athlete info from `olympics.db`. Write a SQL query that retrieves the names of athletes, their sex, the name of the team they belong to, and the name of the game they
participated in. Sort the results by the athlete's name in ascending order.

```
# Function to execute SQL query and retrieve athlete information
def get_athlete_info():
    conn = sqlite3.connect('olympics.db')
    cursor = conn.cursor()
    cursor.execute('''
        ### Query Goes Here ###
    ''')
    athlete_data = cursor.fetchall()
    conn.close()
    return athlete_data
```

#### Step 2: Link the HTML Route in app.py
Update the app.py file to include a route that renders the table.html template and passes the athlete information retrieved from the database.

#### Step 3: Modify table.html
Modify table.html to display information retrieved from the database in table format.

```
<!-- Table formatting -->
<table class="table table-striped">
        <!-- Table Header -->
        <thead>
            <tr>
                <th>Name</th>
                <th>Sex</th>
                <th>Team</th>
                <th>Game</th>
            </tr>
        </thead>

        <!-- Table Body -->
        <tbody>
            <!-- We get athelete_info from the HTML Route in app.py, then we loop through it -->
            {% for athlete in athlete_info %}
            <!-- Table Rows -->
            <tr>
                <td>{{ athlete[0] }}</td>
                <td>{{ athlete[1] }}</td>
                <td>{{ athlete[2] }}</td>
                <td>{{ athlete[3] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
```

### 4) Create and Display a Graph
* Write a Python function in app.py that generates a graph representing the number of female athletes versus the number of male athletes.
    * Hint: Check out the graph route for help.
* Display the generated graph on the `graph.html` (Feel free to use plt.html as a reference)


## Additional Resources:
[Bootstrap CSS Cheatsheet](https://getbootstrap.com/docs/5.0/examples/cheatsheet/)

[Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)

[HTML Guide](https://www.codecademy.com/learn/learn-html/modules/learn-html-elements/cheatsheet)



