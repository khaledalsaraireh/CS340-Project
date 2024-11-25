from flask import Flask, render_template, redirect       #type: ignore
from flask_mysqldb import MySQL                          #type: ignore
from flask import request                                #type: ignore

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
'''
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = '340testenv'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
''' # localhost db info, commented out 

# ---------- Home Page Routes Start ----------
@app.route("/")
def home():
    return render_template("index.j2")
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

@app.route("/delete_player/<int:id>")
def delete_player(id):
    query = "DELETE from Players WHERE playerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/players")


@app.route("/update_player", methods =["POST"])
def update_player():
    playerId = request.form["playerID"]
    playerName = request.form["playerName"]
    nflTeam = request.form["nfl-team"]
    fantasyPoints = request.form["fantasyPoints"]
    position = request.form["position"]
    query = "UPDATE Players SET Players.name = %s, Players.originTeamNFL = %s, Players.playerFantasyPoints = %s, Players.position = %s WHERE Players.playerID = %s"
    cur = mysql.connection.cursor()
    cur.execute(query, (playerName, nflTeam, fantasyPoints, position, playerId ))
    mysql.connection.commit()

    return redirect("/players")
# ---------- Players Routes End ----------



# ---------- Team Routes Start ----------
@app.route("/teams", methods = ["GET", "POST"])
def teams():
    if request.method == "GET":
        query = "SELECT userName FROM TeamOwners"
        cur = mysql.connection.cursor()
        cur.execute(query)
        team_owner_names = cur.fetchall()
        query = "SELECT teamID, teamName, wins, losses, teamFantasyPoints, TeamOwners.userName, Leagues.leagueName FROM Teams LEFT JOIN TeamOwners ON Teams.teamOwnerID = TeamOwners.teamOwnerID LEFT JOIN Leagues ON Teams.leagueID = Leagues.leagueID;"
        cur.execute(query)
        teams_data = cur.fetchall()

    if request.method == "POST":
        teamName = request.form["name"]
        wins = request.form["wins"]
        losses = request.form["losses"]
        fantasyPoints = request.form["teamFantasyPoints"]
        owner = request.form["teamOwnerName"]
        league = request.form["leagueName"]
        query = """
        INSERT INTO Teams (teamName, wins, losses, teamFantasyPoints, teamOwnerID, leagueID)
        VALUES (
            %s, 
            %s, 
            %s, 
            %s, 
            (SELECT teamOwnerID FROM TeamOwners WHERE userName = %s), 
            (SELECT leagueID FROM Leagues WHERE leagueName = %s)
        );
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (teamName, wins, losses, fantasyPoints, owner, league))
        mysql.connection.commit()
        return redirect("/teams")
    
    return render_template("teams.j2", team_owner_names=team_owner_names, teams_data = teams_data)

@app.route("/delete_team/<int:id>")
def delete_team(id):
    query = "DELETE Teams FROM Teams WHERE teamID = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/teams")

@app.route("/update_team", methods =["POST"])
def update_team():
    teamName = request.form["name"]
    wins = request.form["wins"]
    losses = request.form["losses"]
    fantasyPoints = request.form["teamFantasyPoints"]
    owner = request.form["teamOwnerName"]
    league = request.form["leagueName"]
    teamID = request.form["teamID"]
    query = """
    UPDATE Teams
    SET 
        teamName = %s, 
        wins = %s, 
        losses = %s, 
        teamFantasyPoints = %s, 
        teamOwnerID = (SELECT teamOwnerID FROM TeamOwners WHERE userName = %s), 
        leagueID = (SELECT leagueID FROM Leagues WHERE leagueName = %s)
    WHERE teamID = %s
    """
    cur = mysql.connection.cursor()
    cur.execute(query, (teamName, wins, losses, fantasyPoints, owner, league, teamID))
    mysql.connection.commit()

    return redirect("/teams")
# ---------- Team Routes End ----------



# ---------- Team Owner Routes Start ----------
@app.route("/team_owners", methods = ["GET", "POST"])
def team_owners():
    if request.method == "GET":
        query = """
        SELECT teamOwnerID, userName, email, dateOfBirth
        FROM TeamOwners;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
    if request.method == "POST":
        name = request.form["userName"]
        email = request.form["email"]
        dob = request.form["dateOfBirth"]
        query = """
        INSERT INTO TeamOwners (userName, email, dateOfBirth)
        VALUES (%s, %s, %s);
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (name, email, dob))
        mysql.connection.commit()
        return redirect("/team_owners")

    return render_template("team_owners.j2", team_owners_data = data)


@app.route("/delete_owner/<int:id>")
def delete_team_owner(id):
    query = "DELETE TeamOwners FROM TeamOwners WHERE teamOwnerID = %s"
    cur = mysql.connection.cursor() 
    cur.execute(query, (id, ))
    mysql.connection.commit()
    return redirect("/team_owners")


@app.route("/update_team_owner", methods = ["POST"])
def update_team_owner():
    name = request.form["userName"]
    email = request.form["email"]
    dob = request.form["dateOfBirth"]
    ownerID = request.form["teamOwnerID"]
    query = """
    UPDATE TeamOwners
    SET userName = %s, email = %s, dateOfBirth = %s
    WHERE teamOwnerID = %s;
    """
    cur = mysql.connection.cursor() 
    cur.execute(query, (name, email, dob, ownerID))
    mysql.connection.commit()
    return redirect("/team_owners")
# ---------- Team Owner Routes End ----------

if __name__ == "__main__":
    app.run(port=1122, debug=True)