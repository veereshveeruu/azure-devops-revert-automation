import logging
import subprocess
from datetime import datetime


def branch_exists(branch_name):
    result = subprocess.run(
        ["git", "rev-parse", "--verify", branch_name],
        capture_output=True,
        text=True
    )

    return result.returncode == 0


def create_revert_branch(story_id):

    target_branch = "main"

    if not branch_exists(target_branch):

        logging.error(f"Branch {target_branch} not found")

        raise Exception(
            f"Target branch {target_branch} not found"
        )

    # Checkout latest main
    subprocess.run(
        ["git", "checkout", target_branch],
        check=True
    )

    subprocess.run(
        ["git", "pull", "origin", target_branch],
        check=True
    )

    # Create revert branch
    date_str = datetime.now().strftime("%Y%m%d")

    branch_name = f"revert-ab{story_id}-{date_str}"

    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        logging.error(
            f"Failed to create revert branch {branch_name}"
        )

        logging.error(result.stderr)

        raise Exception(
            f"Failed to create revert branch {branch_name}"
        )

    logging.info(f"Created branch {branch_name}")

    return branch_name


def execute_revert(story_id, commits):

    logging.info(f"Original Commit Order: {commits}")

    reversed_commits = list(reversed(commits))

    logging.info(f"Revert Order: {reversed_commits}")

    branch_name = create_revert_branch(story_id)

    for commit in reversed_commits:

        logging.info(f"Reverting Commit: {commit}")

        result = subprocess.run(
            ["git", "revert", "--no-edit", commit],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            logging.error(
                f"Git revert failed for commit {commit}"
            )

            logging.error(result.stderr)

            subprocess.run(
                ["git", "revert", "--abort"],
                capture_output=True,
                text=True
            )

            if "CONFLICT" in result.stderr.upper():

                raise Exception(
                    f"Merge conflict detected while reverting commit {commit}"
                )

            raise Exception(
                f"Git revert failed for commit {commit}"
            )

        logging.info(
            f"Successfully Reverted: {commit}"
        )

    # Add skip-ci to final revert commit
    logging.info(
        f"Adding [skip ci] to revert commit for Story ID {story_id}"
    )

    subprocess.run(
        [
            "git",
            "commit",
            "--amend",
            "-m",
            f"[skip ci] Revert AB#{story_id}"
        ],
        check=True
    )

    return branch_name