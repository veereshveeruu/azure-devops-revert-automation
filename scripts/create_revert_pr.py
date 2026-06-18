import os
import logging
import subprocess
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"


def create_revert_pr(branch_name):

    # Push branch first
    subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        check=True
    )

    diff = subprocess.getoutput(
        "git diff main...HEAD"
    )

    if not diff.strip():

        logging.warning(
            "No changes detected. PR will not be created."
        )

        return None

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/pulls"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "title": f"Revert Changes from {branch_name}",
        "head": branch_name,
        "base": "main",
        "body": (
            f"Automated revert PR created "
            f"for branch {branch_name}"
        )
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    logging.info(
        f"GitHub PR API Status Code: "
        f"{response.status_code}"
    )

    if response.status_code == 201:

        pr_data = response.json()

        logging.info(
            f"Revert PR Created: "
            f"{pr_data['number']}"
        )

        return pr_data["number"]

    logging.error(response.text)

    raise Exception(
        f"Failed to create PR: {response.text}"
    )