import pandas as pd
import numpy as np

# Pulling data from APIs, parsing JSON
import requests
import json

# Interfacing w/ Cloud Storage from Python
from google.cloud import storage

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import HTML, Image

from flask import Flask, jsonify, request
from HTMLGenerator import HTMLGenerator
from BaseballDataProvider import BaseballDataProvider

app = Flask(__name__)

# Example usage
provider = BaseballDataProvider()

@app.route('/', methods=['GET'])
def home():
    return "Select one of the following options: teams or prediction"

@app.route('/predict', methods=['GET'])
def predict():
    # Future implementation for prediction logic
    generator = HTMLGenerator()
    return generator.generate_html("https://statsapi.mlb.com/api/v1/sports");
    # r eturn jsonify({'message': 'Prediction logic not implemented yet.'})

@app.route('/team', methods=['GET'])
def get_team():
    teamname = request.args.get('teamname')
    if not teamname:
        return jsonify({'error': 'No team name provided'}), 400
    
    return jsonify({'teamname': teamname})

@app.route('/all_baseball_leagues_level_competition', methods=['GET'])
def all_baseball_leagues_level_competition():
    return provider.get_all_baseball_leagues_level_competition()

@app.route('/leagues', methods=['GET'])
def leagues():
    return provider.get_leagues()

@app.route('/seasons', methods=['GET'])
def seasons():
    return provider.get_seasons()

@app.route('/teams', methods=['GET'])
def teams():
    return provider.get_teams()

@app.route('/logo', methods=['GET'])
def logo():
    return provider.get_logo()

@app.route('/team_roster', methods=['GET'])
def team_roster():
    return provider.get_team_roster()

@app.route('/all_players_one_season', methods=['GET'])
def all_players_one_season():
    return provider.get_all_players_one_season()

@app.route('/single_player', methods=['GET'])
def single_player():
    return provider.get_single_player()

@app.route('/player_headshot', methods=['GET'])
def player_headshot():
    return provider.get_player_headshot()

@app.route('/game_schedule', methods=['GET'])
def game_schedule():
    return provider.get_game_schedule()

@app.route('/single_game_data', methods=['GET'])
def single_game_data():
    return provider.single_game_data()

@app.route('/single_play_info', methods=['GET'])
def single_play_info():
    return provider.single_play_info()

@app.route('/mlb_fil_room_video_link', methods=['GET'])
def mlb_fil_room_video_link():
    return provider.get_mlb_fil_room_video_link()

@app.route('/mlb_home_run_data', methods=['GET'])
def mlb_home_run_data():
    return provider.get_mlb_home_run_data()

@app.route('/single_home_run_video', methods=['GET'])
def single_home_run_video():
    return provider.get_single_home_run_video()

@app.route('/mlb_fan_fav_data', methods=['GET'])
def mlb_fan_fav_data():
    return provider.get_mlb_fan_fav_data()

@app.route('/most_followed_mlb_player', methods=['GET'])
def most_followed_mlb_player():
    return provider.get_most_followed_mlb_player()

@app.route('/mlb_fan_content_int_data', methods=['GET'])
def mlb_fan_content_int_data():
    return provider.get_mlb_fan_content_int_data()

if __name__ == '__main__':
    app.run()

#@title Function to Process Results from Various MLB Stats API Endpoints
def process_endpoint_url(endpoint_url, pop_key=None):
  """
  Fetches data from a URL, parses JSON, and optionally pops a key.

  Args:
    endpoint_url: The URL to fetch data from.
    pop_key: The key to pop from the JSON data (optional, defaults to None).

  Returns:
    A pandas DataFrame containing the processed data
  """
  json_result = requests.get(endpoint_url).content

  data = json.loads(json_result)

   # if pop_key is provided, pop key and normalize nested fields
  if pop_key:
    df_result = pd.json_normalize(data.pop(pop_key), sep = '_')
  # if pop_key is not provided, normalize entire json
  else:
    df_result = pd.json_normalize(data)

  return df_result

