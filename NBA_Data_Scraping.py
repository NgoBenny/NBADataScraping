import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

nba_url = 'https://www.basketball-reference.com/'

nba_res = requests.get(nba_url)

nba_soup = BeautifulSoup(nba_res.content, "lxml")

nba_team = nba_soup.find(name = 'div', attrs = {'id' : 'teams'})

nba_list = []
for i in nba_team.find_all('option')[1:31]:

    name = i.get('value')
    nba_list.append(name)
    time.sleep(5)

def get_stats(year):
    # Creating a list of dictionaries to then convert into a Pandas Dataframe
    nba_info = []
    
    # Iteratively finding the URL page for each NBA team according to the 'year' parameter and instantiating
    # a BeautifulSoup object
    for i in nba_list:
        team_url = (f'https://www.basketball-reference.com{i}/{str(year)}.html')
        team_res = requests.get(team_url)
        team_soup = BeautifulSoup(team_res.content, 'lxml')
        per_game = team_soup.find(name = 'table', attrs = {'id' : 'per_game'})

        for row in per_game.find_all('tr')[1:]:  # Excluding the first 'tr', since that's the table's title head

            player = {}
            player['Name'] = row.find('a').text.strip()
            
            team = i[-3:]
            player['Team'] = team
            
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
        
    nba_info_df = pd.DataFrame(nba_info)
    return nba_info_df

def main():
    year = 2022
    nba_info_df = get_stats(year)
    print(nba_info_df)
    nba_info_df.to_csv(f'{year}.csv', index=False)

if __name__ == '__main__':
    main()


