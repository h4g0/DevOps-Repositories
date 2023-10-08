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
    print((result.json()))
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

def get_files_repository(owner,repo):
    result = extract_repository(f"https://api.github.com/search/repos/{owner}/{repo}/contents")
    
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


def decoded_base_64(fileloc):
    result = extract_repository(fileloc)
    data = json.loads(result.content)

    decoded_content = base64.b64decode(data["content"])

    return f"{decoded_content}"

def get_repo_tree(owner,repo,branch):

    result = extract_repository(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")

    return result.json()

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

def find_repos_tools(db,repos,repos_filename, repos_code):

    for repo in repos:
        
        
        tools = set()

        print(repo["name"])
        tree = get_repo_tree(repo["owner"]["login"],repo["name"],repo["default_branch"])["tree"]

        for f in tree:

            tool = check_file_names(repos_filename,f["path"])
            
            if tool != None:
            
                if tool != None : tools.add(tool)
            
                if tool == Maven:
                    
                    contents = decoded_base_64(f["url"])
                    tool = check_file_contents(repos_code,contents)
            
                    if tool != None:
                        
                        tools.add(tool)

            if tool != None:
                tools.add(tool)
        
        print(tools)

        """for tool in tools:
            db.add_too_repo(tool,repo.name)
        
        db.mark_as_processed(repo.name)"""

        time.sleep(2)
    

def get_total_repos_per_tool(repos):
    
    count = dict()

    for repo in repos:
        tools = repo["tools"]

        for tool in tools:
            count.update(tool, (count.get(tool) | 0) + 1)

    return count
 
def main():
    
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
    myDB = DB()
        
    time.sleep(5)

    repos = myDB.get_unprocessed_repositories()

    print(len(repos[0:100]))

    find_repos_tools(myDB,repos[100:400],repos_filename,repos_code)

    """print(check_file_extension(repos_extension,"test"))
    print(check_file_extension(repos_extension,"test.io"))
    print(check_file_extension(repos_extension,"test.io"))
    print(check_file_extension(repos_extension,".ioaaas"))"""

    """print(check_file_names(repos_filename,"test"))
    print(check_file_names(repos_filename,"Prometheus.yml"))
    print(check_file_names(repos_filename,"test"))
    print(check_file_names(repos_filename,"pom.xml"))
    print(check_file_names(repos_filename,"test"))
    print(check_file_names(repos_filename,"test"))
    print(check_file_names(repos_filename,"test"))
    print(check_file_names(repos_filename,"Dockerfile"))
    print(check_file_names(repos_filename,"Kube_config_rancher-cluster.yml"))"""


    content = decoded_base_64("https://api.github.com/repos/vuejs/vue/git/blobs/bca41a4940526c0c04688f2db60ca052c34dde29")

    """print(check_file_contents(repos_code,content))
    print(check_file_contents(repos_code,"org.junit.runner.JUnitCore"))
    print(check_file_contents(repos_code,"org.junit.runner.jUnitCore"))"""

    ##decoded_base_64("https://api.github.com/repos/vuejs/vue/git/blobs/bca41a4940526c0c04688f2db60ca052c34dde29")
    ##add_multiple_repositories_to_db(myDB,5)

    ##print(myDB.get_repositories())
    ##get_repo_tree("vuejs","vue")
    ##get_filename_repositories("Docker",0)
    ##pretty_json(extract_docker().json())
    ##total_repositories_tool("Docker")
    ##pretty_json(extract_repository("https://api.github.com").json())
    ##print(extract_repository("https://api.github.com/rate_limit").json())

main()

