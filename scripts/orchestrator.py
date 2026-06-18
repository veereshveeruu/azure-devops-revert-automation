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

        print("Processing:", story_id)

        try:
            pr_number = find_pr(story_id)
            print(f"PR Found: {pr_number}")

            commits = get_pr_commits(pr_number)
            print(f"Commits: {commits}")

            branch_name = execute_revert(story_id, commits)
            print(f"Branch created: {branch_name}")

            revert_pr_number = create_revert_pr(branch_name)
            print(f"Revert PR: {revert_pr_number}")

            update_work_item(story_id, revert_pr_number)
            print("Work item updated successfully")

        except Exception as e:
            print(f"FAILED for story_id {story_id}: {e}")
            raise

    for story_id in story_ids:

        try:

            story_id = story_id.strip()

            print(f"\nProcessing Story ID: {story_id}")
            logging.info(f"Story ID: {story_id}")

            # Find PR
            pr_number = find_pr(story_id)

            print(f"PR Found: {pr_number}")
            logging.info(f"PR Found: {pr_number}")

            # Get commits
            commits = get_pr_commits(pr_number)

            print(f"Commits: {commits}")
            logging.info(f"Commits Found: {commits}")

            # Execute revert
            branch_name = execute_revert(story_id, commits)

            print(f"Branch created: {branch_name}")
            logging.info(f"Revert Branch Created: {branch_name}")

            # Generate SHA256 after revert
            after_hash = generate_repo_hash()

            with open("sha256-after.txt", "w") as f:
                f.write(after_hash)

            print(f"After Hash: {after_hash}")
            logging.info(f"After Hash: {after_hash}")

            # Compare with original SHA256
            if os.path.exists("sha256-before.txt"):

                with open("sha256-before.txt", "r") as f:
                    before_hash = f.read().strip()

                print(f"Before Hash: {before_hash}")
                logging.info(f"Before Hash: {before_hash}")

                if before_hash == after_hash:
                    print("✅ Rollback Successful - Hash Match")
                    logging.info("Rollback Successful - Hash Match")
                else:
                    print("❌ Rollback Validation Failed - Hash Mismatch")
                    logging.error("Rollback Validation Failed - Hash Mismatch")

            else:
                print("⚠ sha256-before.txt not found. Skipping validation.")
                logging.warning(
                    "sha256-before.txt not found. Skipping validation."
                )

            # Create revert PR
            revert_pr_number = create_revert_pr(branch_name)

            print(f"Revert PR: {revert_pr_number}")
            logging.info(f"Revert PR Created: {revert_pr_number}")

            # Update Azure DevOps work item
            update_work_item(story_id, revert_pr_number)

            print("Work item updated successfully")
            logging.info("Azure DevOps Work Item Updated Successfully")

        except Exception as e:

            logging.exception(
                f"Workflow Failed for Story ID {story_id}: {str(e)}"
            )

            raise


if __name__ == "__main__":
    main()