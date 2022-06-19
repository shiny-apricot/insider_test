import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "instance", "database.db")
print("database path:", db_path)

conn = sqlite3.connect(db_path)
print("Opened database successfully")

# create team table with "team_name", "played", "won", "drown", "lost", "GF", "GA", "GD", "points"
conn.execute(
    "CREATE TABLE teams (team_name TEXT, played INTEGER, won INTEGER, drown INTEGER, lost INTEGER, GF INTEGER, GA INTEGER, GD INTEGER, points INTEGER)"
)
print("Table created successfully")

# add some teams to the table
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Arsenal', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Bournemouth', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Brighton', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Burnley', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Cardiff', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Chelsea', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Crystal Palace', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Everton', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Fulham', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Huddersfield', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Leicester', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Bournemouth', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Liverpool', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Man City', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Man United', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Newcastle', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Southampton', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Tottenham', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Watford', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('West Ham', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.execute(
    "INSERT INTO teams (team_name, played, won, drown, lost, GF, GA, GD, points) VALUES ('Wolves', 0, 0, 0, 0, 0, 0, 0, 0)"
)
conn.commit()
print("Records created successfully")


conn.close()
