import os

diretorio_atual = os.getcwd()
print("Diretório Atual:", diretorio_atual)

from worker_analyzer.storage import MongoStorage

# Connection Dict
connection = {
		"url": "mongodb+srv://testing:q1w2e3r4@localhost:27017/?retryWrites=true&w=majority",
		"database": "workeranalyzer"
}

# Collection Param
collection = "sessions"

# Instância
db = MongoStorage(connection, collection)

# Connect
db.connect()
# return True

session = {
	"awesomekey", "lorem ipsum value"
}


# Save
db.save(session)
# Return True, ID: xxxxxx-xxxxxx-xxxxxxx
