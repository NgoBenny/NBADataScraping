import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

nba_url = (f'https://www.basketball-reference.com/teams/GSW/2023.html')

nba_res = requests.get(nba_url)

nba_soup = BeautifulSoup(nba_res.content, "lxml")

nba_per_game = nba_soup.find(name = 'table', attrs = {'id' : 'per_game'})

nba_info = []
for row in nba_per_game.find_all('tr')[1:]:
        player = {}
        player['Name'] = row.find('a').text.strip()
        player['Age'] = row.find('td', {'data-stat' : 'age'}).text
        player['Mins Per Game'] = row.find('td', {'data-stat' : 'mp_per_g'}).text
        player['Field Goal %'] = row.find('td', {'data-stat' : 'fg_pct'}).text
        player['Rebounds Per Game'] = row.find('td', {'data-stat' : 'trb_per_g'}).text
        player['Assists Per Game'] = row.find('td', {'data-stat' : 'ast_per_g'}).text
        player['Steals Per Game'] = row.find('td', {'data-stat' : 'stl_per_g'}).text
        player['Blocks Per Game'] = row.find('td', {'data-stat' : 'blk_per_g'}).text
        player['Turnovers Per Game'] = row.find('td', {'data-stat' : 'tov_per_g'}).text
        player['Points Per Game'] = row.find('td', {'data-stat' : 'pts_per_g'}).text
        
        nba_info.append(player)
        time.sleep(5)

nba_df = pd.DataFrame(nba_info)
nba_df.to_csv("warriors.csv", index=False)

