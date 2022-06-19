import random
import itertools
import pandas as pd
import os
from flask import jsonify
import json


class Team:
    def __init__(self, team_name, played, won, drown, lost, GF, GA, GD, points):
        self.team_name = team_name
        self.played = played
        self.won = won
        self.drown = drown
        self.lost = lost
        self.GF = GF
        self.GA = GA
        self.GD = GD
        self.points = points


class LeagueGenerator:
    def __init__(self, db, avg_file="avg_goals.csv", std_file="std_goals.csv"):
        self.db = db
        self.team_names = []
        self.scores = []
        self.week = 1
        self.is_done = False
        # get avg and std csv files of all teams in Premier League
        try:
            avg_path = os.path.join(os.getcwd(), "league_generator", avg_file)
            std_path = os.path.join(os.getcwd(), "league_generator", std_file)
        except FileNotFoundError:
            print(f"No {avg_file} or {std_file} found")
            return

        self.df_avg = pd.read_csv(avg_path, index_col=0)
        self.df_std = pd.read_csv(std_path, index_col=0)

    def pick_random_teams(self, team_count=4):
        self.team_count = team_count
        try:
            team_list = list(self.df_avg.index)
            self.team_names = random.sample(team_list, team_count)
        except ValueError:
            print("No teams found in the database")
            return
        # drop the database if it exists
        self.db.drop_table()
        self.db.create_table()
        # insert the random teams into the database
        for team in self.team_names:
            team_obj = Team(team, 0, 0, 0, 0, 0, 0, 0, 0)
            self.db.insert_team(team_obj)
        return self.team_names

    def generate_matches(self, pick_random=False, return_json=False):
        """
        Generate all the possible matches of teams.
        """
        # reset the league
        self.is_done = False
        self.week = 1

        if pick_random:
            self.pick_random_teams(team_count=4)

        try:
            # create all the permutations of team pairs
            self.team_match_perm = list(itertools.permutations(self.team_names, 2))
            self.scores = self.generate_scores()
            if return_json:
                team_dict = dict(pairs=self.team_match_perm)
                return json.dumps(team_dict)
            else:
                return self.team_match_perm
        except ValueError:
            print("No teams are picked. Try func => pick_random_teams()")
            return

    def generate_scores(self):
        # decide the scores for each match by considering the average, standard deviation, away and home
        for match in self.team_match_perm:
            # calculate the scores for each match
            # score for home team
            score_home = random.normalvariate(
                self.df_avg.loc[match[0]]["attack_avg_home"],
                self.df_std.loc[match[0]]["attack_std_home"],
            )
            # score for away team
            score_away = random.normalvariate(
                self.df_avg.loc[match[1]]["attack_avg_away"],
                self.df_std.loc[match[1]]["attack_std_away"],
            )
            # round the scores to closest integer
            score_home = round(score_home)
            if score_home < 0:
                score_home = 0
            score_away = round(score_away)
            if score_away < 0:
                score_away = 0
            # append the scores to the list
            self.scores.append([match[0], match[1], score_home, score_away])
        return self.scores

    def play_a_week(self):
        if self.week >= 7:
            self.is_done = True
            print("League is already done")
            return []

        teams_left = self.team_names.copy()
        game_list = []
        # enumerate from reverse
        game_count = len(self.scores)
        for game_index in reversed(range(game_count)):
            print(f"Game index {game_index}")
            print(f"Scores: {self.scores}")
            game = self.scores[game_index]
            if game[0] in teams_left and game[1] in teams_left:
                self.scores.pop(game_index)
                game_list.append(game)
                teams_left.remove(game[0])
                teams_left.remove(game[1])
                if len(game_list) == 2:
                    break

        self.update_stats(game_list)
        self.week += 1
        if self.week == 6:
            self.is_done = True
        if self.week >= 7:
            return []
        return game_list

    def play_all(self):
        for i in range(7):
            self.play_a_week()

    # predict championship based on df_avg and df_std
    def predict_championship(self):
        # get the top 4 teams
        teams = self.db.fetch_teams(sorted=True)
        # get the average and standard deviation of the top 4 teams
        avg_top4 = self.df_avg.loc[teams[:4]]
        std_top4 = self.df_std.loc[teams[:4]]
        # predict the championship
        championship = []

    def update_stats(self, game_list):
        for game in game_list:
            # determine who is won
            if game[2] == game[3]:
                self.db.increment_team_stats(
                    team_name=game[0],
                    drown=1,
                    played=1,
                    points=1,
                    GF=game[2],
                    GA=game[3],
                    GD=game[2] - game[3],
                )
                self.db.increment_team_stats(
                    team_name=game[1],
                    drown=1,
                    played=1,
                    points=1,
                    GF=game[3],
                    GA=game[2],
                    GD=game[3] - game[2],
                )
            elif game[2] > game[3]:
                winner = game[0]
                loser = game[1]
                self.db.increment_team_stats(
                    team_name=winner,
                    played=1,
                    won=1,
                    GF=game[2],
                    GA=game[3],
                    points=3,
                    GD=game[2] - game[3],
                )
                self.db.increment_team_stats(
                    team_name=loser,
                    played=1,
                    lost=1,
                    GF=game[3],
                    GA=game[2],
                    points=0,
                    GD=game[3] - game[2],
                )
            elif game[2] < game[3]:
                winner = game[1]
                loser = game[0]
                self.db.increment_team_stats(
                    team_name=winner,
                    played=1,
                    won=1,
                    GF=game[3],
                    GA=game[2],
                    points=3,
                    GD=game[3] - game[2],
                )
                self.db.increment_team_stats(
                    team_name=loser,
                    played=1,
                    lost=1,
                    GF=game[2],
                    GA=game[3],
                    points=0,
                    GD=game[2] - game[3],
                )
