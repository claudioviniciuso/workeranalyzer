from worker_analyzer.storage import MongoStorage

# Connection Dict
connection = {
		"url": "mongodb+srv://testing:q1w2e3r4@localhost:27017/workeranalyzer?retryWrites=true&w=majority",
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
	"somekey": "lorem ipsum value"
}


# Save
print(db.save(session))
# Return True, ID: xxxxxx-xxxxxx-xxxxxxx
