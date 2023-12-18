import unittest

from pymongo import MongoClient
from worker_analyzer.storage import MongoStorage

class TestMongoStorage(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # Configuração inicial (executada uma vez antes de todos os testes)
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
        # Limpeza após todos os testes (executada uma vez após todos os testes)
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
        self.assertIsNotNone(self.storage.sessions)


    def test_test_connection(self):
        self.storage.create_connection()
        self.assertTrue(self.storage.test_connection())


    def test_connect(self):
        self.assertTrue(self.storage.connect())


    def test_save(self):
        session = {"key": "value"}
        success, _ = self.storage.save(session)
        self.assertTrue(success)


    def test_save_invalid_input(self):
        session = "not_a_dictionary"
        success, _ = self.storage.save(session)
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
