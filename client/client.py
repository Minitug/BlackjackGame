import requests

response = requests.get("http://127.0.0.1:8000/hello")

data = response.json()
print(data["message"])

response = requests.post("http://127.0.0.1:8000/game/start")
data = response.json()

print(data["message"])
print(f"Minimum bet: ${data['minimum_bet']}")

requests.post("http://127.0.0.1:8000/game/start")

response = requests.get("http://127.0.0.1:8000/game/state")
print(response.json())