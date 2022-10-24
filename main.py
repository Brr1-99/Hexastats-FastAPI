from fastapi import FastAPI, Query
from getData import get_data
import json

app = FastAPI()

@app.get("/get_players/")
async def home(players: str = Query(description="The alias of the players"), server: str = Query(description="The key of the server in which the player is located")):
	try:
		# singleMode: ?players=Bruno&server=euw
		# multiMode: ?players=Bruno,Alex&server=euw

		# Probably not correct data
		if len(players) < 3:
			players = []
		# Remove end comma if exists
		elif players[-1] == ',':
			players = players[:-1]

		# Now everything is ok, split the players
		players = players.split(',')

		# There is 1 or multiple players?
		singleMode = len(players) == 1
	except (AttributeError , IndexError , TypeError):
		return json.dumps([])
	# Everything went ok: process the data
	gamers = get_data(players, server, singleMode)
	return gamers