import requests
from loguru import logger

def get_columns(TOKEN, board_id):
    columns = {}
    URL = 'https://api.test-team-flame.ru/column/getByBoard/' + board_id +'?hideClosed=true'
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for column in data:
            column_id = column['id']
            name = column['name']
            columns[column_id] = name
        return columns



def delete_column(TOKEN, space_id, column_id):
    URL = 'https://api.test-team-flame.ru/column/delete/' + column_id
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
    

def create_column(TOKEN, space_id, column_name, board_id, project_id):
    URL = 'https://api.test-team-flame.ru/column/create'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {"name": column_name,
            "boardId": board_id,
            "color": "#ffffff",
            "location": space_id,
            "projectId": project_id,
            "spaceId": space_id}
    
    response = requests.post(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
        return False
    else:
        logger.info(response.text)
        return True