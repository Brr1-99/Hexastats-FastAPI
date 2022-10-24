import requests
from interfaces import build_champ,build_player
from loadMasteries import load_mastery
from bs4 import BeautifulSoup, ResultSet

# Function to factor the extraction of several data
def get_cells_text(doc: ResultSet, x: int) -> int:
	try:
		result = int(doc[x+5].text)
	except:
		result = 0
	return result

def get_ranked_data(doc: ResultSet, mode: str) -> str | int:
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
	data = []
	# Fetch OPGG data for a player
	opgg = "https://"+ ok_server + '.op.gg/summoner/userName=' + player
	result = requests.get(opgg, headers=headers).text
	document = BeautifulSoup(result, 'html.parser')


	champions = "https://op.gg/summoners/" + ok_server + '/' + player + "/champions"
	result2 = requests.get(champions, headers=headers).text
	document2 = BeautifulSoup(result2, 'html.parser')

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

	champs_more_data = document2.find('table', class_='css-147gr6a exo2f213').findChildren('td')

	champs = []

	# Fetch champions data
	for index,champ in enumerate(champs_more_data):

		main_cells = champ[index].find_all('td', class_='css-1wvfkid exo2f211')
		name_champ = main_cells[0].find('div', class_='summoner-name').findChild('a').text
		image_champ = main_cells[0].find('div', class_='summoner-image').findChild('img')['src']

		winrate = int(main_cells[1].find('span', class_='text  red ').text[:-1])

		cells = champ[index].find_all('td', class_='value css-1wvfkid exo2f211')

		try:
			kda = float(cells[0].findChild('strong', class_='css-s6j0s e7m7tjk1').text.split(':')[0])
		except ValueError:
			kda = 100

		kills = float(cells[0].findChild('div', class_='kda').text.split('/')[0])
		deaths = float(cells[0].findChild('div', class_='kda').text.split('/')[1])
		assists = float(cells[0].findChild('div', class_='kda').text.split('/')[2])
		
		gold = get_cells_text(cells, 1)
		cs = get_cells_text(cells, 2)
		max_kills = get_cells_text(cells, 3) 
		max_deaths = get_cells_text(cells, 4) 
		avg_damage_dealt = get_cells_text(cells, 5) 
		avg_damage_taken = get_cells_text(cells, 6) 

		double_kills = get_cells_text(cells, 2)
		triple_kills = get_cells_text(cells, 3)
		quadra_kills = get_cells_text(cells, 4)
		penta_kills = get_cells_text(cells, 5)

		champs.append(build_champ(name=name_champ, image=image_champ, winrate=winrate,
		kda=kda, kills=kills, deaths=deaths, assists=assists, cs=cs, gold=gold,
		max_kills=max_kills, max_deaths=max_deaths, avg_damage_dealt=avg_damage_dealt, avg_damage_taken=avg_damage_taken,
		double_kills=double_kills, triple_kills=triple_kills, quadra_kills=quadra_kills, penta_kills=penta_kills))

	masteries=load_mastery(ok_server, player, headers) 

	data= build_player(
	alias=alias, image=image, level=level, rank_n=global_ranking, rank_p=percent_better_players,
	rank_s=rank_s, image_s=image_s, lp_s=lp_s, win_s=win_s, lose_s=lose_s, winrate_s=winrate_s,
	rank_f=rank_f, image_f=image_f, lp_f=lp_f, win_f=win_f, lose_f=lose_f, winrate_f=winrate_f, champs=champs, masteries=masteries)

	return data