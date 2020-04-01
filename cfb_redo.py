# CFB Poll Redo
# Dylan Klein
# 3/11/20

import requests
# from requests_ntlm import HttpNtlmAuth
# from requests.auth import HTTPBasicAuth
import numpy as np
# import t
import urllib3

urllib3.disable_warnings()

games = 'https://api.collegefootballdata.com/games?year=2019&seasonType=regular'
teams = 'https://api.collegefootballdata.com/teams/fbs?year=2019'

data = requests.get(games, verify=False)
team_info = requests.get(teams, verify=False)


class Static:
    def __init__(self):
        pass

    margin_of_victory = 17  # MOV cap, teams will not be rewarded past this score
    P5_bonus = 1.5  # Bonus for beating a P5 team
    G5_penalty = 1.5  # Penalty for losing to a G5 team
    FCS_penalty = 3  # Penalty for losing to a FCS team


class Stats:
    def __init__(self):
        self.name = ''
        self.wins = 0
        self.losses = 0
        self.score = 0
        self.conf = ''
        self.lost_to = []
        self.beat = []
        self.mov = []


datData = {}  # Overall Dictionary

if team_info.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(team_info.status_code))
for todo_item in team_info.json():
    teamname = todo_item['school']
    # print(teamname)
    conference = todo_item['conference']
    x = Stats()
    x.conf = conference
    x.name = teamname
    x.score = 0
    datData[teamname] = x

home_points = 0
away_points = 0

if data.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(data.status_code))
for todo_item in data.json():
    try:
        home_points = todo_item['home_points']
        # print(home_points)
        away_points = todo_item['away_points']
        # print(away_points)
        margin = home_points - away_points

        if margin >= 0:
            if margin > Static.margin_of_victory:  # Max MOV at 17 points
                margin = Static.margin_of_victory
            margin = round(margin / Static.margin_of_victory, 2)  # Standardize all MOV to a max of 1 point

            winner = todo_item['home_team']
            loser = todo_item['away_team']

        else:
            margin = margin * -1
            if margin > Static.margin_of_victory:  # Max MOV at 17 points
                margin = Static.margin_of_victory
            margin = round(margin / Static.margin_of_victory, 2)  # Standardize all MOV to a max of 1 point
            winner = todo_item['away_team']
            loser = todo_item['home_team']

        if winner in datData:
            datData[winner].wins += 1
            datData[winner].beat.append(loser)
            datData[winner].mov.append(margin)

        if loser in datData:
            datData[loser].losses += 1
            datData[loser].lost_to.append(winner)
            datData[loser].mov.append(margin * -1)

    # print(winner)
    except TypeError:
        continue

# Calculate Scores

maxwins = 0

for team in team_info.json():
    teamname = team['school']
    current_team = datData[teamname]
    # print("Current team is: ")
    # print(current_team.name)
    score = 0

    for k in range(len(current_team.mov)):
        score += current_team.mov[k]
    # score = round(score,2)
    # print(score)
    if current_team.wins > 0:
        beat_opp = current_team.beat
        # print("beaten opponent is: ")
        # print(beat_opp)

        for j in range(len(beat_opp)):
            score += 1
            if beat_opp[j] in datData:
                score += datData[beat_opp[j]].wins
                if (datData[beat_opp[j]].conf == 'Big 12' or
                        datData[beat_opp[j]].conf == 'Big Ten' or
                        datData[beat_opp[j]].conf == 'Pac-12' or
                        datData[beat_opp[j]].conf == 'ACC' or
                        datData[beat_opp[j]].conf == 'SEC' or
                        datData[beat_opp[j]].name == 'Notre Dame'):
                    score += Static.P5_bonus  # Bonus for beating P5 team

    if current_team.losses > 0:
        lost_opp = current_team.lost_to
        # print("lost opponent is: ")
        # print(lost_opp)

        for j in range(len(lost_opp)):
            score -= 1
            if lost_opp[j] in datData:
                score -= datData[lost_opp[j]].losses
                try:
                    # print(current_team.name)
                    # print(datData[lost_opp[j]].conf)
                    if (datData[lost_opp[j]].conf == 'Mountain West' or
                            datData[lost_opp[j]].conf == 'Conference USA' or
                            datData[lost_opp[j]].conf == 'Sun Belt' or
                            datData[lost_opp[j]].conf == 'Mid-American' or
                            datData[lost_opp[j]].conf == 'American Athletic' or
                            datData[lost_opp[j]].conf == 'FBS Independents'):
                        # print(current_team.name)
                        score -= Static.G5_penalty  # Penalty for losing to G5 team
                except KeyError:
                    score -= Static.FCS_penalty  # FCS teams have conference "null" in the api
                    continue
    if current_team.wins + current_team.losses > maxwins:
        maxwins = current_team.wins + current_team.losses

    current_team.score = round(score, 2)  # Rounding Score due to large decimal places

for team in team_info.json():  # Normalize score to remove lack of bye advantage
    teamname = team['school']
    current_team = datData[teamname]
    if current_team.wins + current_team.losses < maxwins:
        avg_score_per_game = current_team.score / (current_team.wins + current_team.losses)
        current_team.score = current_team.score + avg_score_per_game
        current_team.score = round(current_team.score, 2)  # Rounding Score due to large decimal places

Values = []
for team in team_info.json():  # Formatting for Results Viewing
    teamname = team['school']
    current_team = datData[teamname]
    Values.append([current_team.name, current_team.score, current_team.wins, current_team.losses])


def Sort(sub_li):  # Sorts Teams based on Score

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    return sorted(sub_li, key=lambda x: x[1])


Sorted_Values = Sort(Values)
Sorted_Values.reverse()
# print(Sorted_Values)			#Unformatted All 130
print()
for i in range(25):  # Formatted Top 25
    if i < 9:
        print(i + 1, end="  ")
    else:
        print(i + 1, end=" ")
    print(Sorted_Values[i])
