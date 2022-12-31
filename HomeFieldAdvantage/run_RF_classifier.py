# from .model_RF_MLP import RFC_Prediction,MLP_Prediction
# from .get_data_from_db import get_api_data
# from .combine_api_and_db import get_newest_data
# import sqlalchemy as sa
# from django.conf import settings
# from .get_featured_game_info import get_featured_game_vector,send_game_vector_to_db
#
# def stuff():
#     print("Connecting to the database")
#     engine = sa.create_engine(settings.DB_CONNECTION_STRING)
#     get_newest_data(engine)
#     print("Newest data acquired")
#     mydata = get_api_data(engine)
#     print("Past games loaded")
#     # unseenData = get_featured_game_vector(engine, 'CHI', 'DET')
#     # unseenData = get_featured_game_vector(engine, 'DEN', 'KAN') #12/5
#     # unseenData = get_featured_game_vector(engine, 'RAV', 'PIT') #12/5
#     # unseenData = get_featured_game_vector(engine, 'CLT', 'HTX') #12/5
#     # unseenData = get_featured_game_vector(engine, 'PIT', 'MIN')   #12/9
#
#     # unseenData = get_featured_game_vector(engine, 'ATL', 'CAR','2021-12-12')  # 12/12
#     unseenData = get_featured_game_vector(engine, 'NOR', 'TAM', '2021-12-19')  # 12/12
#
#     print("Featured game vector created")
#     send_game_vector_to_db(engine, unseenData)
#     print("Featured vector saved")
#     df = RFC_Prediction(mydata, unseenData)
#     results = df
#     return results
