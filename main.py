import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from api import get_multiple_random_repositories
from db import DB
from tools import find_repos_tools


def pretty_json(item):
    print(json.dumps(item, indent=2))

def add_multiple_repositories_to_db(myDB,pages,stars=20):
    
    repositories = get_multiple_random_repositories(5)

    myDB.add_repositories(repositories)
        
    print(len(repositories))
 
def main():
    
    myDB = DB()

    repos = myDB.get_unprocessed_repositories()

    print(len(repos[0:100]))

    find_repos_tools(myDB,repos[0:100])

  

main()
