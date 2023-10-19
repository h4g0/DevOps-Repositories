import datetime
import requests 
import json
import time
import base64
import functools
import asyncio
from concurrent.futures import ThreadPoolExecutor

from re import search, IGNORECASE

from api import decoded_base_64, get_content_repositories, get_random_repositories_day, get_raw_file, get_repo_tree
from transform_data import reduce_repositories

sleep = 0
sleep_code = 1
workers = 200
workers_git = 32

Maven = "Maven"
Kubernetes = "Kubernetes"
GitHubActions = "GitHubActions"

repos_filename = [("Agola","\.agola"),
                  ("AppVeyor","appveyor\.yml"),
                  ("ArgoCD","argo\-cd"),
                  ("Bytebase","air\.toml"),
                ("Cartographer","cartographer\.yaml"),
                ("CircleCI","circleci"),
                ("Cloud 66 Skycap","cloud66"),
                ("Cloudbees Codeship","codeship-services\.yml"),
                ("Devtron","devtron-ci\.yaml"),
                ("Flipt","flipt\.yml"),
                ("GitLab","gitlab-ci\.yml"),
                ("Google Cloud Build","cloudbuild\.yaml"),
                ("Helmwave","helmwave\.yml"),
                ("Travis","\.travis\.yml"),
                ("Jenkins","Jenkinsfile"),
                ("JenkinsX","jx\-requirements\.yml"),
                ("JenkinsX","buildPack\/pipeline\.yml"),
                ("JenkinsX","jenkins\-x\.yml"),
                ("Keptn","charts\/keptn\/"),
                ("Liquibase","liquibase\.properties"),
                ("Mergify","mergify"),
                ("OctopusDeploy"," \.octopus"),
                ("OpenKruise","charts\/kruise\/"),
                ("OpsMx","charts\/isdargo\/"),
                ("Ortelius","component\.toml"),
                ("Screwdriver","screwdriver.yaml"),
                ("Semaphore","\.semaphore\/semaphore\.yaml"),
                ("TeamCity","\.teamcity"),
                ("werf","werf\.yaml"),
                ("Woodpecker CI", "\.woodpecker\.yml")]

repos_code_yml = [("Codefresh","DaemonSet"),
                ("Codefresh","StatefulSet"),
                 ("XL Deploy","apiVersion\: \(xl-deploy\|xl\)"),
                ("Drone","kind\:"),
                ("Flagger","flagger"),
                ("Harness.io","featureFlags\:"),
                ("Flux","fluxcd"),
                ("GoCD","stages\:"),
                ("Concourse","resources\:"),
                  ("Kubernetes","apiVersion\:"),
                  ("GitHubActions","jobs\:"),
                  ("AWS CodePipeline","roleArn"),
                   ]

def check_file_names(filestools,filename):
    
    for (tool,name) in filestools:
        if search(name,filename,IGNORECASE):
            return tool

    return None

def check_file_extension(toolsextensions,filename):

    for(tool,extension) in toolsextensions:
        if search(extension, filename,IGNORECASE):
            return tool
    
    return None

def check_file_contents(toolcontents,filecontents):

    for(tool,content) in toolcontents:
        if search(content,filecontents,IGNORECASE):
            return tool
        
    return None

def checkExtension(extension,filename):

    if search(extension,filename):
        return True

    return False

def checkExtensionTree(extension,tree):
    
    for f in tree:
        if checkExtension(extension,f["path"]):
            return True
        
    return False

def check_tools(reponame,repos_code,extension):
    
    tools = set()

    for t in repos_code:
        time.sleep(sleep_code)
        if len(get_content_repositories(t[1],reponame,extension)) > 0:
            tools.add(t[0])

    return tools


def check_tools_read_file(reponame,repos_code,tree,branch,extension):


    tools = set()


    ###with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    ###results = pool.map(tester, urls)~


    with ThreadPoolExecutor(max_workers=workers) as executor:

        tasks = []

        for f in tree:

            if checkExtension(extension,f["path"]):
                t = executor.submit(get_raw_file,reponame,branch,f["path"])
                tasks.append(t)

        for t in tasks:
            
            
            rawf = t.result()

            for r in repos_code:
                    
                    if check_file_contents([r] ,rawf):
                        tools.add(r[0])

    return tools

