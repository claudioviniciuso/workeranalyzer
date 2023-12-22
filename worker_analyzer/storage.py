import os
import json

from datetime import datetime
from pymongo import MongoClient
from urllib.parse import urlparse
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
        self.database = None
        self.client = None


    def extrair_info_url_mongodb(self, url):
        # Analisa a URL
        parsed_url = urlparse(url)
        # Obtém a URL sem o nome do banco de dados
        url_sem_db = f"{parsed_url.scheme}://{parsed_url.netloc}/"

        if parsed_url.query:
            url_sem_db += f"?{parsed_url.query}"

        # Obtém o nome do banco de dados, se presente
        database = parsed_url.path[1:]  # Ignora a barra inicial
        # print(f"extrair_info_url_mongodb: {url_sem_db}, {database}")
        return url_sem_db, database


    def create_connection(self):
        ''' Método responsável por criar a cadeia de conexão e acessar client MongoDB.
        '''

        if 'url' not in self.connection:
            raise ValueError("Connection dictionary must contain 'url'")

        if not self.connection['url']:
            raise ValueError("URL in connection dictionary cannot be null")

        # se database não exister no dict `connection` passado, vai tentar
        # verificar se existe database na url de `connection`
        if not 'database' in self.connection:
            url, database = self.extrair_info_url_mongodb(self.connection['url'])

            if not database:
                raise ValueError("Database cannot be empty")

        # Se chegar aqui, significa que passou pelas validações e esta tudo
        # definido no dict `connection`
        if 'database' not in locals():
            database = self.connection['database']

        if 'url' not in locals():
            url = self.connection['url']

        try:
            self.client = MongoClient(url)
            self.database = self.client[database]

        except Exception as e:
            raise ConnectionError(f"Error creating connection: {str(e)}")


    def test_connection(self):
        ''' Valida se a conexão está ativa, se o database e a collection existe.
        Em caso negativo, retornar false e exception.test
        '''
        if not self.client:
            return False

        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            raise ConnectionError(f"Connection test failed: {str(e)}")


    def connect(self):
        ''' Método responsável por criar a conexão, testar e retornar True ou
        False. Em caso de erro, retorna detalhamento do `Exception`.
        '''
        try:
            self.create_connection()
            return self.test_connection()
        except Exception as e:
            return str(e)


    def save(self, session: dict):
        ''' Recebe como parâmetro um dicionário Python chamado `session` que deve
        ser armazenado na `collection` informada. Deve retornar um status:
        `Success` ou `Failure` e o ID do documento que foi criado no MongoDB.
        '''
        if not isinstance(session, dict):
            return False, "Input is not a dictionary"

        if not self.client or (not self.client.is_primary and not self.client.connected):
            raise Exception("Connection is not active")

        try:
            # Transforma timestamps em strings, se houver
            session = self.date_to_isoformat(session)

            new_doc = self.database[self.collection_name].insert_one(session)
            return True, str(new_doc.inserted_id)

        except Exception as e:
            return False, str(e)
