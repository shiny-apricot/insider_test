# import sqlite
import sqlite3
import os


class db:
    def __init__(self, app, db_filename="database.db"):
        self.app = app
        self.conn = None
        self.db_path = os.path.join(self.app.instance_path, db_filename)

    def drop_table(self, table="teams"):
        """
        Drop the table if it exists.
        The connection has to be established inside this function.
        """
        # read the database.db file in sqlite format
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table}")

    def create_table(self, db_filename="database.db", table="teams", drop=False):
        """
        Create the table if it doesn't exist.
        The connection has to be established inside this function.
        """
        db_path = os.path.join(self.app.instance_path, db_filename)
        # read the database.db file in sqlite format
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            f"""CREATE TABLE IF NOT EXISTS {table} (
                team_name TEXT,
                played INTEGER,
                won INTEGER,
                drown INTEGER,
                lost INTEGER,
                GF INTEGER,
                GA INTEGER,
                GD INTEGER,
                points INTEGER
            )"""
        )
        conn.commit()
        conn.close()

    def insert_team(self, team):
        """
        Insert a team into the database.
        The connection has to be established inside this function.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            f"INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                team.team_name,
                team.played,
                team.won,
                team.drown,
                team.lost,
                team.GF,
                team.GA,
                team.GD,
                team.points,
            ),
        )
        conn.commit()
        conn.close()

    def increment_team_stats(
        self,
        points,
        team_name,
        played=1,
        won=0,
        drown=0,
        lost=0,
        GF=0,
        GA=0,
        GD=0,
        table_name="teams",
    ):
        """
        Increment the stats of a team.
        The connection has to be established inside this function.
        """
        if team_name is None:
            print("team_name is None")
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            f"UPDATE {table_name} SET played = played + ?, won = won + ?, drown = drown + ?, lost = lost + ?, GF = GF + ?, GA = GA + ?, GD = GD + ?, points = points + ? WHERE team_name = ?",
            (played, won, drown, lost, GF, GA, GD, points, team_name),
        )
        conn.commit()
        conn.close()

    def fetch_teams(
        self, json=False, db_filename="database.db", table_name="teams", sort=False
    ):
        """
        Return a list of all teams in the database.
        The connection has to be established inside this function.
        """
        db_path = os.path.join(self.app.instance_path, db_filename)
        conn = sqlite3.connect(db_path)

        team_list = []
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()

        for row in rows:
            team_dict = {
                "team_name": row[0],
                "played": row[1],
                "won": row[2],
                "drown": row[3],
                "lost": row[4],
                "GF": row[5],
                "GA": row[6],
                "GD": row[7],
                "points": row[8],
            }
            team_list.append(team_dict)

        if sort:
            # if two team has the same point, sort by GD, if GD is equal, sort by GF
            team_list.sort(key=lambda x: x["GF"], reverse=True)
            team_list.sort(key=lambda x: x["GD"], reverse=True)
            team_list.sort(key=lambda x: x["points"], reverse=True)

        if json:
            return dict(teams=team_list)
        # else
        return team_list

    # copy all the information from the table to a new table
    def copy_table(self, table="teams", new_table="teams_copy"):
        """
        Copy the table to a new table.
        The connection has to be established inside this function.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        c.execute(f"DROP TABLE IF EXISTS {new_table}")
        c.execute(
            f"""CREATE TABLE IF NOT EXISTS {new_table} (
                team_name TEXT,
                played INTEGER,
                won INTEGER,
                drown INTEGER,
                lost INTEGER,
                GF INTEGER,
                GA INTEGER,
                GD INTEGER,
                points INTEGER
            )"""
        )
        for row in rows:
            c.execute(
                f"INSERT INTO {new_table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                ),
            )
        conn.commit()
        conn.close()

