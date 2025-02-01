import pandas as pd
import numpy as np
from io import BytesIO
import base64
import requests
import json
from flask import jsonify
from IPython.display import HTML, Image
# Pulling data from APIs, parsing JSON
from prompt_toolkit import HTML
from DisplayUtil import DisplayUtil

# amazonq-ignore-next-line
class BaseballDataProvider:
    def __init__(self):
        self.du = DisplayUtil()

    def get_all_baseball_leagues_level_competition(self):
        return jsonify({'message': 'Thank you'})

    def get_leagues(self):
        sports_endpoint_url = 'https://statsapi.mlb.com/api/v1/sports'

        sports = process_endpoint_url(sports_endpoint_url, 'sports')
        return self.du.display(sports)
       

    def get_seasons(self):
        seasons_endpoint_url = 'https://statsapi.mlb.com/api/v1/seasons/all?sportId=1'

        seasons = process_endpoint_url(seasons_endpoint_url, 'seasons')

        return self.du.display(seasons)

    def get_teams(self):
        # Use "?sportId=1" in following URL for MLB only
        teams_endpoint_url = 'https://statsapi.mlb.com/api/v1/teams?sportId=1'

        teams = process_endpoint_url(teams_endpoint_url, 'teams')

        return self.du.display(teams)
       

    def get_logo(self):
        #@title Get Team Logo

        # Pick single team ID to get logo for (default is 119 for Dodgers)
        team_id = 119 # @param {type:"integer"}

        # Get team logo using team_id
        team_logo_url = f'https://www.mlbstatic.com/team-logos/{team_id}.svg'

        # Display team logo (can change size if desired)

        return self.du.display(Image(url = team_logo_url, width=100, height=100))
        

    def get_team_roster(self, team_id:int, season:int):
        # Pick single team ID to get roster for (default is 118 for Dodgers)
        single_team_roster_url = f'https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?season={season}'

        single_team_roster = process_endpoint_url(single_team_roster_url, 'roster')

        return self.du.display(single_team_roster)
        
    #@param {type:"integer"}
    def get_all_players_one_season(self,season:int = 2024):

        single_season_players_url = f'https://statsapi.mlb.com/api/v1/sports/1/players?season={season}'

        players = process_endpoint_url(single_season_players_url, 'people')

        return self.du.display(players)

    #@title Single Player Information
    # Pick single player ID to get info for (default is 660271 for Shohei Ohtani)
    #@param {type:"integer"}
    def get_single_player(self,player_id:int = 660271):
      
        single_player_url = f'https://statsapi.mlb.com/api/v1/people/{player_id}/'

        single_player_info_json = json.loads(requests.get(single_player_url).content)

        return self.du.display(single_player_info_json)

    def get_player_headshot(self):
        return jsonify({'message': 'Thank you'})

    def get_game_schedule(self):
        return jsonify({'message': 'Thank you'})

    def single_game_data(self):
        return jsonify({'message': 'Thank you'})

    def single_play_info(self):
        return jsonify({'message': 'Thank you'})

    def get_mlb_fil_room_video_link(self,game_pk: str):
        if not game_pk:
            return jsonify({'error': 'No game_pk provided'}), 400
        
        #g ame_pk = '747066' #@param{type:"string"}

        single_game_feed_url = f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'

        single_game_info_json = json.loads(requests.get(single_game_feed_url).content)

        single_game_play = single_game_info_json['liveData']['plays']['currentPlay']

        single_game_play_id = single_game_play['playEvents'][-1]['playId']

        single_play_video_url = f'https://www.mlb.com/video/search?q=playid=\"{single_game_play_id}\"'

        return single_play_video_url;
        #r eturn jsonify({'message': 'Thank you'})

    def get_mlb_home_run_data(self, hr_play_id: str):

        #@title Get MLB Home Runs Data from Cloud Storage
        mlb_hr_csvs_list = [
        'https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/2016-mlb-homeruns.csv',
        'https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/2017-mlb-homeruns.csv',
        'https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/2024-mlb-homeruns.csv',
        'https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/2024-postseason-mlb-homeruns.csv'
        ]

        mlb_hrs = pd.DataFrame({'csv_file': mlb_hr_csvs_list})

        # Extract season from the 'csv_file' column using regex
        mlb_hrs['season'] = mlb_hrs['csv_file'].str.extract(r'/datasets/(\d{4})')

        mlb_hrs['hr_data'] = mlb_hrs['csv_file'].apply(pd.read_csv)

        for index, row in mlb_hrs.iterrows():
            hr_df = row['hr_data']
            hr_df['season'] = row['season']

        all_mlb_hrs = (pd.concat(mlb_hrs['hr_data'].tolist(), ignore_index = True)
        [['season', 'play_id', 'title', 'ExitVelocity', 'LaunchAngle', 'HitDistance',
            'video']])

        all_mlb_hrs['ExitVelocity'] = all_mlb_hrs['ExitVelocity'].str.extract(r'(\d+)').astype(float)

        #h r_play_id = "560a2f9b-9589-4e4b-95f5-2ef796334a94" # @param {type:"string"}

         # Get video URL for specific play from MLB dataset
        hr_video_url = all_mlb_hrs[all_mlb_hrs['play_id'] == hr_play_id]['video'].iloc[0]

        return HTML(f"""<video width="640" height="360" controls>
           <source src="{hr_video_url}" type="video/mp4">
           Your browser does not support the video tag.
         </video>""")
        
        #r eturn jsonify({'message': 'Thank you'})

    def get_single_home_run_video(self):
        return jsonify({'message': 'Thank you'})

    #def get_mlb_fan_fav_data(self):
    #    return jsonify({'message': 'Thank you'})

    #def get_most_followed_mlb_player(self):
    #    return jsonify({'message': 'Thank you'})

    #def get_mlb_fan_content_int_data(self):
    #    return jsonify({'message': 'Thank you'})
    
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

                        