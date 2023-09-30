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