from pymongo import MongoClient

MONGO_URI = "mongodb://mongo:27017/"
client = MongoClient(MONGO_URI)
db = client.messages
