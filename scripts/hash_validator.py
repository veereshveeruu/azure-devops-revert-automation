import hashlib
import logging
import logging
import os

def generate_repo_hash(repo_path="."):
    sha256 = hashlib.sha256()

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        # Ignore .git folder
        dirs[:] = [d for d in dirs if d != ".git"]

        for file in filenames:
            files.append(os.path.join(root, file))

    files.sort()

    for filepath in files:
        try:
            with open(filepath, "rb") as f:
                sha256.update(f.read())
        except Exception:
            pass

    return sha256.hexdigest()

if __name__ == "__main__":
    before_hash = generate_repo_hash()
    after_hash = generate_repo_hash()
    logging.info(f"SHA256 Before : {before_hash}")
    logging.info(f"SHA256 After : {after_hash}")
    if before_hash == after_hash:
        logging.info("Validation Passed")
    else:
        logging.info("Validation Failed")

