from github import Github

g = Github()
repo = g.search_repositories("Connection-Software-Browser")

def print_repo(repo):
    print(list(repo)[0])

print_repo(repo)