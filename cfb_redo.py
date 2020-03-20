#CFB Poll Redo
#3/11/20

import requests
# from requests_ntlm import HttpNtlmAuth
# from requests.auth import HTTPBasicAuth
import numpy as np
import urllib3
urllib3.disable_warnings()

games = 'https://api.collegefootballdata.com/games?year=2019&seasonType=regular'
teams = 'https://api.collegefootballdata.com/teams/fbs?year=2019'

data = requests.get(games, verify=False)	#Prevents SSL error at work
team_info = requests.get(teams, verify=False)

class Static:
	margin_of_victory = 17		#MOV cap, teams will not be rewarded past this score 
	P5_bonus = 1.5				#Bonus for beating a P5 team
	G5_penalty = 1.5			#Penalty for losing to a G5 team

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

datData = {}		#Overall Dictionary

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
		print(todo_item['home_team'])

		if(margin >= 0):
			if (margin > Static.margin_of_victory): #Max MOV at 17 points
				margin = Static.margin_of_victory
			margin = round(margin/Static.margin_of_victory,2) #Standardize all MOV to a max of 1 point
			
			winner = todo_item['home_team']
			loser = todo_item['away_team']
			if winner in datData:
				datData[winner].wins += 1
				datData[winner].beat.append(loser)
				datData[winner].mov.append(margin)
			
			if loser in datData:
				datData[loser].losses += 1
				datData[loser].lost_to.append(winner)
				datData[loser].mov.append(margin*-1)
			
		else:
			winner = todo_item['away_team']
			loser = todo_item['home_team']
	
	
	
	except TypeError:
		break
	
	
	# for i in range(sheet.nrows):
	# winner = sheet.cell_value(i,5)
	# if winner.startswith('('):
		# winner = winner.split(')')[1].lstrip()
	# loser = sheet.cell_value(i,7)
	# if loser.startswith('('):
		# loser = loser.split(')')[1].lstrip()
		
	# margin = float(sheet.cell_value(i,6)) - float(sheet.cell_value(i,8))	
	# if (margin > Static.margin_of_victory): #Max MOV at 17 points
		# margin = Static.margin_of_victory
	# margin = round(margin/Static.margin_of_victory,2) #Standardize all MOV to a max of 1 point
	
	# if winner in datData:
		# datData[winner].wins += 1
		# datData[winner].beat.append(loser)
		# datData[winner].mov.append(margin)
	# if loser in datData:
		# datData[loser].losses += 1
		# datData[loser].lost_to.append(winner)
		# datData[loser].mov.append(margin*-1)
	
	
	
	
	
	
	
	
	
	
	
	
	
