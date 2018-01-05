import json
import requests
import math
url="https://backend-challenge-summer-2018.herokuapp.com/challenges.json"
cur_list=[]
def get_json(url, challenge_id):
	page=1
	payload={'page':page, 'id':challenge_id}
	response=requests.get(url, params=payload).json()
	pagination=response['pagination']
	total_pages=math.ceil(pagination['total']/pagination['per_page'])
	page+=1
	print(total_pages)
	while(page<=total_pages):
		payload['page']=page
		secondary_response=requests.get(url, params=payload).json()
		for menu in secondary_response['menus']:
			response['menus'].append(menu)
		page+=1
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

# def gen_menu(id, repeat):
# 	menu_dict=dict()
# 	total_children=0
# 	menu_dict['root_id']=id;
# 	child=set()
# 	child.update(response['menus'][id-1]['child_ids'])
# 	total_children+=len(response['menus'][id-1]['child_ids'])
# 	print(child)
	

# def get_kids(id):
# 	return response['menus'][id-1]['child_ids']

response=get_json(url,2)
# gen_menu(2, False)
# for menu in response['menus']:
# 	print(menu)
valid_menus=[]
invalid_menus=[]
for menu in response['menus']:
	if('parent_id' not in menu):
		loop=0
		cur_list=[]
		for child in menu['child_ids']:
			loop=loop+check_child(menu['id'], child, response)
		print(cur_list)









