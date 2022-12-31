import pandas as pd
from sportsipy.nfl.teams import Teams
from sqlalchemy import text
from datetime import datetime as dt


def get_api_data(start_year, stop_year, pull_date=dt(2010, 2, 1).date()):
    df_merged = pd.DataFrame()
    season = pd.DataFrame()
    for years in range(start_year, (stop_year + 1)):
        teams = Teams(years)
        df_home = pd.DataFrame()
        df_away = pd.DataFrame()
        for team in teams:
            df_sched = pd.DataFrame()
            schedule = pd.DataFrame(team.schedule.dataframe)
            team_schedule = pd.DataFrame(schedule)
            schedule['datetime'] = pd.to_datetime(schedule['datetime']).dt.date
            schedule = schedule.where(schedule['datetime'] > pull_date)
            df_home = df_home.append(schedule.where(schedule['location'] == 'Home'))
            df_away = df_away.append(schedule.where(schedule['location'] == 'Away'))
            df_home = df_home.dropna()
            df_away = df_away.dropna()
            team_schedule = team_schedule.where(team_schedule['location'] == 'Home')
            team_schedule = team_schedule.dropna(subset=['datetime'])
            df_sched['away_team'] = team_schedule['opponent_name']
            df_sched['home_team'] = team.name
            df_sched['score_home'] = team_schedule['points_scored']
            df_sched['score_away'] = team_schedule['points_allowed']
            df_sched['game_date'] = team_schedule['datetime']
            season = season.append(df_sched)
        game = pd.merge(left=df_home, right=df_away, left_on='boxscore_index', right_on='boxscore_index',
                        suffixes=('_Home', '_Away'))
        df_merged = df_merged.append(game)
    print('Success')
    return df_merged, season


def get_initial_data(engine):
    df, sched = get_api_data(2012, 2020)
    df.to_sql(name='APIData', con=engine, if_exists='replace', index=False)


def get_newest_data(engine):
    with engine.connect() as connection:
        last_pull = connection.execute(text("SELECT last_pull_date FROM Last_Pull;"))
        for d in last_pull:
            lpdate = d[0]
        if dt.today().date() > lpdate:
            df, sched = get_api_data(lpdate.year, dt.today().year, lpdate)
            df.to_sql(name='APIData', con=engine, if_exists='append', index=False)
            sched.to_sql(name='Schedule', con=engine, if_exists='replace', index=False)
            stmt = 'UPDATE Last_Pull SET last_pull_date=\'{}\' WHERE id=1'.format(dt.today().date())
            connection.execute(text(stmt))
