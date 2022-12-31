from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
from .get_data_from_db import get_api_data, get_my_prediction
from .model_RF_MLP import RFC_Prediction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .get_featured_game_info import get_featured_game_vector
from .make_pages import make_schedule_page, make_vector_page
import sqlalchemy as sa
from .team_dict import team_dict
from django.conf import settings

ENGINE = sa.create_engine(settings.DB_CONNECTION_STRING)


def home_page(request):
    return render(request, "HomeFieldAdvantage/home.html")


def game_page(request):
    df = make_schedule_page()
    send_it = pd.DataFrame(columns=['home_team', 'away_team', 'game_date'])
    my_choice = ''
    num_choice = 0
    if request.POST:
        for i in range(len(df)):
            if 'pred{}'.format(i) in request.POST:
                my_choice = 'pred'
                num_choice = i
            else:
                if 'vec{}'.format(i) in request.POST:
                    my_choice = 'vec'
                    num_choice = i
        send_it.at[0, 'home_team'] = df.iat[num_choice, 1]
        send_it.at[0, 'away_team'] = df.iat[num_choice, 0]
        send_it.at[0, 'game_date'] = df.iat[num_choice, 4]
        send_it.to_sql(name='GameToGet', con=ENGINE, if_exists='replace', index=False)
        ht = send_it.at[0, 'home_team']
        at = send_it.at[0, 'away_team']
        home_team = team_dict[ht]['abbr']
        away_team = team_dict[at]['abbr']
        date_tm = send_it['game_date'][0]
        data = get_featured_game_vector(ENGINE, home_team, away_team, date_tm)
        data.to_sql(name='FeaturedGame', con=ENGINE, if_exists='replace', index=False)
        if my_choice == 'vec':
            make_vector_page(ENGINE)
            return HttpResponseRedirect("/vector/")
        else:
            if my_choice == 'pred':
                mydata = get_api_data(ENGINE)
                df = RFC_Prediction(mydata, data)
                return render(request, 'HomeFieldAdvantage/TestResults.html', {'data': df})
        if df.empty:  # added this to display error message caused by null values
            df = {False: "Error was found in data processing"}
            return render(request, 'HomeFieldAdvantage/TestResults.html', {'data': df})
    return render(request, "HomeFieldAdvantage/upcomingGames.html")


def vector(request):
    if request.method == "POST":
        df = pd.DataFrame.from_dict(request.POST, orient='index')
        df = df.transpose()
        df = df.drop(['csrfmiddlewaretoken'], axis=1)
        df = df.drop(['addVec'], axis=1)
        df.at['datetime_Home'] = pd.to_datetime(df['datetime_Home']).dt.date
        mydata = get_api_data(ENGINE)
        prediction = RFC_Prediction(mydata, df)
        if request.user.is_authenticated:
            username = request.user.username
            username = username.replace(' ', '')
            prediction.to_sql(name=username, con=ENGINE, if_exists='replace', index=False)
        return render(request, 'HomeFieldAdvantage/TestResults.html', {'data': prediction})
    return render(request, "HomeFieldAdvantage/vector.html")


def about_us(request):
    return render(request, "HomeFieldAdvantage/about_us.html")


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('HomeFieldAdvantage:login')
        context = {'form': form}
        return render(request, 'HomeFieldAdvantage/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('HomeFieldAdvantage:home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'HomeFieldAdvantage/login.html', context)


def logout_view(request):
    return render(logout(request), "HomeFieldAdvantage/home.html")


@login_required()
def my_prediction(request):
    if request.user.is_authenticated:
        username = request.user.username
        username = username.replace(' ','')
        try:
            my_pred = get_my_prediction(ENGINE,username)
        except:
            my_pred = {False: 'No data has been found.'}
    else:
        my_pred = {False: 'No data has been found.'}

    return render(request, "HomeFieldAdvantage/my_prediction.html", {'myPred': my_pred})
