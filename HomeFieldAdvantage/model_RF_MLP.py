from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from IPython.display import display
import matplotlib.pyplot as plt
from string import ascii_letters
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
import seaborn as sns

# select desired features, normalize, balance datasets and split data into training/testing
def dataProcessing(data,unseenData):
    df = data

    ## Checking NaN and deplicated values in the dataset
    if df.isna().sum().max() != 0 or unseenData.isna().sum().max() != 0:
        df = df.dropna()
        unseenData = unseenData.dropna()

    categorical_features = df.dtypes[df.dtypes == 'object'].index

    ## as a record for the team names of the unseenData
    dates = unseenData['datetime_Home']
    homeTeam = unseenData['opponent_name_Away']
    awayTeam = unseenData['opponent_name_Home']
    teamInfo = pd.concat([dates, homeTeam, awayTeam], axis=1)
    teamInfo.columns = ['DateTime', 'home_team', 'away_team']

    result_home = df['result_Home']  # current target variable
    result_away = df['result_Away']  # target variable for predict away teams

    # convert the target variable into numerical values for train, validate the model
    target = result_home
    target = target.replace('Win', 1)
    target = target.replace('Loss', 0)
    target = target.replace('Tie', 2)

    # df = df.drop(categorical_features, axis=1)
    # synonyms_features = ["extra_points_attempted_Home", "field_goals_attempted_Home",
    #                      "pass_attempts_Home", "pass_completion_rate_Home", "points_allowed_Home",
    #                      "extra_points_attempted_Away", "field_goals_attempted_Away",
    #                      "pass_attempts_Away", "pass_completion_rate_Away", "points_allowed_Away"]
    # df = df.drop(synonyms_features, axis=1)
    # df = pd.concat([df, target], axis=1)
    # correlated = df.corr()
    # positive_corr = correlated[correlated['result_Home'] > 0]['result_Home']
    # desired_features = positive_corr.keys()[0:-1]

    """ Selected a total of 28 features. The first half is the features related to 
        home teams that are positively correlated to the target variable, the second 
        half is the features corresponding to the away teams
    """
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

    ## 28 after remove categorial and all related to points and touchdown
    # desired_features = ['interceptions_Home', 'pass_completions_Home',
    #                     'pass_yards_Home', 'pass_yards_per_attempt_Home', 'punt_yards_Home',
    #                     'punts_Home', 'quarterback_rating_Home', 'rush_attempts_Home',
    #                     'rush_yards_Home', 'rush_yards_per_attempt_Home',
    #                     'third_down_conversions_Home', 'times_sacked_Home', 'week_Home',
    #                     'yards_lost_from_sacks_Home', 'interceptions_Away',
    #                     'pass_completions_Away', 'pass_yards_Away',
    #                     'pass_yards_per_attempt_Away', 'punt_yards_Away', 'punts_Away',
    #                     'quarterback_rating_Away', 'rush_attempts_Away', 'rush_yards_Away',
    #                     'rush_yards_per_attempt_Away', 'third_down_conversions_Away',
    #                     'times_sacked_Away', 'week_Away', 'yards_lost_from_sacks_Away']

    """ if the desired features exist in the both the training, unseen dataset,
        and the unseen data is not null, grab it, otherwise return False """
    if ((all(x in df.columns for x in desired_features)) and (all(x in unseenData.columns for x in desired_features)) and (unseenData.shape[0] != 0)):
        train_data = df[desired_features]
        unseen_data = unseenData[desired_features]

        # normalize datasets, use this when dataset gets larger
        norm_train = norm_data(train_data)

        #up/down sampling to balance the data
        smote = SMOTE(sampling_strategy='minority')
        X_data,Y_label = smote.fit_resample(train_data,target)

        ## split data into training and testing
        x_train,x_test,y_train,y_test = train_test_split(X_data, Y_label, test_size=0.2)

        return x_train,x_test,y_train,y_test,unseen_data,teamInfo
    else:
        return False

def norm_data(data):
  # normalize the data, so the range with be from 0 to 1
  scaler = MinMaxScaler()
  scaler.fit(data)

  norm_df = pd.DataFrame(scaler.transform(data))
  norm_df.columns = data.columns

  return norm_df

