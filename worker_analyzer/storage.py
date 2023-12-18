import os
import json

from datetime import datetime
from pymongo import MongoClient
from .common import StorageFunctions


class LocalStorage(StorageFunctions):
    def __init__(self, path):
        if not isinstance(path, str) or not path:
            raise ValueError("Path must be a non-empty string")
        # Verify path ended with '/' and remove it
        if path[-1] == "/":
            path = path[:-1]

        self.path = path

    def save(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("Expected dictionary for 'session'")

        try:
            os.makedirs(self.path, exist_ok=True)
        except OSError as e:
            raise Exception(f"Failed to create directory")

        formatted_date = datetime.now().strftime("%Y%m%d%H%M%S")
        identifier = data.get("id") if data.get("id") else "report"
        file_name = f"{formatted_date}_{identifier}.json"
        file_path = os.path.join(self.path, file_name)

        try:
            with open(file_path, "w") as f:
                json.dump(self.date_to_isoformat(data), f)
        except OSError as e:
            raise Exception(f"Failed to write to file")


class MongoStorage(StorageFunctions):


    def __init__(self, connection, collection):
        self.connection = connection
        self.collection_name = collection
        self.client = None
        self.sessions = None


    def parse_url():
        pass

    def create_connection(self):
        ''' Método responsável por criar a cadeia de conexão e acessar client MongoDB.
        '''
        if 'url' not in self.connection or 'database' not in self.connection:
            raise ValueError("Connection dictionary must contain 'url' and 'database'")

        if not self.connection['url']:
            raise ValueError("URL in connection dictionary cannot be null")

        try:
            # Remova a porta da URL
            url_without_port = self.connection['url'].split(':')[0]
            print(url_without_port)
            self.client = MongoClient(url_without_port)
            self.sessions = self.client[self.connection['database']][self.collection_name]
        except Exception as e:
            raise ConnectionError(f"Error creating connection: {str(e)}")

        # if 'url' not in self.connection or 'database' not in self.connection:
        #     raise ValueError("Connection dictionary must contain 'url' and 'database'")

        # if not self.connection['url']:
        #     raise ValueError("URL in connection dictionary cannot be null")

        # try:
        #     url_without_port = self.connection['url'].split(':')[0]
        #     self.client = MongoClient(url_without_port)
        #     # self.client = MongoClient(self.connection['url'])
        #     self.sessions = self.client[self.connection['database']][self.collection_name]
        # except Exception as e:
        #     raise ConnectionError(f"Error creating connection: {str(e)}")


    def test_connection(self):
        ''' Valida se a conexão está ativa, se o database e a collection existe. Em caso negativo, retornar false e exception.test
        '''
        if not self.client:
            return False

        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            raise ConnectionError(f"Connection test failed: {str(e)}")


    def connect(self):
        ''' Método responsável por criar a conexão, testar e retornar True ou False. Em caso de erro, retornar detalhamento do exception.
        '''
        try:
            self.create_connection()
            return self.test_connection()
        except Exception as e:
            return str(e)


    def save(self, session):
        ''' Recebe como parâmetro um dicionário Python chamado `session` que deve ser armazenado na `collection` informada. Deve retornar um status: Success ou Failure e o ID do documento que foi criado no MongoDB.
        '''
        if not isinstance(session, dict):
            return False, "Input is not a dictionary"

        try:
            # Transforma timestamps em strings, se houver
            session = self.date_to_isoformat(session)

            result = self.sessions.insert_one(session)
            return True, str(result.inserted_id)
        except Exception as e:
            return False, str(e)
