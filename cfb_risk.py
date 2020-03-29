#CFB Poll Redo
#3/11/20

import requests
import numpy as np
import urllib3
urllib3.disable_warnings()

turns = 'https://collegefootballrisk.com/api/turns'
turn_info = requests.get(turns, verify=False)
if turn_info.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(team_info.status_code))
for todo_item in turn_info.json():
	current_turn = todo_item['day']	#overwrite value to last, which is current turn

teams = 'https://collegefootballrisk.com/api/stats/team?team=Ohio%20State'
leaderboard = 'https://collegefootballrisk.com/api/stats/leaderboard?season=2&day='+ str(current_turn)


data = requests.get(teams, verify=False)	#Prevents SSL error at work
team_info = requests.get(leaderboard, verify=False)


class Stats:
	def __init__(self):
		self.name = ''
		self.rank = 0
		self.territory = 0
		self.player = 0
		self.stars = 0


datData = {}		#Overall Dictionary

if team_info.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(team_info.status_code))
for todo_item in team_info.json():
	teamname = todo_item['name']
	# print(teamname)
	rank = todo_item['rank']
	territory = todo_item['territoryCount']
	player = todo_item['playerCount']
	star = todo_item['starPower']

	x = Stats()
	x.rank = rank
	x.name = teamname
	x.territory = territory
	x.player = player
	x.star = star

	datData[teamname] = x

Values = []
for team in team_info.json():					#Formatting for Results Viewing
	teamname = team['name']
	current_team = datData[teamname]
	Values.append([current_team.name, current_team.rank, current_team.territory, current_team.star])

# def Sort(sub_li): 	#Sorts Teams based on Score

    # # reverse = None (Sorts in Ascending order)
    # # key is set to sort using second element of
    # # sublist lambda has been used
    # return(sorted(sub_li, key = lambda x: x[3]))

# Sorted_Values = Sort(Values)
# Sorted_Values.reverse()

print('current turn is ' + str(current_turn))
print('Ohio State Territories and rank: ' + datData['Ohio State'].territory + "," + datData['Ohio State'].rank)
# print(Sorted_Values)

# print()
# for i in range(25):				#Formatted Top 25
	# if (i < 9):
		# print(i+1, end ="  ")
	# else:
		# print(i+1, end =" ")
	# print(Sorted_Values[i])