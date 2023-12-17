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


    def __init__(self, connection: dict, collection: str):

        pass


    def create_connection(connection, collection):
        ''' Método responsável por criar a cadeia de conexão e acessar client MongoDB.
        '''
    # - Deve validar se o dicionário connection tem todos as keys necessárias (url, database)
    # - Deve validar se a URL não é nula
    # - Deve instanciar o client MongoDB
        pass


    def test_connection():
        # Valida se a conexão está ativa, se o database e a collection existe. Em caso negativo, retornar false e exception.test
        pass


    def connect():
        # Método que será responsável por criar a conexão, testar e retornar true ou false. Em caso de erro, retornar detalhamento do exception.
        pass


    def save():
        ''' Recebe como parâmetro um Dicionário Python chamado session que deve ser armazenado na collection informada. Deve retornar um status: Success ou Failure e o ID do documento que foi criado no MongoDB.
        '''
        # - Deve verificar se realmente é um dicionário
        # - Deve tratar valores timestamp
