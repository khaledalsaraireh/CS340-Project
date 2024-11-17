from flask import Flask, render_template, redirect, json #type: ignore
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

# ---------- Home Page Routes Start ----------
@app.route("/")
def home():
    return render_template("index.j2")

@app.route("/index")
def index():
    return redirect("/")
# ---------- Home Page Routes End ----------




# ---------- Players Routes Start ----------
@app.route("/players", methods=["POST", "GET"])
def players():

    if request.method == "POST":
        player_name = request.form["playerName"]
        nfl_team = request.form["nfl-team"]
        fantasy_points = request.form["fantasyPoints"]
        position = request.form["position"]

        query = "INSERT INTO Players (name, originTeamNFL, playerFantasyPoints, position) VALUES (%s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (player_name, nfl_team, fantasy_points, position))
        mysql.connection.commit()
        
        return redirect("/players")
    
    if request.method == "GET":
        query = "SELECT playerID, name, originTeamNFL, playerFantasyPoints, position FROM Players"
        cur = mysql.connection.cursor()
        cur.execute(query)
        player_data = cur.fetchall()

    return render_template("players.j2", player_data = player_data)

# ---------- Players Routes End ----------
if __name__ == "__main__":
    app.run(port=1122, debug=True)