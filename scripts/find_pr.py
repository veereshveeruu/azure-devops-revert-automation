import os
import requests

OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# User Story ID comes from input

work_item_id = os.getenv("WORK_ITEM_ID")

response = requests.get(
    f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=all",
    headers=headers
)

prs = response.json()

if response.status_code != 200:
    print("GitHub API Error:")
    print(prs)
    exit()

search_text = f"AB#{work_item_id}"

pr_found = False

for pr in prs:
    if search_text in pr["title"]:
        print("PR Found")
        print("PR Number:", pr["number"])
        print("Title:", pr["title"])
        pr_found = True
        break

if not pr_found:
    print(f"No PR found for {search_text}")