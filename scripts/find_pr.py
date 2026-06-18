import logging
from github_commit_finder import find_commits_by_work_item
from commit_to_pr import get_pr_from_commit


OWNER = "veereshveeruu"
REPO = "azure-devops-revert-automation"


def find_pr(work_item_id):

    commits = find_commits_by_work_item(work_item_id, OWNER, REPO)

    if not commits:
        print("No commits found for work item")
        return None

    for sha in commits:

        pr_number = get_pr_from_commit(OWNER, REPO, sha)

        if pr_number:
            print("PR Found:", pr_number)
            return pr_number

    return None