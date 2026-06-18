import os
import logging
import traceback

from find_pr import find_pr
from get_pr_commits import get_pr_commits
from github_revert import execute_revert
from create_revert_pr import create_revert_pr
from get_workitem import update_work_item
from hash_validator import generate_repo_hash



# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/revert_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    print("=== ORCHESTRATOR STARTED ===")

    story_ids = os.getenv("WORK_ITEM_IDS")

    print("WORK_ITEM_IDS:", story_ids)

    if not story_ids:
        raise Exception("WORK_ITEM_IDS is missing")

    story_ids = story_ids.split(",")

    for story_id in story_ids:

        story_id = story_id.strip()

        print(f"\nProcessing Story ID: {story_id}")
        logging.info(f"Story ID: {story_id}")

        try:

            # Step 1: Find PR
            pr_number = find_pr(story_id)

            print(f"PR Found: {pr_number}")
            logging.info(f"PR Found: {pr_number}")

            if not pr_number:
                print(f"❌ No PR found for {story_id}. Skipping.")
                continue

            # Step 2: Get commits
            commits = get_pr_commits(pr_number)

            print(f"Commits: {commits}")
            logging.info(f"Commits: {commits}")

            if not commits:
                print(f"⚠ No commits for PR {pr_number}. Skipping.")
                continue

            # Step 3: Revert
            branch_name = execute_revert(story_id, commits)

            print(f"Branch created: {branch_name}")
            logging.info(f"Branch created: {branch_name}")

            # Step 4: SHA validation
            after_hash = generate_repo_hash()

            with open("sha256-after.txt", "w") as f:
                f.write(after_hash)

            # Step 5: Compare
            if os.path.exists("sha256-before.txt"):

                with open("sha256-before.txt", "r") as f:
                    before_hash = f.read().strip()

                if before_hash == after_hash:
                    print("✅ Rollback Successful")
                else:
                    print("❌ Rollback Failed")

            # Step 6: Create PR
            revert_pr_number = create_revert_pr(branch_name)

            print(f"Revert PR: {revert_pr_number}")

            # Step 7: Update Work Item
            update_work_item(story_id, revert_pr_number)

            print("Work item updated successfully")

        except Exception as e:
            logging.exception(f"Failed for {story_id}: {str(e)}")
            print(f"FAILED for {story_id}: {e}")


if __name__ == "__main__":
    main()