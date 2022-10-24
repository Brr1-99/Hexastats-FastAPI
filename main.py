import requests
from fastapi import FastAPI, Header
from whitelist import validate_server
from loadDatas import load_data

# Headers to avoid bot protection
headers = requests.utils.default_headers()
headers.update({
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
})


app = FastAPI()

@app.get("/get_player/{player}/{server}")
async def home(
	player: str = Header(description="The alias of the player"), 
	server: str = Header(description="The server in which the player is located")
	)-> dict:

	ok_server = validate_server(server)

	return load_data(ok_server, headers, player)
	