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

def check_child(parent_id, child):
	cur_list.append(child)
	#If where we came from isnt the same as the parent id
	if(parent_id != menus[child-1].get('parent_id', 0)):
		return 1
	#If the current child has no further children
	if(len(menus[child-1]['child_ids'])==0):
		return 0
	cycle_count=0
	#Iterate through each new child node
	for new_child in menus[child-1]['child_ids']:
		cycle_count+=check_child(child, new_child)
	return cycle_count

menus=get_json(url,2)['menus']

valid_menus=[]
invalid_menus=[]
for menu in menus:
	if('parent_id' not in menu):
		cycle=0
		cur_list=[]

		for child in menu['child_ids']:
			cycle+=check_child(menu['id'], child)
		temp_dict={"root_id":menu['id'],"children":cur_list}
		if(cycle>0):
			invalid_menus.append(temp_dict)
		else:
			valid_menus.append(temp_dict)
final_dict={"valid_menus":valid_menus, "invalid_menus":invalid_menus}
print(final_dict)









