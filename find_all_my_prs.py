import csv
import os
import sys
from github import Github, GithubException
import tempfile


def get_open_pull_requests(organization_name, user_name):
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)

    organization = g.get_organization(organization_name)
    repositories = organization.get_repos()

    result = []

    for index, repo in enumerate(repositories):
        pull_requests = repo.get_pulls(state='open')

        if index%10 == 0:
            print(f"Processing {index+1} of {repositories.totalCount}")

        for pr in pull_requests:
            if pr.user.login == user_name:
                result.append((repo.name, pr))

    return result

def save_to_temp_csv(open_pull_requests):
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["Repo Name","Title", "User", "State", "Url", "Diff Url"])  # Write header
        for pr in open_pull_requests:
            writer.writerow([pr[0], pr[1].title, pr[1].user.login, pr[1].state, pr[1].html_url, pr[1].diff_url])  

    os.startfile(temp_file.name)

if __name__ == "__main__":

    # Check if the branch name is passed as a command-line argument
    if len(sys.argv) != 3:
        print("Usage: python find_by_branch.py <organization_name> <user_name>")
        sys.exit(1)

    organization_name = sys.argv[1]
    user_name = sys.argv[2]

    result = get_open_pull_requests(organization_name, user_name)

    save_to_temp_csv(result)


