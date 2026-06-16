import subprocess
from datetime import datetime


def run_command(command):
    """
    Execute shell command and return output.
    """
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(
            f"Command failed:\n{command}\n\nError:\n{result.stderr}"
        )

    return result.stdout.strip()


def create_revert_branch(story_id):
    """
    Create a new revert branch.
    """
    branch_name = f"revert-{story_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    print(f"Creating branch: {branch_name}")

    run_command(f"git checkout -b {branch_name}")

    return branch_name


def revert_commits(commit_list):
    """
    Revert commits in reverse order.
    """
    if not commit_list:
        raise Exception("No commits found to revert.")

    print(f"Found {len(commit_list)} commits to revert")

    for commit_sha in reversed(commit_list):
        print(f"Reverting commit: {commit_sha}")

        run_command(
            f'git revert {commit_sha} --no-edit'
        )

    print("All commits reverted successfully")


def push_branch(branch_name):
    """
    Push revert branch to remote.
    """
    print(f"Pushing branch: {branch_name}")

    run_command(
        f"git push origin {branch_name}"
    )

    print("Branch pushed successfully")


def execute_revert(story_id, commit_list):
    """
    Main revert execution.
    """
    branch_name = create_revert_branch(story_id)

    revert_commits(commit_list)

    push_branch(branch_name)

    return branch_name