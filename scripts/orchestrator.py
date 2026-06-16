import find_pr
import get_pr_commits
import github_revert
import create_revert_pr
import update_work_item
import os
import requests
import execute_revert

story_id = input("Enter Story ID: ")

pr_number = find_pr(story_id)

commits = get_pr_commits(pr_number)

branch_name = execute_revert(story_id, commits)

pr_number = create_revert_pr(branch_name)

update_work_item(story_id, pr_number)