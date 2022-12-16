import requests 
import json
import time
from requests.structures import CaseInsensitiveDict

##key = "2959d348671d85a18f55a226831cd1883017dade"
key = "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"

def extract_repository(url):
    headers = CaseInsensitiveDict()
    
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {key}"

    result = requests.get(url, headers)

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

def extract_maven2():
    return extract_repository("https://api.github.com/search/topics?q=maven&per_page=2&sort=stars&order=desc")

def extract_maven():
    return extract_repository("https://api.github.com/search/repositories?q=maven+stars:>=10&per_page=2&sort=stars&order=desc")

def extract_gradle():
    return extract_repository("https://api.github.com/search/repositories?q=language:Gradle&per_page=2&sort=stars&order=desc")

def extract_travis():
    return extract_repository("https://api.github.com/search/repositories?q=language:Gradle&per_page=2&sort=stars&order=desc")


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
    result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:{min}..{max}+stars:>={stars}&page={page}&per_page=2&sort=stars&order=desc")
    print(pretty_json(result.json()))
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

def tools_repositories(tools):
    for tool in tools:
        time.sleep(20)
        print(total_repositories_tool(tool))


def tools_repositories_stars(tools):
    print("0 to 10")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:0..10&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("10 to 50")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:10..50&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("50 to 100")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:50..100&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("100 to 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:100..1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("more than 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+stars:>=1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

def tools_repositories_followers(tools):
    print("0 to 10")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+followers:0..10&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("10 to 50")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+followers:10..50&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("50 to 100")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+followers:50..100&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("100 to 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+followers:100..1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("more than 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+followers:>=1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)


def tools_repositories_forks(tools):
    print("0 to 10")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+forks:0..10&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("10 to 50")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+forks:10..50&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)


    print("50 to 100")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+forks:50..100&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("100 to 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+forks:100..1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("more than 1000")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+forks:>=1000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)


def tools_repositories_type(tools):
    print("public")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+is:public&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("private")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+is:private&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)
     
def tools_repositories_archived(tools):
    print("true")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+archived:true&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("false")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+archived:false&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)


def tools_repositories_size(tools):
    print("less than 100 MB")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:<=100000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("100 MB to 1 GB")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:100000..1000000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    print("1 GB to 10 GB")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:1000000..10000000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

    
    print("more than 10 GB")
    for tool in tools:
        result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+size:>=10000000&page=1&per_page=2&sort=stars&order=desc")
        print(result.json()["total_count"])
        time.sleep(20)

def tools_per_year(tools):
    start = 2010
    end = 2023

    for year in range(start,end):
        print(year)
        
        for tool in tools:
            result = extract_repository(f"https://api.github.com/search/repositories?q={tool}+created:{year}-01-01..{year}-12-31&page=1&per_page=2&sort=stars&order=desc")
            print(result.json()["total_count"])
            time.sleep(20)

def main():
    
    tools = ["Travis","Flyway","Maven","Gradle","Rake","Jenkins",
    "Open Stack","Rancher","Docker","Ansible",
    "Terraform","Octopus Deploy","Bamboo","JUnit","Selenium","Progress Chef",
    "Puppet","Nagios","Zabbix","Prometheus","Logstash","Graylog","Kubernetes",
    "Mesos"
    ]
    
    tools_repositories_forks(tools)
    
    ##pretty_json(extract_docker().json())
    ##total_repositories_tool("Docker")
    ##pretty_json(extract_repository("https://api.github.com").json())
    ##print(extract_repository("https://api.github.com/rate_limit").json())

main()

