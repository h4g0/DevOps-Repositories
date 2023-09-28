from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from keys import uri


class DB:
    # Send a ping to confirm a successful connection

    def __init__(self):
        
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def add_repositories(self,respoitories):
        mycol = self.client.Repositories["random"]

        mycol.insert_many(respoitories)

    def get_repositories(self):
        mycol = self.client.Repositories["random"]

        return list(mycol.find({}))
