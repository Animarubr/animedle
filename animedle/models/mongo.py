from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Mongo():
    
    def __init__(self) -> None:
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.database = self.client.get_database("animedle")
    
    