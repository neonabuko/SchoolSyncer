from typing import Any, Dict
import requests
from messages import Messages

API_URL = "http://100.102.72.128:5170/"

status_outputs = Messages()


def handle_post(route: str, post_data: Dict[str, Any], query_param: Dict[str, str]):
    entity_name = query_param.get('name')
    post_response = requests.post(API_URL + route, json=post_data)
    
    if post_response.status_code == 200: 
        status_outputs.ok(entity_name)
        return post_response.json()
    
    elif post_response.status_code == 409:
        query_response = requests.get(API_URL + f'{route}/by-name', params=query_param)
        status_outputs.conflict(entity_name)
        
        if query_response.status_code == 200: 
            if query_response.json():
                return query_response.json()[0]
        
        return None
    
    raise requests.HTTPError(post_response.reason)

