import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from api import change_token, get_content_repositories, get_multiple_random_repositories, get_rate_limit, get_raw_file
from db import DB
from stats import get_cicd_percent_per_year, get_language_number_of_tools_distribution, get_languages_cicd, get_languages_cicd_morethanone, get_languages_more_than_one_percent, get_map_tool_tool, get_number_of_tools_distribution, get_number_tools_per_year, get_programming_languages, get_programming_languages_all, get_programming_languages_repos, get_programming_languages_repos_normalized, get_stats_repos_per_tool, get_tools_language_cicd, get_tools_more_than_one_percent, migrations_programming_language, migrations_programming_languages_to_from, migrations_tools, migrations_tools_time_to_fall, migrations_travis, percentage_tools_2019_2023
from tools import find_repos_tools, get_all_random_repositories_dates, get_repos_data_dates, get_total_repos_per_tool
from transform_data import reduce_repositories
from multiprocessing import Pool
from keys import key
from run_all_stats import run_all_stats_and_save

import csv
import argparse



def pretty_json(item):
    print(json.dumps(item, indent=2))

def add_multiple_repositories_to_db(myDB,pages,stars=20):
    
    
    repositories = reduce_repositories(get_multiple_random_repositories(pages,stars))

    myDB.add_repositories(repositories)
        
    print(len(repositories))

def get_tool_usage_statistics(myDB):
    
    repos = myDB.get_processed_repositories()

    print(len(repos))

    print(get_total_repos_per_tool(repos))

def process_repositories(myDB):
        
    #repos = myDB.get_random_unprocessed_repositorioes(count)
    repos = myDB.get_repositories()

    find_repos_tools(myDB,repos)

def test_time_per_repo(myDB,number_of_repos):
    start = time.time()

    process_repositories(myDB,number_of_repos)

    total_time = time.time() - start

    print(f"total time {total_time}: time per repo: {total_time / number_of_repos}")

def process_repos_keys(myDB,count):
    
    onehour = (60 * 60)

    keys = [key]

    timeperkey = int(onehour / len(keys))

    print(timeperkey / 60)
    
    for k in keys:

        change_token(k)

        start = time.time()

        process_repositories(myDB,count)
        
        times = int(time.time() - start)
        
        sleeping_time = timeperkey - times

        if sleeping_time < 0:
            continue

        print(f"sleeping for {sleeping_time} seconds")

        time.sleep(sleeping_time)

def get_language_repos(repos,language):

    data2 = repos
    data2 = list(filter(lambda x: len(x['tools_used']) > 0, data2))
    data2 = list(filter(lambda x:  x["language"] ==  language, data2))

    exists = dict()

    for x in data2:
        exists.update({x["full_name"]: True})    

    return exists

def get_language_used_repos(repos):

    data2 = repos
    data2 = list(filter(lambda x: len(x['tools_used']) > 0, data2))

    language = dict()

    for x in data2:
        language.update({x["full_name"]: x["language"]})    


    return language

def get_project_owners():
    f = open('enterprise_projects.txt', "r", encoding="utf8")
    tsv_reader = csv.DictReader(f, delimiter="\t")


    d = dict()

    for t in tsv_reader:
        owner = t.get("aligent")
        d.update({owner: True})

    return d

def save_entreprise_repos():
    owners = get_project_owners()

    f = open('Repositories.random-processed.json',encoding="utf8")
    data = json.load(f)
    print(len(data))
    print(data[0])
    
    ##cicd_projects = filter(lambda x: len(x.get("tools_used")) > 0,data)
    entreprise_projects = list(filter(lambda x: owners.get(x.get("owner"), False),data))
    print(len(list(entreprise_projects)))

    with open('data.json', 'w') as f:
        json.dump(entreprise_projects, f)

def get_repos_entreprise():
    f = open('Repositories.entreprise_repos.json',encoding="utf8")
    data = json.load(f)

    d = dict()

    for repo in data:
        d.update({repo["full_name"]: True})

    return d

def save_repos_entreprise_history():
    repos_dict = get_repos_entreprise()
    f = open('Repositories.repo_tools_history.json',encoding="utf8")
    

    data2 = json.load(f)
    
    data2 = list(filter(lambda x: repos_dict.get(x["repo_full_name"],False), data2))
    	
    print(len(data2))
    
    with open('data.json', 'w') as f:
        json.dump(data2, f)

def top_enter(data):
    enterprises = dict()
    for proj in data:
        enter = proj["owner"]
        enter_C = enterprises.get(enter,0) + 1
        enterprises.update({enter: enter_C})
    
    enterprises = sorted(list(enterprises.items()),key=lambda x: x[1],reverse=True)

    return enterprises

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for repository management.")

    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subcommand for getting random repositories
    get_random_parser = subparsers.add_parser('get_repositories', help='Get random repositories')
    get_random_parser.add_argument('start', type=str, help='Start date')
    get_random_parser.add_argument('end', type=str, help='End date')
    get_random_parser.add_argument('stars', type=int, help='Minimum stars')

    # Subcommand for processing repositories
    process_parser = subparsers.add_parser('process', help='Process repositories')

    # Subcommand for running stats and saving
    stats_parser = subparsers.add_parser('run_stats', help='Run statistics and save results')
    stats_parser.add_argument('dataset', type=str, help='Dataset name')
    stats_parser.add_argument('stats_folder', type=str, help='Folder to save statistics')

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == 'get_repositories':
        myDB = DB()
        get_repos_data_dates(myDB,args.start, args.end, args.stars)
    elif args.command == 'process':
        myDB = DB()
        process_repositories(myDB)
    elif args.command == 'run_stats':
        f = open(args.dataset,encoding="utf8")
        data = json.load(f)

        run_all_stats_and_save(data, args.stats_folder)

main()