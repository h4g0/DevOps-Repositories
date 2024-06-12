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
from keys import key,keyhugo2,keyhugo3,keyjacome
import csv

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

def process_repositories(myDB,count):
        
    repos = myDB.get_random_unprocessed_repositorioes(count)
    
    find_repos_tools(myDB,repos)

def test_time_per_repo(myDB,number_of_repos):
    start = time.time()

    process_repositories(myDB,number_of_repos)

    total_time = time.time() - start

    print(f"total time {total_time}: time per repo: {total_time / number_of_repos}")

def process_repos_keys(myDB,count):
    
    onehour = (60 * 60)

    keys = [key,keyhugo2,keyhugo3,keyjacome]

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
    
    cicd_projects = filter(lambda x: len(x.get("tools_used")) > 0,data)
    entreprise_projects = list(filter(lambda x: owners.get(x.get("owner"), False),cicd_projects))
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
        
def main():
    
    ##myDB = DB()

    ##get_raw_file("MPLew-is/github-api-client","main","Examples/GithubActionsWebhookClient/ReadMe.md")
    ##get_tool_usage_statistics(myDB)

   

    ##repos = myDB.get_random_processed_repositories(10000)

    ##repos = myDB.get_processed_repositories_with_tools()

    ##print(get_map_tool_tool(repos))


    """repos_filename = [("Agola","\.agola"),
                    ("AppVeyor","appveyor\.yml"),
                    ("ArgoCD","argo\-cd"),
                    ("Bytebase","air\.toml"),
                    ("Cartographer","cartographer\.yaml"),
                    ("CircleCI","circleci"),
                    ("Cloud 66 Skycap","cloud66"),
                    ("Cloudbees Codeship","codeship\-services\.yml"),
                    ("Devtron","devtron\-ci\.yaml"),
                    ("Flipt","flipt\.yml"),
                    ("GitLab","gitlab\-ci\.yml"),
                    ("Google Cloud Build","cloudbuild\.yaml"),
                    ("Helmwave","helmwave\.yml"),
                    ("Travis","\.travis\.yml"),
                    ("Jenkins","Jenkinsfile"),
                    ("JenkinsX","jx\-requirements\.yml"),
                    ("Keptn","charts\/keptn\/"),
                    ("Liquibase","liquibase\.properties"),
                    ("Mergify","mergify"),
                    ("OctopusDeploy"," \.octopus"),
                    ("OpenKruise","charts\/kruise\/"),
                    ("OpsMx","charts\/isdargo\/"),
                    ("Ortelius","component\.toml"),
                    ("Screwdriver","screwdriver\.yaml"),
                    ("Semaphore","\.semaphore\/semaphore\.yaml"),
                    ("TeamCity","\.teamcity"),
                    ("werf","werf\.yaml"),
                    ("Woodpecker CI", "\.woodpecker\.yml"),
                    ("GitHubActions","github\/workflows")]

    repos_code_yml = [("Codefresh","DaemonSet"),
                    ("XL Deploy","apiVersion\: \(xl-deploy\|xl\)"),
                    ("Drone","kind\:"),
                    ("Flagger","flagger"),
                    ("Harness.io","featureFlags\:"),
                    ("Flux","fluxcd"),
                    ("GoCD","stages\:"),
                    ("Concourse","resources\:"),
                    ("Kubernetes","apiVersion\:"),
                    ("AWS CodePipeline","roleArn"),
                    ]


    repos = []

    repos.extend(repos_filename)
    repos.extend(repos_code_yml)

    print(len(repos))

    for i in range(0,len(repos),2):
        print(f"{repos[i][0]} & {repos[i+1][0]}\\\\")
        print("\hline")"""

    

    ##print(list(tsv_reader)[1].get("aligent"))
    ##languages = get_language_used_repos(data2)

    ##migrations_tools_time_to_fall(data) 

    ##print(len(data2))

    ##migrations_programming_language(data, languages)
    ##data = list(filter(lambda x: exists.get(x["repo_full_name"], False), data))
    
    ##migrations_travis(data)
    ##print(len(data))

    ##tools_one_percent = [x[0] for x in get_languages_more_than_one_percent(data)]

    ##print(tools_one_percent)
    ##migrations_tools(data)
    ##print(data[0])

    ##percentage_tools_2019_2023(data)
    
    """count = 0
    count_ci = 0

    for repo in data:
        tools = repo.get("tools_used",[])

        if len(tools) > 0:
            count_ci+= 1

        #if ("CircleCI" in tools) or ("GitHubActions" in tools) or ("Travis" in tools) or ("Jenkins" in tools) or ("GitLab" in tools):  
        if ("Travis" in tools) or ("GitHubActions" in tools):
            count += 1
    
    print(count)
    print(count/len(data))
    print(count/count_ci)"""
    

  

   
    """data = list(filter(lambda x: len(x["tools_used"]) > 0, data))
    print(get_language_number_of_tools_distribution(data))"""

    ##print(get_stats_repos_per_tool(repos))    
    ##get_rate_limit()
    ##process_repos_keys(myDB,20)
    """while True:
        process_repos_keys(myDB,5000)"""
    ##test_time_per_repo(myDB,1000)

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