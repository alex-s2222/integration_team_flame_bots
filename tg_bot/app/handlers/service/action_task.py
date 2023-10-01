import requests
from loguru import logger
from datetime import datetime


def get_task(TOKEN, column_id):
    tasks = {}
    URL = 'https://api.test-team-flame.ru/task/getTasksByColumn/' + column_id
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url=URL, headers=headers)
    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        for task in data:
            task_id = task['id']
            name = task['name']
            tasks[task_id] = name
        return tasks
    

def delete_task(TOKEN, space_id, task_id):
    URL = 'https://api.test-team-flame.ru/task/delete/' + task_id
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
    

def create_task(TOKEN, space_id, column_id, task_name):
    URL = 'https://api.test-team-flame.ru/task/create'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    data = {"name": task_name,
            "description": "",
            "priority": "",
            "status": [
                "to-do"
            ],
            "columnId": column_id,
            "files": [],
            "users": [],
            "dependenceOf": [],
            "subTasks": [],
            "startDate": now,
            "endDate": now,
            "location": space_id}
    
    response = requests.post(url=URL, headers=headers, json=data)

    if (response.status_code >= 200) and (response.status_code < 300):
        data = response.json()
        logger.info(data)
        return False
    else:
        logger.info(response.text)
        return True