import requests
import os

# ==========================
# GitHub Configuration
# ==========================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"

# ==========================
# User Input
# ==========================
branch_name = input("Enter Revert Branch Name: ").strip()

# Example:
# revert-US-123

base_branch = "main"

# ==========================
# GitHub API URL
# ==========================
url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

payload = {
    "title": f"Revert Changes from {branch_name}",
    "head": branch_name,
    "base": base_branch,
    "body": f"Automated revert PR created for branch {branch_name}"
}
import subprocess

diff = subprocess.getoutput("git diff main...HEAD")

if not diff.strip():
    print("No changes detected. PR will not be created.")
    exit(0)
response = requests.post(
    url,
    headers=headers,
    json=payload
)

print(f"\nStatus Code: {response.status_code}")

if response.status_code == 201:
    pr_data = response.json()

    print("\nPR Created Successfully")
    print(f"PR Number : {pr_data['number']}")
    print(f"PR URL    : {pr_data['html_url']}")
else:
    print("\nFailed to Create PR")
    print(response.text)