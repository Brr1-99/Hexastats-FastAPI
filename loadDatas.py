import requests
from interfaces import build_champ,build_player
from loadMasteries import load_mastery
from bs4 import BeautifulSoup, ResultSet


def get_ranked_data(doc: ResultSet, mode: str) -> str:
	# Fetch some repetitive data
	image = doc.find('div', class_='css-1v663t e1x14w4w1').findChild('img')['src'].split('?')[0]
	try :
		rank = doc.find_all('div', class_='tier')[mode].text
		lp = int(doc.find_all('div', class_='lp')[mode].text.split(' ')[0])
		win = int(doc.find_all('div', class_='win-lose')[mode].text.split(' ')[0][:-1])
		lose = int(doc.find_all('div', class_='win-lose')[mode].text.split(' ')[1][:-1])
		winrate = int(doc.find_all('div', class_='ratio')[mode].text.split(' ')[-1][:-1])

	except ValueError:
		rank = 'Unranked'
		lp = 0
		win = 0
		lose = 0
		winrate = 0
	
	return image, rank, lp, win, lose, winrate

def load_data(ok_server: str, headers: str, player: str) -> dict:
	# Fetch OPGG data for a player
	data = []
	opgg = f"https://{ok_server}.op.gg/summoner/userName={player}"
	result = requests.get(opgg, headers=headers).text
	document = BeautifulSoup(result, 'html.parser')

	alias = player

	image = document.find('div', class_='profile-icon').findChild('img')['src']
	level = int(document.find('div', class_='profile-icon').findChild('span').text)

	# Fetch solo/duo data 
	image_s, rank_s, lp_s, win_s, lose_s, winrate_s = get_ranked_data(document, 0)

	try:
		global_ranking = int(document.find('span', class_='ranking').string.replace(',',''))
		percent_better_players = float(document.find('div', class_='rank').findChild('a').text.split('(')[1].split('%')[0])

	except AttributeError:
		global_ranking = 0
		percent_better_players = 0

	# Fetch flex data 
	image_f, rank_f, lp_f, win_f, lose_f, winrate_f = get_ranked_data(document, 1)

	# Fetch 10 most played champions data

	champions = f"https://www.op.gg/_next/data/w5wAhn-XD9o_8LpBUs6vL/summoners/{ok_server}/{player}/champions.json"
	result2 = requests.get(champions, headers=headers).json()
	champs_data = result2['pageProps']['data']['most_champions']['champion_stats']

	champs = []

	for champ in champs_data[:10]:
		id = champ['id']
		games = champ['play']

		winrate = round(100*champ['win']/games)

		kills = round(champ['kill']/games, 1)
		deaths = round(champ['death']/games, 1)
		assists = round(champ['assist']/games, 1)
		kda = round((kills+assists)/deaths, 1)

		cs = round((champ['minion_kill']+champ['neutral_minion_kill'])/games, 1)
		gold = round(champ['gold_earned']/games)

		max_kills = champ['most_kill']
		max_deaths = champ['max_death']
		
		avg_damage_dealt = round(champ['damage_dealt']/games)
		avg_damage_taken = round(champ['damage_taken']/games)

		double_kills = champ['double_kill']
		triple_kills = champ['triple_kill']
		quadra_kills = champ['quadra_kill']
		penta_kills = champ['penta_kill']

		champs.append(build_champ(id=id, winrate=winrate,
		kda=kda, kills=kills, deaths=deaths, assists=assists, cs=cs, gold=gold,
		max_kills=max_kills, max_deaths=max_deaths, avg_damage_dealt=avg_damage_dealt, avg_damage_taken=avg_damage_taken,
		double_kills=double_kills, triple_kills=triple_kills, quadra_kills=quadra_kills, penta_kills=penta_kills))

	masteries=load_mastery(ok_server, player, headers) 

	data= build_player(
	alias=alias, image=image, level=level, rank_n=global_ranking, rank_p=percent_better_players,
	rank_s=rank_s, image_s=image_s, lp_s=lp_s, win_s=win_s, lose_s=lose_s, winrate_s=winrate_s,
	rank_f=rank_f, image_f=image_f, lp_f=lp_f, win_f=win_f, lose_f=lose_f, winrate_f=winrate_f, champs=champs, masteries=masteries)

	return data