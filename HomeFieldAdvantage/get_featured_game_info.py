import pandas as pd
import numpy as np


def get_featured_game_vector(engine, home_team, away_team, game_date):

    desired_features = ['extra_points_made_Home', 'field_goals_made_Home', 'overtime_Home',
                        'pass_touchdowns_Home', 'pass_yards_Home',
                        'pass_yards_per_attempt_Home', 'points_scored_Home',
                        'quarterback_rating_Home', 'rush_attempts_Home', 'rush_touchdowns_Home',
                        'rush_yards_Home', 'rush_yards_per_attempt_Home',
                        'third_down_attempts_Home', 'third_down_conversions_Home',

                        'extra_points_made_Away', 'field_goals_made_Away', 'overtime_Away',
                        'pass_touchdowns_Away', 'pass_yards_Away',
                        'pass_yards_per_attempt_Away', 'points_scored_Away',
                        'quarterback_rating_Away', 'rush_attempts_Away', 'rush_touchdowns_Away',
                        'rush_yards_Away', 'rush_yards_per_attempt_Away',
                        'third_down_attempts_Away', 'third_down_conversions_Away']

    past_games = pd.DataFrame()
    past_games_home_team = get_past_games(engine, home_team, away_team)
    past_games_away_team = get_past_games(engine, away_team, home_team)
    season_games_home_team = get_season_games(engine, home_team)
    season_games_away_team = get_season_games(engine, away_team)
    past_games = past_games.append(past_games_home_team)
    past_games = past_games.append(past_games_away_team)
    past_games = past_games.append(season_games_home_team)
    past_games = past_games.append(season_games_away_team)
    past_games = past_games.dropna()
    game_vector = pd.DataFrame(columns=desired_features)
    for feature in desired_features:
        game_vector.at[0, feature] = np.mean(past_games[feature].astype(float))
    game_vector['datetime_Home'] = game_date
    game_vector['opponent_name_Away'] = home_team
    game_vector['opponent_name_Home'] = away_team
    return game_vector


def rename_features(past_games, to_rename, rename_to):
    for key in past_games.keys():
        if rename_to in key:
            temp_key = key.replace(rename_to, 'Temp')
            past_games = past_games.rename(columns={key: temp_key})
        if to_rename in key:
            rename_to_key = key.replace(to_rename, rename_to)
            past_games = past_games.rename(columns={key: rename_to_key})
    for key in past_games.keys():
        if 'Temp' in key:
            to_rename_key = key.replace('Temp', to_rename)
            past_games = past_games.rename(columns={key: to_rename_key})
    return past_games


def get_past_games_statement(home_team, away_team):
    stmt = "SELECT * FROM APIData WHERE (opponent_abbr_Away = \'{}\' AND opponent_abbr_Home = \'{}\') AND " \
           "datetime_Home >= '2010-03-01' ORDER BY datetime_Home;".format(home_team, away_team)
    return stmt


def get_season_games_statement(home_team):
    stmt1 = "SELECT * FROM APIData WHERE opponent_abbr_Away = \'{}\' AND datetime_Home >= '2021-03-01' ORDER BY " \
            "datetime_Home;".format(home_team)
    stmt2 = "SELECT * FROM APIData WHERE opponent_abbr_Home = \'{}\' AND datetime_Home >= '2021-03-01' ORDER BY " \
            "datetime_Home;".format(home_team)
    return stmt1, stmt2


def get_past_games(engine, home_team, away_team):
    with engine.connect():
        stmt_home = get_past_games_statement(home_team, away_team)
        past_games_home = pd.read_sql(stmt_home, engine.connect())
        past_games_home = past_games_home.dropna()
        past_games_home = drop_features(past_games_home, 'Away')
        stmt_away = get_past_games_statement(away_team, home_team)
        past_games_away = pd.read_sql(stmt_away, engine.connect())
        past_games_away = past_games_away.dropna()
        past_games_away = drop_features(past_games_away, 'Home')
        past_games_away = past_games_away.drop('boxscore_index', axis=1)
    past_games = pd.concat((past_games_home, past_games_away), axis=1)
    return past_games


def get_season_games(engine, home_team):
    with engine.connect():
        stmt1, stmt2 = get_season_games_statement(home_team)
        past_games_home = pd.read_sql(stmt1, engine.connect())
        past_games_home = past_games_home.dropna()
        past_games_away = pd.read_sql(stmt2, engine.connect())
        past_games_away = past_games_away.dropna()
        past_games_away = rename_features(past_games_away, 'Away', 'Home')
    past_games = past_games_home.append(past_games_away)
    return past_games


def drop_features(past_games, to_drop):
    for key in past_games.keys():
        if to_drop in key:
            past_games = past_games.drop(columns=[key], axis=1)
    return past_games


def send_game_vector_to_db(engine, vector):
    with engine.connect():
        vector.to_sql(name='Featured_Vectors', con=engine, if_exists='append', index=False)
