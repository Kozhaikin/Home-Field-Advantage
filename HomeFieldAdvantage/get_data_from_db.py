import pandas as pd
from django.conf import settings

def get_api_data(engine):
    connection = engine.connect()
    data = connection.execute("SELECT * FROM APIData")
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df


def get_schedule_data(engine):
    connection = engine.connect()
    data = connection.execute("SELECT * FROM Schedule WHERE game_date > \'{}\' ORDER BY game_date DESC".format(settings.BEGIN_SEASON))
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df


def get_featured_game_vectors(engine):
    connection = engine.connect()
    data = connection.execute("SELECT * FROM Featured_Vectors")
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df


def get_team_info(engine):
    connection = engine.connect()
    data = connection.execute("SELECT * FROM GameToGet")
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df


def get_my_prediction(engine,username):
    connection = engine.connect()
    # change it to retrieve by username or other unique identifier and "My_Prediction"
    data = connection.execute("SELECT * FROM "+username)
    print("Data:",data)
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df


def get_featured_game(engine):
    connection = engine.connect()
    data = connection.execute("SELECT * FROM FeaturedGame")
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df

