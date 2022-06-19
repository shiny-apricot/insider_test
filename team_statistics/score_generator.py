import random
import itertools
import pandas as pd
import os


class ScoreGenerator:
    def __init__(self, avg_file="avg_goals.csv", std_file="std_goals.csv"):
        # get avg and std csv files
        avg_path = os.path.join(os.getcwd(), "team_statistics", avg_file)
        std_path = os.path.join(os.getcwd(), "team_statistics", std_file)
        self.df_avg = pd.read_csv(avg_path, index_col=0)
        self.df_std = pd.read_csv(std_path, index_col=0)

    def generate_matches(self):
        # create all the permutations of 20 teams
        try:
            team_list = list(self.df_avg.index)
        except KeyError:
            print("No teams found in avg_goals.csv")
            return
        self.team_list_perm = list(itertools.permutations(team_list, 2))
        return self.team_list_perm

    def generate_scores(self):
        team_list_perm = self.generate_matches()
        # decide the scores for each match by considering the average, standard deviation, away and home
        scores = []
        for match in team_list_perm:
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
            scores.append([match[0], match[1], score_home, score_away])
        return scores
