import requests 
import json

key = "git: https://github.com/ on DESKTOP-F58GI75 at 29-Oct-2019 21:46"

def extract_repository(url):
    result = requests.get(url, {"Authorization": f"Bearer {key}"})
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

def extract_maven():
    return extract_repository("https://api.github.com/search/repositories?q=maven+language:xml&per_page=2&sort=stars&order=desc")

def extract_gradle():
    return extract_repository("https://api.github.com/search/repositories?q=language:Gradle&per_page=2&sort=stars&order=desc")

def pretty_json(item):
    print(json.dumps(item, indent=2))

def main():
    pretty_json(extract_gradle().json()['items'])


main()