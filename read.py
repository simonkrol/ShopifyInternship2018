import json
import requests
import math
url="https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page="
def get_json(url):
	page=1
	response=requests.get(url+str(page)).json()
	pagination=response['pagination']
	total_pages=math.ceil(pagination['total']/pagination['per_page'])
	page+=1
	print(total_pages)
	while(page<=total_pages):
		secondary_response=requests.get(url+str(page)).json()
		for menu in secondary_response['menus']:
			response['menus'].append(menu)
		page+=1
	print(len(response['menus']))


response=requests.get("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page=1")
json_data=response.json()
get_json(url)
#for menu in json_data['menus']:
#	print(menu)





