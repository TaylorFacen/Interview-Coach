from pymongo import MongoClient

from .config import MONGO_URL

class DB:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.interviewCoachDB

    def get_categories(self):
        db = self.db
        return list(db.categories.find())
