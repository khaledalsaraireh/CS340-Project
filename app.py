from flask import Flask, render_template, redirect       #type: ignore
from flask_mysqldb import MySQL                          #type: ignore
from flask import request                                #type: ignore
import os

# Citation for the following
# Date: 11/17/24
# Adapted from Flask Starter App Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_palmerj2'
app.config['MYSQL_PASSWORD'] = '0690' # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_palmerj2'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.j2")

@app.route("/index")
def index():
    return redirect("/")

if __name__ == "__main__":
    app.run(port=1122, debug=True)