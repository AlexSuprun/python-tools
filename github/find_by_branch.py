import os
import sys
from github import Github, GithubException

def search_repos_by_branch(organization_name, branch_name):
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)

    organization = g.get_organization(organization_name)
    repositories = organization.get_repos()

    result = [] 

    for index, repo in enumerate(repositories):
        if index % 10==0:
            print(f"Processing repo {index+1} of {repositories.totalCount}")
        
        try:
            branch = repo.get_branch(branch_name)
            result.append(repo)
        except GithubException as ex:
            if ex.status != 404:
                print(f"Error processing {repo.name}, Error: {ex.message}")

    return result


if __name__ == "__main__":

    # Check if the branch name is passed as a command-line argument
    if len(sys.argv) != 3:
        print("Usage: python script.py <branch_name>")
        sys.exit(1)

    organization_name = sys.argv[1]
    branch_name = sys.argv[2]

    result = search_repos_by_branch(organization_name, branch_name)

    for repo in result:
        print(f"{repo.name},https://github.com/Splitit/{repo.name}/tree/{branch_name}")


