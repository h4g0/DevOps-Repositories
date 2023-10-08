import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from api import get_multiple_random_repositories
from db import DB
from tools import find_repos_tools, get_total_repos_per_tool


def pretty_json(item):
    print(json.dumps(item, indent=2))

def add_multiple_repositories_to_db(myDB,pages,stars=20):
    
    repositories = get_multiple_random_repositories(pages,stars)

    myDB.add_repositories(repositories)
        
    print(len(repositories))

def get_tool_usage_statistics(myDB):
    
    repos = myDB.get_repositories()

    print(len(repos))

    print(get_total_repos_per_tool(repos))

def process_repositories(myDB):
    
    repos = myDB.get_unprocessed_repositories()
  
    find_repos_tools(myDB,repos[0:50])

def main():
    
    myDB = DB()

    time.sleep(5)

    add_multiple_repositories_to_db(myDB,20,10)
main()

