import os

from find_pr import find_pr_by_story
from get_pr_commits import get_pr_commits
from github_revert import execute_revert
from create_revert_pr import create_revert_pr
from get_workitem import update_work_item


def main():

    # From GitHub Actions (NO input())
    story_id = os.getenv("WORK_ITEM_ID")

    if not story_id:
        raise Exception("WORK_ITEM_ID is missing")

    print(f"Processing Story ID: {story_id}")

    # 1. Find PR from Work Item
    pr_number = find_pr_by_story(story_id)

    print(f"PR Found: {pr_number}")

    # 2. Get commits from PR
    commits = get_pr_commits(pr_number)

    print(f"Commits: {commits}")

    # 3. Revert commits + create branch
    branch_name = execute_revert(story_id, commits)

    print(f"Branch created: {branch_name}")

    # 4. Create revert PR
    revert_pr_number = create_revert_pr(branch_name)

    print(f"Revert PR: {revert_pr_number}")

    # 5. Update Azure DevOps work item
    update_work_item(story_id, revert_pr_number)

    print("Work item updated successfully")


if __name__ == "__main__":
    main()