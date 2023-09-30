import requests

def get_user_spaces(TOKEN):
    spaces = {}
    URL = 'https://api.test-team-flame.ru/space/spacesByUserId'
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)
    
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for space in data:
            space_id = space['id']
            name = space['name']
            spaces[space_id] = name
        return spaces
    

def delete_user_space(TOKEN, space_id):
    URL = 'https://api.test-team-flame.ru/space/delete'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {'id': space_id}

    response = requests.delete(url=URL, headers=headers, json=data)
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        return False
    else:
        return True
    
    
def create_user_space(TOKEN, space_name):
    URL = 'https://api.test-team-flame.ru/space/create'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {"name": space_name,
            "logo": "",
            "color": "#ffffff",
            "invites": []}
    response = requests.post(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        return False
    else:
        return True