def RFC_Prediction(data,unseenData):

    # if desired feature not found, return an empty dataframe
    if (dataProcessing(data,unseenData) == False):
        return pd.DataFrame()
    x_train,x_test,y_train,y_test,unseen_data,tmInfo = dataProcessing(data,unseenData)

     ## feed data into the Random Forest model
    rfc = RandomForestClassifier(n_estimators=50, max_depth=30,random_state=0)

    rfc.fit(x_train, y_train)
    y_pred = rfc.predict(x_test)

    accuracy_RFC= accuracy_score(y_test, y_pred)
    accuracy_RFC= np.round(accuracy_RFC*100,2)
    print('Random Forest Accuracy:',accuracy_RFC)

    print('\nclassification_report for RFC:\n-------------------------------------------------------')
    print(classification_report(y_test, y_pred))
    
    ## Random Forest: make predictions on the new data
    y_pred_RFC = rfc.predict(unseen_data)

    ## Random Forest: the predicted probabilities, and get the max prob.
    prob = rfc.predict_proba(unseen_data)
    maxProb = np.max(prob,axis=1)
    print("max prob:",maxProb)
    maxProb = np.round(maxProb*100,2)
    print('Pred:',y_pred_RFC)
    print('Prob:',prob)

    ## Random Forest predicted results
    gameWinner = {"Game": [], "Winner": [], "Win_Prob": []}
    str_tmInfo = str(tmInfo["DateTime"][0])+ ' ' + tmInfo["home_team"][0] + ' vs ' + tmInfo["away_team"][0]
    if y_pred_RFC == 1:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append(tmInfo ['home_team'][0])
        gameWinner["Win_Prob"].append(str(maxProb)[1:-1]+'%')
    elif y_pred_RFC == 0:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append(tmInfo ['away_team'][0])
        gameWinner["Win_Prob"].append(str(maxProb)[1:-1]+'%')
    else:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append("Tie")
        gameWinner["Win_Prob"].append(str(maxProb)[1:-1]+'%')

    return pd.DataFrame.from_dict(gameWinner)

def MLP_Prediction(data,unseenData):
    
    from sklearn.neural_network import MLPClassifier

    if (dataProcessing(data,unseenData) == False):
        return pd.DataFrame()
    x_train,x_test,y_train,y_test,unseen_data,tmInfo = dataProcessing(data,unseenData)
    
    #using neural networks model, MLP, to make predictions
    neurons = np.arange(15,20,5)
    totalAcc = 0
    print('\n')
    for i in neurons:
        # mlp = MLPClassifier(hidden_layer_sizes=(i,4),activation='logistic',solver='lbfgs',batch_size=50,learning_rate_init=0.01,max_iter=1000).fit(x_train,np.ravel(y_train))
        mlp = MLPClassifier(hidden_layer_sizes=(i,4),activation='relu',solver='sgd',batch_size=50,learning_rate_init=0.01,max_iter=200).fit(x_train,np.ravel(y_train))
        y_pred_MLP = mlp.predict(x_test)
        totalAcc += accuracy_score(y_test, y_pred_MLP)

        print('neurons=',i,'Training accuracy: {:.2f}'.format(mlp.score(x_train, y_train)),'  ',
            'Test accuracy: {:.2f}'.format(accuracy_score(y_test, y_pred_MLP)))

    acc_MLP = np.round(totalAcc/len(neurons)*100,2)
    print('Average accurancy using MLP:',acc_MLP,'%\n')

    print('\nPerformance of MLP:')
    print(classification_report(y_test, y_pred_MLP))

    ## MLP: predict on the unseen data
    y_pred_MLP = mlp.predict(unseen_data)

    prob_MLP = mlp.predict_proba(unseen_data)
    maxProb_MLP = np.max(prob_MLP,1)
    maxProb_MLP = np.round(maxProb_MLP*100,2)
    print('Predicted label:',y_pred_MLP)
    print("Win prob:",prob_MLP)
    print('Max prob:',maxProb_MLP)
    ## MLP predicted results
    gameWinner = {"Game": [], "Winner": [], "Win_Prob": []}
    str_tmInfo = tmInfo.values[0][0] + ' ' + tmInfo.values[0][1] + ' vs ' + tmInfo.values[0][2]
    if y_pred_MLP[0] == 1:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append(tmInfo['home_team'][0])
        gameWinner["Win_Prob"].append(str(maxProb_MLP)[1:-1]+'%')
    elif y_pred_MLP[0] == 0:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append(tmInfo['away_team'][0])
        gameWinner["Win_Prob"].append(str(maxProb_MLP)[1:-1]+'%')
    else:
        gameWinner["Game"].append(str_tmInfo)
        gameWinner["Winner"].append("Tie")
        gameWinner["Win_Prob"].append(str(maxProb_MLP)[1:-1]+'%')

    return pd.DataFrame.from_dict(gameWinner)


## get predictions from the Random Forest Classifier
# df = gd()
# game_winner_RFC = RFC_Prediction(df)
#
# # example of what kind of info will be displayed in the fontend
# key_list = list(game_winner_RFC.keys())
# print("The Predictions from the Random Forest Classifier:\n")
# for i in range(len(game_winner_RFC[key_list[0]])):
#     for k in key_list:
#         print(k,':',game_winner_RFC[k][0])
#     print()

## get predictions from the Muli-layer Proceptron Classifier
# game_winner_MLP = MLP_Prediction('backend/model/all_processed.csv')

# key_list = list(gamegame_winner_MLP_winner.keys())
# print("The Predictions from the Muli-layer Proceptron Classifier:\n")
# for i in range(len(game_winner_MLP[key_list[0]])):
#     for k in key_list:
#         print(k,':',game_winner_MLP[k][0])
#     print()