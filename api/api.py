from flask import Flask, render_template, request, jsonify
from api import create_app
from api.db_class import db
from api.league_generator.league import LeagueGenerator
import json

app = create_app()
db = db(app)
league_generator = LeagueGenerator(db)

# a simple page that says hello
@app.route("/hello")
def hello():
    return "Hello, World!"


# return a list of all teams as json
@app.route("/table", methods=["GET"])
def table():
    team_json = db.fetch_teams(json=True, sort=True)
    return team_json  # TODO : we may need to jsonify the team_list


@app.route("/generate_league", methods=["GET"])
def generate_league():
    league_generator.generate_matches(pick_random=True)
    team_json = db.fetch_teams(json=True)
    return team_json


@app.route("/next_week", methods=["GET"])
def get_next_week():
    print("NEXT WEEK")
    games = league_generator.play_a_week()
    game_list = []
    for game in games:
        match_dict = {"home": game[0], "away": game[1], "score": f"{game[2]}-{game[3]}"}
        game_list.append(match_dict)

    return jsonify(game_list)


@app.route("/is_done", methods=["GET"])
def is_done():
    is_done = league_generator.is_done
    print("IS_DONE:", is_done)
    if is_done:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/play_all", methods=["GET"])
def play_all():
    league_generator.play_all()
    return "Done"


@app.route("/predictions", methods=["GET"])
def predictions():
    predictions = league_generator.predict_championship(simulation_count=20)
    pred_list = []
    for pred in predictions:
        pred_dict = {"team": pred[0], "prediction": pred[1]}
        pred_list.append(pred_dict)
    print(f"## pred list == {pred_list}")
    return jsonify(pred_list)
