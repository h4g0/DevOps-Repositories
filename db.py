import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateMany

from keys import uri


def add_tools_once(name,tools,tree):
        
        client = MongoClient(uri, server_api=ServerApi('1'))

        mycol = client.Repositories["random"]

        mycol.update_many({"full_name": name}, {"$set": {"tree": tree,"tools_used": tools, "processtools": True }})

class DB:
    # Send a ping to confirm a successful connection

    def __init__(self):
        
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def reset_connetion(self):
        
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


    def get_processed_repositories(self):
        mycol = self.client.Repositories["random"]
        
        return list(mycol.find({ "processtools": True}))

    def get_processed_repositories_with_tools(self):
        mycol = self.client.Repositories["random"]
        
        return list(mycol.find({ "processtools": True, "tools_used": { "$not": {"$size": 0} }}))
    
    def get_random_processed_repositories(self,size):
        mycol = self.client.Repositories["random"]

        match = { "$match":  {"processtools": True}}
        sample = {"$sample": {"size": size}} 

        return list(mycol.aggregate([ match, sample]))
    
    def get_random_unprocessed_repositorioes(self,size):
        mycol = self.client.Repositories["random"]

        qor =  {"$or": [{"processtools": None} , {"processtools": False}]}
        match = { "$match":  qor}
        sample = {"$sample": {"size": size}} 

        return list(mycol.aggregate([ match, sample]))
    
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

        mycol.update_many({"full_name": name}, {"$set": {"processtools": True}})

    def add_tools(self,name,tools,tree):
        mycol = self.client.Repositories["random"]

        mycol.update_many({"full_name": name}, {"$set": {"tree": tree,"tools_used": tools, "processtools": True }})

    def add_tools_many(self,repos):
        
        bulkreqs = []

        for repo in repos:

            name,tools,tree = repo
            bulkreqs.append(UpdateMany({"_id": name}, {"$set": {"tree": tree,"tools_used": tools, "processtools": True }}))

        
        mycol = self.client.Repositories["random"]

        mycol.bulk_write(bulkreqs)

    def mark_as_unprocessed(self):
        mycol = self.client.Repositories["random"]

        mycol.update_many({}, {"$set": {"tools_used": [], "processtools": False }})