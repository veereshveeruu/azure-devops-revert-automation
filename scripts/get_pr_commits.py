import os
import requests

OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"
PR_NUMBER = input("Enter PR Number: ")

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/commits"

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

if response.status_code == 200:
    commits = response.json()

    commit_list = []

    for commit in commits:
        sha = commit["sha"]
        commit_list.append(sha)
        print(sha)

    print("\nCommit List:", commit_list)

else:
    print(response.text)