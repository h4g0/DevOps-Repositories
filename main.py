import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from api import get_content_repositories, get_multiple_random_repositories, get_raw_file
from db import DB
from tools import find_repos_tools, get_all_random_repositories_dates, get_repos_data_dates, get_total_repos_per_tool
from transform_data import reduce_repositories
from multiprocessing import Pool

def pretty_json(item):
    print(json.dumps(item, indent=2))

def add_multiple_repositories_to_db(myDB,pages,stars=20):
    
    
    repositories = reduce_repositories(get_multiple_random_repositories(pages,stars))

    myDB.add_repositories(repositories)
        
    print(len(repositories))

def get_tool_usage_statistics(myDB):
    
    repos = myDB.get_repositories()

    print(len(repos))

    print(get_total_repos_per_tool(repos))

def process_repositories(myDB,count):
        
    repos = myDB.get_random_unprocessed_repositorioes(count)
    
    find_repos_tools(myDB,repos)

def test_time_per_repo(myDB,number_of_repos):
    start = time.time()

    process_repositories(myDB,number_of_repos)

    total_time = time.time() - start

    print(f"total time {total_time}: time per repo: {total_time / number_of_repos}")

def main():
    
    myDB = DB()

    time.sleep(5)
    ##get_raw_file("MPLew-is/github-api-client","main","Examples/GithubActionsWebhookClient/ReadMe.md")

    test_time_per_repo(myDB,1000)
    ##add_multiple_repositories_to_db(myDB,2,10)
    ##get_tool_usage_statistics(myDB)
    
    ##get_repos_data_dates(myDB,"08/04/10","23/10/15")

    """start = time.time()

    rr = get_repos_data_dates(myDB,"12/01/01","16/12/31",10)
    
    print( time.time() - start )"""
    
    """rr = [x["stargazers_count"]for x in get_all_random_repositories_dates("2023-10-08","2023-10-15")]

    print(rr)

    ur = set()

    for r in rr:
        ur.add(r)

    print(len(ur))"""

    """start = time.time()

    await process_repositories(myDB)

    print( time.time() - start )"""


main()