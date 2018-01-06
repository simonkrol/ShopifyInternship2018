import math

import json
import requests
import copy

# The rest api endpoint for this challenge and the example id.
_url='https://backend-challenge-summer-2018.herokuapp.com/challenges.json'
_example_id = 2


def get_json():
    """Generates the json response.

    Reads the pagination to combine all given pages of json data. 
    Uses the url and example_id listed above. Returns a json response.

    Returns json response, a dictionary containing menus and pagination
    """
    payload = {'page':1, 'id':_example_id}
    response = requests.get(_url, params=payload).json()
    pagination = response['pagination']
    total_pages = math.ceil(pagination['total']/pagination['per_page'])
    while(payload['page']<total_pages):  
        payload['page'] += 1
        for menu in requests.get(_url, params=payload).json()['menus']:
            response['menus'].append(menu)
    return response


def check_child(parent_id, child_id):
    """Check for cycle in child_id branch of menus

    Check if the childs parent_id matches the menu that pointed
    to it. This being false is indicative of a cycle. Is also
    responsible for compiling the list of child nodes. Recursively
    searches through the child_id's entire branch to locate cycles.

    Arguments:
    parent_id -- the id of the menu that pointed to the child
    child_id -- the id of the child being checked

    Returns 1 if a cycle was found in this branch of menus. 
    Returns 0 otherwise.
    """
    global cur_list, menus
    cur_list.append(child_id)
    child_data = menus[child_id - 1]
    #If previous menu isnt the same as the parent id
    if(parent_id != child_data.get('parent_id', 0)):
        return 1

    #If the current child has no further children
    if(len(child_data['child_ids']) == 0):
        return 0

    cycle_count = 0
    #Iterate through each new child node
    for new_child_id in child_data['child_ids']:
        cycle_count += check_child(child_id, new_child_id)

    return cycle_count


def validate():
    """Validate that no cycles exist in the retrieved menus.

    Creates a dictionary storing a list of valid and a list of
    invalid menu paths. Each path stores a dictionary containing
    the path's root_id as well as all children of that root menu.
    Valid paths are those that have no cycles within them.
   
    Returns the dictionary storing the valid and invalid lists.
    """
    global cur_list, menus
    menus=get_json()['menus']

    validation={'valid_menus':[], 'invalid_menus':[]}
    
    for menu in menus:
        if('parent_id' not in menu):
            cycle = 0
            cur_list=[]
            for child in menu['child_ids']:
                cycle += check_child(menu['id'], child)
            temp_dict = {'root_id':menu['id'], 'children':cur_list}
            if(cycle>0):
                validation['invalid_menus'].append(copy.deepcopy(temp_dict))
            else:
                validation['valid_menus'].append(copy.deepcopy(temp_dict))
    print(validation)
    return validation


validate()







