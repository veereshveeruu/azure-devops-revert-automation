import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.cloak-preview+json"
}

def find_commits_by_work_item(work_item_id, owner, repo):

    query = f"AB#{work_item_id}"

    url = f"https://api.github.com/search/commits?q={query}+repo:{owner}/{repo}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        raise Exception("Failed to search commits")

    data = response.json()

    commits = []

    for item in data.get("items", []):
        sha = item["sha"]
        commits.append(sha)

    return commits