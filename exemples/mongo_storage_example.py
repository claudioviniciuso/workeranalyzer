from worker_analyzer.storage import MongoStorage

# Connection Dict
connection = {
		"url": "mongodb+srv://username:pwd@host/?retryWrites=true&w=majority",
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
	"key", "value"
}


# Save
db.save(session)
# Return True, ID: xxxxxx-xxxxxx-xxxxxxx
