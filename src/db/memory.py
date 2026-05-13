import os
import datetime
import pymongo
from dotenv import load_dotenv

load_dotenv()
class Mongomemory:
    def __init__(self):

        client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        self.collection = client["eduhub"]["conversations"]

    def save_conversation(self, user_id, question, input_type, parsed, routed, solved, verified):
        document = {
            "user_id": user_id,
            "question": question,
            "input_type": input_type,
            "parsed_result": parsed,
            "router_result": routed,
            "solver_result": solved,
            "verifier_result": verified,
            "timestamp": datetime.datetime.utcnow()

        }
        self.collection.insert_one(document)

    def get_history(self,user_id,limit=10):
        results = self.collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        return list(results)


