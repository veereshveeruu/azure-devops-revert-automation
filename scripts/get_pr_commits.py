import logging
import os
import requests

OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}


def get_pr_commits(pr_number):

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/pulls/{pr_number}/commits"
    )

    response = requests.get(url, headers=headers)
def get_pr_commits(pr_number):

    if not pr_number:
        logging.error("PR number is None. Skipping commit fetch.")
        return []

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/pulls/{pr_number}/commits"
    )

    response = requests.get(url, headers=headers)

    logging.info(f"GitHub API Status Code: {response.status_code}")

    if response.status_code != 200:
        logging.error(
            f"Failed to fetch commits for PR {pr_number}: {response.text}"
        )
        return []   # <-- IMPORTANT (don’t crash pipeline)

    commits = response.json()

    commit_list = []

    for commit in commits:
        sha = commit["sha"]
        commit_list.append(sha)
        logging.info(f"Commit Found: {sha}")

    logging.info(f"Commit List: {commit_list}")

    return commit_list
    logging.info(f"GitHub API Status Code: {response.status_code}")

    if response.status_code != 200:
        logging.error(
            f"Failed to fetch commits for PR {pr_number}: "
            f"{response.text}"
        )
        raise Exception(
            f"Failed to fetch commits for PR {pr_number}"
        )

    commits = response.json()

    commit_list = []

    for commit in commits:

        sha = commit["sha"]

        commit_list.append(sha)

        logging.info(f"Commit Found: {sha}")

    logging.info(f"Commit List: {commit_list}")

    return commit_list