import random

from pymongo import MongoClient

from .config import MONGO_URL

class DB:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.interviewCoachDB

    def get_categories(self):
        return list(self.db.categories.find())
    
    def get_questions(self, category, limit):
        questions = list(self.db.questions.aggregate([
            {
                "$lookup": {
                    "from": "categories",
                    "localField": "categoryId",
                    "foreignField": "_id",
                    "as": "category"
                }
            }, {
                "$unwind": "$category"
            }, {
                "$match": {
                    "category.category": category
                }
            }, {
                "$project": {
                    "question": 1,
                    "categoryId": 1,
                    "category": "$category.category"
                }
            }
        ]))

        # Randomly select {limit} records 
        # Not using Mongo's "sample" operation because it could potentially return duplicate objects
        return random.choices(questions, k = limit)
