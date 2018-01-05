import json
import requests
import math
url="https://backend-challenge-summer-2018.herokuapp.com/challenges.json"
cur_list=[]
def get_json(url, challenge_id):
	payload={'page':1, 'id':challenge_id}
	response=requests.get(url, params=payload).json()
	pagination=response['pagination']
	total_pages=math.ceil(pagination['total']/pagination['per_page'])
	
	while(payload['page']<total_pages):
		payload['page']+=1
		secondary_response=requests.get(url, params=payload).json()
		for menu in secondary_response['menus']:
			response['menus'].append(menu)
	return response

def check_child(parent_id, child, response):
	cur_list.append(child)
	if(parent_id != response['menus'][child-1].get('parent_id', 0)):
		return 1
	if(len(response['menus'][child-1]['child_ids'])==0):
		return 0
	loop=0
	for new_child in response['menus'][child-1]['child_ids']:
		loop=loop+check_child(child, new_child, response)
	return loop

response=get_json(url,2)

valid_menus=[]
invalid_menus=[]
for menu in response['menus']:
	if('parent_id' not in menu):
		loop=0
		cur_list=[]
		for child in menu['child_ids']:
			loop=loop+check_child(menu['id'], child, response)
		print(cur_list)









