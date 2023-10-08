import requests 
import json
import time
import base64
from re import search, IGNORECASE

from api import decoded_base_64, get_repo_tree

sleep = 2

Maven = "Maven"
Kubernetes = "Kubernetes"

repos_filename = [("Travis","\.travis\.yml"),
                        ("Gradle","Build\.gradle"),
                        ("Rake","Rakefile"),
                        ("Jenkins","Jenkinsfile"),
                        ("Rancher","Kube_config_rancher-cluster\.yml"),
                        ("Docker","Dockerfile"),
                        ("Progress Cheff","Metadata\.rb"),
                        ("Puppet","Site\.pp"),
                        ("Nagios","Nagios\.cfg"),
                        ("Prometheus","Prometheus\.yml"),
                        ("Maven","pom\.xml"),
                        ("CircleCI","circleci"),
                        ('Kubernetes',"deployment\.yml"),
                        ('Kubernetes',"service\.yml")]
    
repos_code = [("JUnit","org\.junit\.runner\.JUnitCore"),
                    ("Selenium","org\.seleniumhq\.selenium"),
                    ("Mesos","org\.apache.mesos")]

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



def find_repos_tools(db,repos,max_file_calls=10):

    for repo in repos:
        
        
        tools = set()

        count_file_calls = 0

        print(repo["name"])
        tree = get_repo_tree(repo["owner"]["login"],repo["name"],repo["default_branch"])["tree"]

        for f in tree:

            tool = check_file_names(repos_filename,f["path"])
            
            if tool != None:
            
               
                tools.add(tool)
            
                if (tool == Maven) and (count_file_calls < max_file_calls):
                    
                    count_file_calls += 1

                    print(f["path"])
                    contents = decoded_base_64(f["url"])
                    tool = check_file_contents(repos_code,contents)
            
                    if tool != None:
                        
                        tools.add(tool)

        print(tools)

        db.add_tools(f["name"],list(tools))

        time.sleep(sleep)

def get_total_repos_per_tool(repos):
    
    count = dict()

    for repo in repos:
        tools = repo["tools"]

        for tool in tools:
            count.update(tool, (count.get(tool) | 0) + 1)

    return count


def get_repository_names_from_db(myDB,number):

    repos = myDB.get_repositories()

    repo_names = [x["full name"] for x in repos]

    return repo_names[:number]