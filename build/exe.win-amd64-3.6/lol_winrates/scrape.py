from bs4 import BeautifulSoup
import requests
import json

#Makes a list of top 10 champions by tier based on role data.
def tierlist_list(data):
	tierlist_list_out = []
	for champ in data.find_all('div', class_='champion-index-table__name'):
		if len(tierlist_list_out) >= 5: break
		tierlist_list_out.append(champ.text.replace(' ','').replace("'","").replace(".","").replace(" & Willump", ""))

	return tierlist_list_out


#Makes a list of the winrates of champions by tier based on role data.
def winrate_list(data):
	winrate_list_out = []
	value_count = 2
	for champ_winrate in data.find_all('td', class_='champion-index-table__cell champion-index-table__cell--value'):
		if value_count == 30: break
		value_count += 1
		if value_count % 3 == 0:
			winrate_list_out.append(champ_winrate.text)

	return winrate_list_out

#Makes a list of the pickrates of champions by tier based on role data.
def pickrate_list(data):
	winrate_list_out = []
	value_count = 1
	for champ_winrate in data.find_all('td', class_='champion-index-table__cell champion-index-table__cell--value'):
		if value_count == 30: break
		value_count += 1
		if value_count % 3 == 0:
			winrate_list_out.append(champ_winrate.text)

	return winrate_list_out

#https://opgg-static.akamaized.net/images/lol/champion/Zac.png?image=q_auto,w_140&v=1581511032
def make_tierlist(champ_list, winrate_list, pickrate_list):
	tierlist_out = {}
	for i in range(len(champ_list)):
		tierlist_out[champ_list[i]] = [winrate_list[i]] 
		tierlist_out[champ_list[i]].append("https://opgg-static.akamaized.net/images/lol/champion/{}.png?image=q_auto,w_140&v=1581511032".format(champ_list[i]))
		tierlist_out[champ_list[i]].append(pickrate_list[i])

	return tierlist_out



source = requests.get('https://na.op.gg/champion/statistics').text

soup = BeautifulSoup(source, 'lxml')

#HTML Parsing for roles
top_data = soup.find('tbody', class_='tabItem champion-trend-tier-TOP')
jungle_data = soup.find('tbody', class_='tabItem champion-trend-tier-JUNGLE')
mid_data = soup.find('tbody', class_='tabItem champion-trend-tier-MID')
adc_data = soup.find('tbody', class_='tabItem champion-trend-tier-ADC')
support_data = soup.find('tbody', class_='tabItem champion-trend-tier-SUPPORT')

#Top 10 chmapions in each role by tier in order
top_tierlist_champion = tierlist_list(top_data)
jungle_tierlist_champion = tierlist_list(jungle_data)
mid_tierlist_champion = tierlist_list(mid_data)
adc_tierlist_champion = tierlist_list(adc_data)
support_tierlist_champion = tierlist_list(support_data)

#Winrates of the top 10 champions in each role by tier in order
top_tierlist_winrate = winrate_list(top_data)
jungle_tierlist_winrate = winrate_list(jungle_data)
mid_tierlist_winrate = winrate_list(mid_data)
adc_tierlist_winrate = winrate_list(adc_data)
support_tierlist_winrate = winrate_list(support_data)

#Pickrates of the top 10 champions in each role by tier in order
top_tierlist_pickrate = pickrate_list(top_data)
jungle_tierlist_pickrate = pickrate_list(jungle_data)
mid_tierlist_pickrate = pickrate_list(mid_data)
adc_tierlist_pickrate = pickrate_list(adc_data)
support_tierlist_pickrate = pickrate_list(support_data)

#Combining top 10 champions with their corresponsing winrates.
top_tierlist = make_tierlist(top_tierlist_champion, top_tierlist_winrate, top_tierlist_pickrate)
jungle_tierlist = make_tierlist(jungle_tierlist_champion, jungle_tierlist_winrate, jungle_tierlist_pickrate)
mid_tierlist = make_tierlist(mid_tierlist_champion, mid_tierlist_winrate, mid_tierlist_pickrate)
adc_tierlist = make_tierlist(adc_tierlist_champion, adc_tierlist_winrate, adc_tierlist_pickrate)
support_tierlist = make_tierlist(support_tierlist_champion, support_tierlist_winrate, support_tierlist_pickrate)

