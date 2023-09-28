import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from keys import key
from db import DB

def extract_repository(url):
    
    headers = {'Authorization': f'token {key}'}

    result = requests.request("GET", url, headers=headers)

    return result


def extract_repositories():
    final_result = []

    result = extract_repository()

    while( result.len > 0):
        final_result.push(result)
        result = extract_repository() 

    return final_result

def extract_tool_content():
    return extract_repositories()

def extract_tool_extension():
    return extract_repositories()


def extract_docker():
    return extract_repository("https://api.github.com/search/repositories?q=docker+stars:>=10&per_page=2&sort=stars&order=desc")

def extract_tool_repository(tool, stars, page):
    result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:>={stars}&page={page}&per_page=2&sort=stars&order=desc")
    print(pretty_json(result.json()))
    return result.json()

def total_repositories_tool(tool):
    result = extract_repository(f"https://api.github.com/search/repositories?q={tool}&page=1&per_page=2&sort=stars&order=desc")

    return result.json()["total_count"]
    
def extract_tool_repository_size(tool, stars, page,min,max):
    result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:{min}..{max}+stars:>={stars}&page={page}&sort=stars&order=desc")
    print(p(result.json()))
    return result.json()


def get_random_repositories(stars = 20,page=0):
    result = extract_repository(f"https://api.github.com/search/repositories?q=stars:>={stars}&per_page=100&page={page}&order=desc")

    print(len(result.json()["items"]))
    ##print(pretty_json(result.json()))
    
    return result.json()["items"]

def get_multiple_random_repositories(pages, stars=20):
    repositories = []

    for i in range(0,pages):
        time.sleep(15)
        repositories.extend(get_random_repositories(stars, i))


    return repositories 

def get_filename_repositories(filename,repo,stars = 20):
    result = extract_repository(f"https://api.github.com/search/code?q=filename={filename}&repo={repo}&stars:>={stars}&per_page=100&order=desc")
    
    print(result.json())
    print(len(result.json()["items"]))
    ##print(pretty_json(result.json()))
    
    return result.json()

def get_content_repositories(contemt,repo,stars = 20):
    result = extract_repository(f"https://api.github.com/search/code?q=content={content}&repo={repo}&stars:>={stars}&per_page=100&order=desc")
    
    print(result.json())
    print(len(result.json()["items"]))
    ##print(pretty_json(result.json()))
    
    return result.json()
   
def extract_tool(tool,stars):
    page = 0
    items  = []

    result = extract_tool_repository(tool,stars,page)

    curr_items = result["items"]

    items.extend(curr_items)

    while(len(curr_items) != 0):
        time.sleep(15)
        page += 1
        result = extract_tool_repository(tool,stars,page)
        pretty_json(result)
        ##print(result)
        curr_items = result["items"]
        
        items.extend(curr_items)
        print(len(curr_items))
    
    return items

def pretty_json(item):
    print(json.dumps(item, indent=2))

def add_multiple_repositories_to_db(myDB,pages,stars=20):
    
    repositories = get_multiple_random_repositories(5)

    myDB.add_repositories(repositories)
        
    print(len(repositories))

def get_repository_names_from_db(myDB,number):

    repos = myDB.get_repositories()

    repo_names = [x["full name"] for x in repos]

    return repo_names[:number]

def main():
    
    repos_filename = [("Travis",".travis.yml"),
                        ("Gradle","Build.gradle"),
                        ("Rake","Rakefile"),
                        ("Jenkins","Jenkinsfile"),
                        ("Rancher","Kube_config_rancher-cluster.yml"),
                        ("Docker","Dockerfile"),
                        ("Progress Cheff","Metadata.rb"),
                        ("Puppet","Site.pp"),
                        ("Nagios","Nagios.cfg"),
                        ("Prometheus","Prometheus.yml")]
    
    repos_code = [("Maven","/maven.apache.org"),
                    ("JUnit","import org.junit.runner.JUnitCore"),
                    ("Selenium","<groupId>org.seleniumhq.selenium</groupId>"),
                    ("Mesos","<groupId>org.apache.mesos</groupId>")]
    myDB = DB()
        
    time.sleep(15)

    print(get_repository_names_from_db(myDB,10))
    ##add_multiple_repositories_to_db(myDB,5)

    ##print(myDB.get_repositories())
    
    ##get_filename_repositories("Docker",0)
    ##pretty_json(extract_docker().json())
    ##total_repositories_tool("Docker")
    ##pretty_json(extract_repository("https://api.github.com").json())
    ##print(extract_repository("https://api.github.com/rate_limit").json())

main()

