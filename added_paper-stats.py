def main():
    
    f = open('Repositories.entreprise_tools_history.json',encoding="utf8")
    ##f = open('Repositories.entreprise_repos.json',encoding="utf8")
    #f = open('Repositories.repo_tools_history.json',encoding="utf8")
    #f = open('Repositories.entreprise_tools_history.json',encoding="utf8")


    data2 = json.load(f)

    print(len(data2))

    def all_equal(lst):
        diff = []
        for i in range(1,len(lst)):
            if lst[i] != lst[i-1]:
                diff.append(lst[i])

        return diff
                
    def get_year_from_date(date_dict):
        # Extract the date string directly from the dictionary
        date_string = date_dict['$date']
        
        # The year is the first 4 characters of the date string
        year = date_string[:4]
        
        return int(year)


    def has_tools_before(snapshots):
        for s in snapshots:
            year = get_year_from_date(s.get("date"))

            if year <= 2020:
                tools = list(filter(lambda x: x != "GitHubActions", s.get("tools", [])))

                if len(tools) > 0:
                    return True
        return False
                
    def tool_migrations(snapshots):
        flat_tools = [tool for s in snapshots for tool in s.get("tools", [])]

        return ("GitHubActions" in  flat_tools)

    print(data2[0])
    
    has_github_actions = list(filter(lambda x: tool_migrations(x.get('snapshots')) ,data2))

    print(len(has_github_actions))

    has_tool_before_git = list(filter(lambda x: has_tools_before(x.get("snapshots")), has_github_actions))

    print(len(has_tool_before_git))