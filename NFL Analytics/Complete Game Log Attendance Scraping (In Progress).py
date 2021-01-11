import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import time
import shutil
import re
import os
import json
import string
import glob


import urllib.request
import csv

mainurl = 'https://www.espn.com/nfl/team/depth/_/name/lac/los-angeles-chargers'
BASE_URL = 'https://www.pro-football-reference.com{0}'
PLAYER_LIST_URL = 'https://www.pro-football-reference.com/players/'
PLAYER_PROFILE_URL = 'https://www.pro-football-reference.com/players/{0}/{1}'
PLAYER_GAMELOG_URL = 'https://www.pro-football-reference.com/players/{0}/{1}/gamelog/{2}'

GAMES_URL = 'https://www.espn.com/nfl/matchup?gameId='
SCOREBOARD = 'https://www.espn.com/nfl/scoreboard/_/year/'
ayear = 2000
gameids = [];
while ayear < 2021:
  aweek = 1
  print(ayear)
  while aweek < 18:
    print(aweek)
    weekgames = SCOREBOARD + str(ayear) + '/seasontype/2/week' + str(aweek) 
    con = urllib.request.urlopen(urllib.request.Request(weekgames))
    soup = BeautifulSoup(con, 'html.parser')
    gameids = gameids + [game['id'] for game in soup.find_all('article', {'class': 'scoreboard football pregame js-show'})]
    for game in gameids:
      game = GAMES_URL + game
    aweek+=1
  ayear+=1

gameno = 0
hometeam = []
awayteam = []
awayypp = []
homeypp = []
for game in gameids:
  print(game)
  soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(game)), 'html.parser')
  hometeam += soup.find('div', {'class': 'team home'}).find('span', {'class': 'short-name'})
  awayteam += soup.find('div', {'class': 'team away'}).find('span', {'class': 'short-name'})
  ypps = soup.find('tr', {'data-stat-attr': 'yardsPerPlay'})
  awayypp +=ypps[1].split('\n')[0].split(' ')[1]
  homeypp +=ypps[2].split('\n')[0].split(' ')[1]
for thing in awayypp:
  print(thing)




PARTICIPATION_THRESHHOLD = 25
offense = 1
dualpos = 0

req = urllib.request.Request(mainurl)
con = urllib.request.urlopen(req)

playreq = urllib.request.Request(PLAYER_LIST_URL)


parse2 = BeautifulSoup(con, 'html.parser')

letters = list(string.ascii_uppercase)
i = 0
for letter in letters:
  response = urllib.request.urlopen(PLAYER_LIST_URL + letter)
  soup = BeautifulSoup(response, 'html.parser')
  players = soup.find('div', {'id': 'div_players'}).find_all('a')
  player_profile_urls = [BASE_URL.format(player['href']) for player in players]
  for player_profile_url in player_profile_urls:
    i+=1 #commment out later
    request = urllib.request.urlopen(urllib.request.Request(player_profile_url+'/gamelog'))
    soup = BeautifulSoup(request, 'html.parser')
    profile_section = soup.find('div', {'id': 'meta'})
    profile = {'name' : None, 'wowy' : None};
    profile['name'] = profile_section.find('h1', {'itemprop': 'name'}).contents[0]
    profile_attributes = profile_section.find_all('p')
    current_attribute = 1      

    profile['position'] = profile_attributes[current_attribute].contents[2].split('\n')[0].split(' ')[1]
    current_attribute += 1

    num_attributes = len(profile_attributes)

    game_section = soup.find('div', {'id': 'all_stats'})
    
    years = game_section.find_all('td', {'class': 'left', 'data-stat': 'year_id'})
    dates = game_section.find_all('td', {'class': 'left', 'data-stat': 'game_date'})
    gamenums = game_section.find_all('td', {'class': 'right', 'data-stat': 'game_num'})
    weeks = game_section.find_all('td', {'class': 'right', 'data-stat': 'week_num'})
    team = game_section.find_all('td', {'class': 'left', 'data-stat': 'team'})
    homeoraway = game_section.find_all('td', {'class': 'right', 'data-stat': 'game_location'})
    opponent = game_section.find_all('td', {'class': 'left', 'data-stat': 'opp'})



    OFFENSIVE_POSITIONS = {'QB', 'RB', 'HB', 'TB', 'FB', 'LH', 'RH', 'BB', 'B', 'WB', 'WR', 'FL', 'SE', 'E', 'TE', 'LE', 'LT', 'LOT', 'T', 'LG', 'G', 'C', 'RG', 'RT', 'ROT', 'RE'}
    DEFENSIVE_POSITIONS = {'DL', 'LDE', 'DE', 'LDT', 'DT', 'NT', 'MG', 'DG', 'RDT', 'RDE', 'LOLB', 'RUSH', 'OLB', 'LLB', 'LILB', 'WILL', 'ILB', 'SLB', 'MLB', 'MIKE', 'WLB', 'RILB', 'RLB', 'ROLB', 'SAM', 'LB', 'LCB', 'CB', 'RCB', 'SS', 'FS', 'LDH', 'RDH', 'LS', 'S', 'RS', 'DB'}
    participation = [];
    if '-' in profile['position']:
      dualpos = 1
    elif (profile['position'] in OFFENSIVE_POSITIONS):
      offense = 1
      participation = game_section.find_all('td', {'class': 'right iz', 'data-stat': 'off_pct'})
    elif (profile['position'] in DEFENSIVE_POSITIONS):
      participation = game_section.find_all('td', {'class': 'right iz', 'data-stat': 'def_pct'})
    
    
    i=0
    for thing in participation:
      if participation[i] is not None:
        if '%' in participation[i]:             participation[i].replace('%', '')
        if int(participation[i]) <= PARTICIPATION_THRESHHOLD:
          participation[i] = 0
      i+=1

    
      

  


    



t = parse2.find_all('a', {'class' : 'AnchorLink'})


with open('index.csv', 'a') as csv_file:
  writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
  #i=0
  for col1, col2, col3 in zip(t):
    writer.writerow([col1.get_text().strip()])
    if(col2.get_text().strip() != ""):
      writer.writerow([col2.get_text().strip()])
    if(col3.get_text().strip() != ""):
      writer.writerow([col3.get_text().strip()])

