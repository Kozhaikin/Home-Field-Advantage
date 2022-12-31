import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone


# # class Question(models.Model):
# #
# #     question_text = models.CharField(max_length=200)
# #     pub_date = models.DateTimeField('date published')
# #     def __str__(self):
# #         return self.question_text
# #
# #     @admin.display(
# #         boolean=True,
# #         ordering='pub_date',
# #         description='Published recently?',
# #     )
# #     def was_published_recently(self):
# #         now = timezone.now()
# #         return now - datetime.timedelta(days=1) <= self.pub_date <= now
# #
# # class Choice(models.Model):
# #     question = models.ForeignKey(Question, on_delete=models.CASCADE)
# #     choice_text = models.CharField(max_length=200)
# #     votes = models.IntegerField(default=0)
# #     def __str__(self):
# #         return self.choice_text
#
# # #for the Super Bowl teams on the My Prediction page
# class SuperBowlTeams(models.Model):
#     #for grab the data from db later
#     teamName1 = models.CharField(max_length=100)
#     teamName2 = models.CharField(max_length=100)
#     teamScore1 = models.IntegerField(default=0)
#     teamScore2 = models.IntegerField(default=0)
#     winProb1 = models.CharField(max_length=100)
#     winProb2 = models.CharField(max_length=100)
#     class Meta:
#         db_table = ""  #need to change it to the table name in the db
#
#
# # #the predicted Super Bowl result to be displayed on the homepage
# class SuperBowlHomepage(models.Model):
#     teamName = models.CharField(max_length=100)
#     winProb = models.CharField(max_length=100)
#     class Meta:
#         db_table = ""  #need to change it to the table name in the db
#
#
#
# #for testing pull data from db to display in the "Data" page
# class Teams(models.Model):
#     team_id = models.AutoField(primary_key=True)
#     team_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'teams'
#
#
# class TestTbl(models.Model):
#     test_id = models.AutoField(primary_key=True)
#     team = models.ForeignKey(Teams, models.DO_NOTHING)
#     wins = models.IntegerField()
#     last_game_date = models.DateField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'test_tbl'

class LastPullDate(models.Model):
    last_pull_date = models.DateField(blank=False, null=False, auto_now_add=True)

    class Meta:
        db_table = 'Last_Pull'

# class BoxScores(models.Model):
#
#     id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
#     boxscore_index = models.CharField(max_length=200)
#     date = models.DateField(blank=True, null=True)
#     datetime = models.DateTimeField(blank=True, null=True)
#     day = models.CharField(max_length=4)
#     extra_points_attempted = models.IntegerField()
#     extra_points_made = models.IntegerField()
#     field_goals_attempted = models.IntegerField()
#     field_goals_made = models.IntegerField()
#     fourth_down_attempts = models.IntegerField()
#     fourth_down_conversions = models.IntegerField()
#     interceptions = models.IntegerField()
#     location = models.CharField(max_length=20)
#     opponent_abbr = models.CharField(max_length=3)
#     opponent_name = models.CharField(max_length=40)
#     overtime = models.IntegerField()
#     pass_attempts = models.IntegerField()
#     pass_completion_rate = models.FloatField()
#     pass_completions = models.IntegerField()
#     pass_touchdowns = models.IntegerField()
#     pass_yards = models.IntegerField()
#     pass_yards_per_attempt = models.FloatField()
#     points_allowed = models.IntegerField()
#     points_scored = models.IntegerField()
#     punt_yards = models.IntegerField()
#     punts = models.IntegerField()
#     quarterback_rating = models.FloatField()
#     result = models.CharField(max_length=5)
#     rush_attempts = models.IntegerField()
#     rush_touchdowns = models.IntegerField()
#     rush_yards = models.IntegerField()
#     rush_yards_per_attempt = models.FloatField()
#     third_down_attempts = models.IntegerField()
#     third_down_conversions = models.IntegerField()
#     time_of_possession = models.DateTimeField(blank=True, null=True)
#     times_sacked = models.IntegerField()
#     game_type = models.CharField(max_length=10)
#     week = models.IntegerField()
#     yards_lost_from_sacks = models.IntegerField()
#
#     class Meta:
#         db_table = 'BoxScores'
