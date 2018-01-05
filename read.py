import json
import requests
response=requests.get("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page=1")
json_string=response.json()
print(json_string)

