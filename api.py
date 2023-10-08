import requests 
import json
import time
from requests.structures import CaseInsensitiveDict
from keys import key
from db import DB
import base64
from re import search, IGNORECASE

Maven = "Maven"
Kubernetes = "Kubernetes"

sleep = 2

def extract_repository(url):
    
    headers = {'Authorization': f'token {key}'}

    result = requests.request("GET", url, headers=headers)

    return result

def get_random_repositories(stars = 20,page=0):
    result = extract_repository(f"https://api.github.com/search/repositories?q=stars:>={stars}&per_page=100&page={page}&order=desc")

    print(len(result.json()["items"]))
    ##print(pretty_json(result.json()))
    
    return result.json()["items"]

def get_multiple_random_repositories(pages, stars=20):
    repositories = []

    for i in range(0,pages):
        time.sleep(sleep)
        repositories.extend(get_random_repositories(stars, i))


    return repositories 

def pretty_json(item):
    print(json.dumps(item, indent=2))


def decoded_base_64(fileloc):
    result = extract_repository(fileloc)
    data = json.loads(result.content)

    decoded_content = base64.b64decode(data["content"])

    return f"{decoded_content}"

def get_repo_tree(owner,repo,branch):

    result = extract_repository(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")

    return result.json()