def count_extension(tree,extension):
    
    count = 0
    for f in tree:
        if checkExtension(extension,f["path"]):
            count += 1

    return count


def find_tools_inside_files(repo,tree):

    tools = set()

    yaml_c = count_extension(tree,'\.yaml') + count_extension(tree,'\.yml')
    package_json = count_extension(tree,'\.package.json')

    print(f"Count yaml: {yaml_c} package.json: {package_json}")
          
    if checkExtensionTree("\.yml",tree) or checkExtensionTree("\.yaml",tree):
        
        new_tools = check_tools_read_file(repo["full_name"],repos_code_yml,tree,repo["default_branch"],"\.yml")
        tools = tools.union(new_tools)

        new_tools = check_tools_read_file(repo["full_name"],repos_code_yml,tree,repo["default_branch"],"\.yaml")
        tools = tools.union(new_tools)

    return tools

def find_repos_tool(db,repo):

    ##start = time.time()

    tools = set()

    print(repo["name"])

    tree = get_repo_tree(repo["owner"],repo["name"],repo["default_branch"])["tree"]

    for f in tree:

        tool = check_file_names(repos_filename,f["path"])
            
        if tool != None:
               
            tools.add(tool)
   

    new_tools = find_tools_inside_files(repo,tree)

    tools = tools.union(new_tools)


    print(tools)

    ###db.add_tools(repo["name"],list(tools))

    ##print(tools)
    ##print(f"tool time {time.time() - start}")
    
    return tools

async def test():
    print("test")

def find_repos_tools(db,repos):

    def find_repos_tool_container(repo):
        
        try:
            tools = find_repos_tool(db,repo)

            return tools
        
        except:
            full_name = repo["full_name"]
            print(f"Error for repo {full_name}")

            return set()
        
    tools_in_repos = []

    futures = []

    with ThreadPoolExecutor(max_workers=workers_git) as executor:

        for repo in repos:
            f = executor.submit(find_repos_tool_container,repo)
            futures.append(f)
        
    for f in futures:

        tools = f.result()

        if(len(tools) > 0):
            tools_in_repos.append(tools)

       
    for tool in tools_in_repos:
        print(tool)

    print(len(tools_in_repos))

def get_total_repos_per_tool(repos):
    
    count = dict()

    for repo in repos:
        print(repo.get("name"))
        tools = repo.get("tools_used") or []


        for tool in tools:
            new_count =  count.get(tool,0) + 1
            count.update({tool: new_count})

    return count


def get_repository_names_from_db(myDB,number):

    repos = myDB.get_repositories()

    repo_names = [x["full name"] for x in repos]

    return repo_names[:number]

def get_all_random_repositories_dates(start,end,stars):

    repos = []
    names = set()

    def add_new_repos(new_repos):

        for r in new_repos:
            if not (r["full_name"] in names):
                repos.append(r)
                names.add(r["full_name"])
    
    new_repos = get_random_repositories_day(start,end,0)

    add_new_repos(new_repos)
    
    page = 1
    
    while(len(new_repos) > 0):
        new_repos = get_random_repositories_day(start,end,page)
        
        if(len(new_repos) > 0 and new_repos[0]["stargazers_count"] < stars):
            return repos
        
        add_new_repos(new_repos)

        page += 1

    return repos

def get_repos_data_dates(myDB,start,finish,stars):

    curr_date = finish
    datetime_curr_date = datetime.datetime.strptime(curr_date, "%y/%m/%d")
    datetine_start = datetime.datetime.strptime(start, "%y/%m/%d")

    while(datetime_curr_date > datetine_start):
        
        end_date = datetime_curr_date.strftime('%Y-%m-%d')

        datetime_curr_date = datetime_curr_date - datetime.timedelta(days=7)

        start_date_obj = ( datetime_curr_date + datetime.timedelta(days=1) )
        start_date =  start_date_obj.strftime('%Y-%m-%d')

        if(start_date_obj < datetine_start):
            start_date =  datetine_start.strftime('%Y-%m-%d')

        print(f"----{start_date}----{end_date}\n")

  
        rr = list(filter(lambda x: x["stargazers_count"] >= stars,get_all_random_repositories_dates(start_date,end_date,stars)))

        print(len(rr))

        myDB.add_repositories(reduce_repositories(rr))