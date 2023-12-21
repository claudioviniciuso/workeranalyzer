import unittest
from unittest.mock import MagicMock, patch

from pymongo import MongoClient
from worker_analyzer.storage import MongoStorage

class TestMongoStorage(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # Configuração inicial
        cls.connection = {
            "url": "mongodb://localhost:27017/",
            "database": "test_workeranalyser"
        }
        cls.collection = "test_collection"
        cls.client = MongoClient(cls.connection["url"])
        cls.db = cls.client[cls.connection["database"]]
        cls.db.create_collection(cls.collection)


    @classmethod
    def tearDownClass(cls):
        # Limpeza após todos os testes
        cls.client.drop_database(cls.connection["database"])
        cls.client.close()


    def setUp(self):
        # Configuração antes de cada teste
        self.storage = MongoStorage(self.connection, self.collection)


    def tearDown(self):
        # Limpeza após cada teste
        self.storage = None


    def test_create_connection(self):
        self.storage.create_connection()
        self.assertIsNotNone(self.storage.client)
        self.assertIsNotNone(self.storage.database)


    def test_test_connection(self):
        self.storage.create_connection()
        self.assertTrue(self.storage.test_connection())


    def test_connect(self):
        self.assertTrue(self.storage.connect())


    def test_save(self):
        self.storage.connect()
        session = {"testing": "test_save"}
        success, _ = self.storage.save(session)
        self.assertTrue(success)


    def test_save_invalid_input(self):
        self.storage.connect()
        session = "not_a_dictionary"
        success, _ = self.storage.save(session)
        self.assertFalse(success)


    def test_save_connection_not_active(self):
        with self.assertRaises(Exception) as context:
            session = {"testing": "test_save_connection_not_active"}
            self.storage.save(session)

        self.assertEqual(str(context.exception), "Connection is not active")


    def test_raise_exception_when_connection_not_have_database(self):
        connection = {
            "url": "mongodb+srv://localhost:27017/",
        }
        storage = MongoStorage(connection, '')

        with self.assertRaises(ValueError) as context:
            storage.create_connection()

        self.assertEqual(str(context.exception), "Database cannot be empty")


    @patch('pymongo.MongoClient')
    def test_save_connection_not_active(self, mock_mongo_client):
        # Configura o mock para simular uma conexão não ativa
        mock_client = MagicMock()
        mock_client.is_primary = False
        mock_client.connected = False
        mock_mongo_client.return_value = mock_client

        # Testa o método save
        with self.assertRaises(Exception) as context:
            session = {"key": "value"}
            self.storage.save(session)

        self.assertEqual(str(context.exception), "Connection is not active")


    def test_extrair_info_url_mongodb(self):
        urls = [
            {
                "url": 'mongodb://localhost:27017/testing',
                "url_sem_db": 'mongodb://localhost:27017/',
                "database_compare": 'testing'
            },
            {
                "url": 'mongodb+srv://testing:q1w2e3r4@localhost:27017/testing?retryWrites=true&w=majority',
                "url_sem_db": 'mongodb+srv://testing:q1w2e3r4@localhost:27017/?retryWrites=true&w=majority',
                "database_compare": 'testing'
            },
            {
                "url": 'mongodb://localhost:27017',
                "url_sem_db": 'mongodb://localhost:27017/',
                "database_compare": ''
            },
        ]

        for url in urls:
            storage = MongoStorage(url, '')
            url_sem_db, database = storage.extrair_info_url_mongodb(url["url"])

            self.assertEqual(url_sem_db, url["url_sem_db"])
            self.assertEqual(database, url["database_compare"])


if __name__ == "__main__":
    unittest.main()
