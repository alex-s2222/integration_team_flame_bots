import requests
from loguru import logger

def get_projects(TOKEN, space_id):
    projects = {}
    URL = 'https://api.test-team-flame.ru/project/projectsBySpace/' + space_id 
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for space in data:
            space_id = space['id']
            name = space['name']
            projects[space_id] = name
        return projects 
    

def create_project(TOKEN, space_id, project_name, key_project):
    URL = 'https://api.test-team-flame.ru/project/create'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {"name": project_name,
            "logo": "https://play-lh.googleusercontent.com/ZyWNGIfzUyoajtFcD7NhMksHEZh37f-MkHVGr5Yfefa-IX7yj9SMfI82Z7a2wpdKCA=w240-h480-rw",
            "space": space_id,
            "color": "#ffffff",
            "private": False,
            "projectKey": "RUS-"+key_project,
            "location": space_id}
    
    response = requests.post(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
        return False
    else:
        logger.info(response.text)
        return True
    

def delete_project(TOKEN, space_id, project_id):
    URL = 'https://api.test-team-flame.ru/project/delete/' + project_id
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {'location': space_id}

    response = requests.delete(url=URL, headers=headers, json=data)
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
        return False
    else:
        logger.info(response.text)
        return True