from .get_data_from_db import *
import sqlalchemy as sa
import pandas as pd
from .combine_api_and_db import get_newest_data


def make_schedule_page():
    engine = sa.create_engine(settings.DB_CONNECTION_STRING)
    get_newest_data(engine)
    df = get_schedule_data(engine)
    df['score_home'] = df['score_home'].fillna('-')
    df['score_away'] = df['score_away'].fillna('guh')
    for i, row in df.iterrows():
        if df.iat[i, 2] == '-':
            df.iat[
                i, 2] = '''<form method="post" novalidate>{{% csrf_token %}}<button class="pred_btn" input type="hidden" name="pred{}" value=""  onclick="location.href=''" >Predict Game</button> </form>'''.format(i)
        if df.iat[i, 3] == 'guh':
            df.iat[
                i, 3] = '''<form method="post" novalidate>{{% csrf_token %}}<button class="pred_btn" input type="hidden" name="vec{}" value=""  onclick="location.href=''" >Make My Vector</button> </form>'''.format(i)
    html = df.to_html(render_links=True, escape=False,index=False)
    # write html to file
    text_file = open("HomeFieldAdvantage/templates/HomeFieldAdvantage/sched.html", "w")
    text_file.write(html)
    text_file.close()
    return df


def make_vector_dataframe(df, home_or_away, team):
    page_df = pd.DataFrame()
    for (column_name, column_data) in df.iteritems():
        if 'opponent' in str(column_name) or 'date' in str(column_name):
            page_df.at[column_name, 0] = '<label for="{}">{}:</label>'.format(column_name, column_name)
            page_df.at[column_name, 1] = '<input type="text" id="{}" name="{}" value="{}" readonly>'.format(column_name,
                                                                                                 column_name,
                                                                                               column_data[0])
        else:
            if home_or_away in str(column_name):
                strip_name = column_name.replace(home_or_away, team)
                page_df.at[column_name, 0] = '<label for="{}">{}:</label>'.format(column_name, strip_name)
                page_df.at[column_name, 1] = '<input type="text" id="{}" name="{}" value="{:.4}">'.format(column_name, column_name, column_data[0])
            else:
                pass
    html = page_df.to_html(render_links=True, escape=False, index=False, header=False)
    file_name = "HomeFieldAdvantage/templates/HomeFieldAdvantage/{}_vector.html".format(home_or_away)
    text_file = open(file_name, "w")
    text_file.write(html)
    text_file.close()


def make_vector_page(engine):
    df = get_featured_game(engine)
    home_team = df.at[0, 'opponent_name_Away']
    away_team = df.at[0, 'opponent_name_Home']
    make_vector_dataframe(df, 'Home', home_team)
    make_vector_dataframe(df, 'Away', away_team)
    return df


