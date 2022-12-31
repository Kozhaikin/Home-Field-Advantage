# Generated by Django 3.2.9 on 2021-11-18 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeFieldAdvantage', '0004_delete_boxscore'),
    ]

    operations = operations = [
        migrations.CreateModel(
            name='Boxscore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxscore_index', models.CharField(max_length=200)),
                ('date', models.DateField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('day', models.CharField(max_length=4)),
                ('extra_points_attempted', models.IntegerField()),
                ('extra_points_made', models.IntegerField()),
                ('field_goals_attempted', models.IntegerField()),
                ('field_goals_made', models.IntegerField()),
                ('fourth_down_attempts', models.IntegerField()),
                ('fourth_down_conversions', models.IntegerField()),
                ('interceptions', models.IntegerField()),
                ('location', models.CharField(max_length=20)),
                ('opponent_abbr', models.CharField(max_length=3)),
                ('opponent_name', models.CharField(max_length=40)),
                ('overtime', models.IntegerField()),
                ('pass_attempts', models.IntegerField()),
                ('pass_completion_rate', models.FloatField()),
                ('pass_completions', models.IntegerField()),
                ('pass_touchdowns', models.IntegerField()),
                ('pass_yards', models.IntegerField()),
                ('pass_yards_per_attempt', models.FloatField()),
                ('points_allowed', models.IntegerField()),
                ('points_scored', models.IntegerField()),
                ('punt_yards', models.IntegerField()),
                ('punts', models.IntegerField()),
                ('quarterback_rating', models.FloatField()),
                ('result', models.CharField(max_length=5)),
                ('rush_attempts', models.IntegerField()),
                ('rush_touchdowns', models.IntegerField()),
                ('rush_yards', models.IntegerField()),
                ('rush_yards_per_attempt', models.FloatField()),
                ('third_down_attempts', models.IntegerField()),
                ('third_down_conversions', models.IntegerField()),
                ('time_of_possession', models.DateTimeField(blank=True, null=True)),
                ('times_sacked', models.IntegerField()),
                ('type', models.CharField(max_length=10)),
                ('week', models.IntegerField()),
                ('yards_lost_from_sacks', models.IntegerField())
            ],
        ),

    ]

