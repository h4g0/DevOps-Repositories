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
    
    def get_unprocessed_repositories(self):
        mycol = self.client.Repositories["random"]
        
        return list(mycol.find({ "$or": [{"processtools": None} , {"processtools": False}]}))
    
    def add_tool_repo(self,tool,repo):
        mycol = self.client.Repositories[tool]

        mycol.insert_one(repo)

    def get_repository(self, name):
        mycol = self.client.Repositories["random"]

        repos = list(mycol.find({"name": {name}}))

        if (len(repos) > 0): return repos[0]

        return None

    def mark_as_processed(self,name):
        mycol = self.client.Repositories["random"]

        mycol.update_many({"name": {name}, "processtools": True})

    def add_tools(self,name,tools):
        mycol = self.client.Repositories["random"]

        mycol.update_many({"name": {name}}, {"tools_used": tools,"processtools": True})
