
parameters = [
    "id",
    "node_id",
    "name",
    "full_name",
    "private",
    "fork",
    "created_at",
    "updated_at",
    "pushed_at",
    "size",
    "stargazers_count",
    "watchers_count",
    "language",
    "has_issues",
    "has_projects",
    "forks_count",
    "topics",
    "visibility",
    "forks",
    "open_issues",
    "default_branch",
    "permissions",
    "score"
    ]

def reduce_size_repository(original):
    new = dict()

    for parameter in parameters:
        new[parameter] = original[parameter]
    
    new["owner"] = original["owner"]["login"]

    return new

def reduce_repositories(original):
    new = []

    for repo in original:
        new.append(reduce_size_repository(repo))

    return new