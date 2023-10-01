import requests
from loguru import logger

def get_boards(TOKEN, project_id):
    boards = {}
    URL = 'https://api.test-team-flame.ru/board/boardsByProject/' + project_id
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for board in data:
            board_id = board['id']
            name = board['name']
            boards[board_id] = name
        return boards


def delete_board(TOKEN, space_id, board_id):
    URL = 'https://api.test-team-flame.ru/board/delete/' + board_id
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
    

def create_board(TOKEN, space_id, board_name, project_id):
    URL = 'https://api.test-team-flame.ru/board/create'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    data = {"name": board_name,
            "logo": "",
            "projectId": project_id,
            "spaceId": space_id,
            "color": "#ffffff",
            "location": space_id}
    
    response = requests.post(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
        return False
    else:
        logger.info(response.text)
        return True