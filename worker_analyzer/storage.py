import os
from datetime import datetime
import json

class LocalStorage:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def _prepare_data_for_json(data):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, dict):
                data[key] = LocalStorage._prepare_data_for_json(value)
            elif isinstance(value, list):
                data[key] = [LocalStorage._prepare_data_for_json(item) if isinstance(item, dict) else item for item in value]
        return data

    def save(self, session:dict):
        if not isinstance(session, dict):
            raise TypeError("Expected dictionary for 'session'")
        
        os.makedirs(self.path, exist_ok=True)
        formatted_date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f'{formatted_date}_{session["id"]}.json'
        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'w') as f:
            json.dump(LocalStorage._prepare_data_for_json(session), f)

