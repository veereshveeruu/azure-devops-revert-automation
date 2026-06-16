from github_revert import execute_revert

story_id = input("Enter Story ID: ")

commits = input(
    "Enter commit ids separated by comma: "
).split(",")

commits = [c.strip() for c in commits]

branch = execute_revert(story_id, commits)

print(f"Created Branch: {branch}")