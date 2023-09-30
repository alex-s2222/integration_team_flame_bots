import requests
from loguru import logger


def get_user_spaces(TOKEN):
    """Получаем имена и id пространства"""
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


def get_user_projects(TOKEN, space_id):
    """получаем имена и id проектов"""
    projects = {}
    URL = 'https://api.test-team-flame.ru/project/projectsBySpace/' + space_id
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)
    
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for project in data:
            project_id = project['id']
            name = project['name']
            projects[project_id] = name
        return projects
    
def delete_user_space(TOKEN):
    URL = 'https://api.test-team-flame.ru/space/delete'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {'id':'65186775e0d83c7a77ffb34a'}

    response = requests.delete(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
    else:
        logger.info(response.text)

    
    

if __name__ == '__main__':
    TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsZXgtczIyMjJAbWFpbC5ydSIsInVzZXJJZCI6IjY1MTc0MTAwZWMxZGNjYjBkMzMwYmJlYiIsImlhdCI6MTY5NjA3MTA1NSwiZXhwIjoxNjk2MzcxMDU1fQ.H9oGphVuV4x9Do4Whbjf6qzdF6PXUKy1a5cRwC5knls'
    delete_user_space(TOKEN)