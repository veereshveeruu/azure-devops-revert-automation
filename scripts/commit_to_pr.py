import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_pr_from_commit(owner, repo, sha):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}/pulls"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        return None

    prs = response.json()

    if not prs:
        return None

    return prs[0]["number"]