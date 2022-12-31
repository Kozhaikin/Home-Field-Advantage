import pandas as pd
import numpy as np
from datetime import date

# get the schedule for all games
df = pd.read_csv("HomeFieldAdvantage/templates/HomeFieldAdvantage/schedule/allSchedule.cvs",index_col=0) 

# get the schedule for upcoming games and extract desired features, add 2 new features(win prob.) to it
now = date.today()
today = now.strftime("%Y-%m-%d") #convert current date to string
feature = ['Week','Day','Date','Time','Winner/tie','Unnamed: 6','Loser/tie']
gameDF = df.loc[df['Date']>= today,feature] #get future game schedule
gameDF=gameDF.rename(columns = {'Winner/tie':'Team1','Unnamed: 6':' ','Loser/tie':'Team2'})
gameDF["Team1 Win Prob."] =''
gameDF["Team2 Win Prob."] =''
gameDF.index.name = gameDF.columns[0]
newGameDF = gameDF.set_index(gameDF[gameDF.columns[0]])
newGameDF = newGameDF.drop("Week",axis=1)

newGameDF.to_csv('HomeFieldAdvantage/templates/HomeFieldAdvantage/schedule/futureSchedule.cvs')
from prettytable import PrettyTable

#use PrettyTable to convert the data frame into a html file
#looks better than the regular table
file = open("HomeFieldAdvantage/templates/HomeFieldAdvantage/schedule/futureSchedule.cvs", 'r') 
file = file.readlines() 
head = file[0] 
head = head.rstrip('\n').split(',')
head
#for headings
table = PrettyTable([head[i] for i in range(len(head))]) 
for i in range(1, len(file)) : 
    table.add_row(file[i].split(','))
htmlCode = table.get_html_string() 
final_htmlFile = open('HomeFieldAdvantage/templates/HomeFieldAdvantage/schedule/gameSchedue.html', 'w') 
final_htmlFile=final_htmlFile.write(htmlCode)