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
    

if __name__ == '__main__':
    TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsZXgtczIyMjJAbWFpbC5ydSIsInVzZXJJZCI6IjY1MTc0MTAwZWMxZGNjYjBkMzMwYmJlYiIsImlhdCI6MTY5NjA0MTQyMiwiZXhwIjoxNjk2MzQxNDIyfQ.Dbu2qDp-jMa84h4TpOMx3RLhv6PrIXV0LyGCt1eRFew'
    spaces = get_user_spaces(TOKEN)
    logger.info(spaces)
    projects = []
    for id, name in spaces.items():
        projects.append(get_user_projects(TOKEN, id))

    logger.info(projects)