import json
import os

from github_api import GithubAPI


owner_user_name = "Chukobyte"
owner_repo = "star-bot"
bot_github_token = os.getenv("STAR_BOT_GITHUB_TOKEN")
stargazers_db_file_path = "stargazers_db.json"

print("1. Loading stargazers db file if it exists")
saved_stargazers = []
try:
    with open(stargazers_db_file_path, 'r') as json_file:
        data = json.load(json_file)
        saved_stargazers = data.get("users", [])
        print(f"Stargazers db loaded!  Saved stargazers: {saved_stargazers}")
except FileNotFoundError:
    print(f"{stargazers_db_file_path} doesn't exist, skipping loading...")
print("")

print("2. Getting current stargazers")
stargazers = GithubAPI.get_repo_stargazers(owner_user_name, owner_repo, bot_github_token)
print(f"Current stargazers: {stargazers}")
print(f"Current stargazers count: {len(stargazers)}")
print("")

print("3. Unstarring user repos who unstarred this one")
for gazer in saved_stargazers:
    if gazer not in stargazers:
        for repo in GithubAPI.get_user_repositories(gazer, bot_github_token):
            GithubAPI.unstar_repository(gazer, repo, bot_github_token)
            print(f"Unstarred {gazer}/{repo}")
print("")

print("4. Star all users repos that starred this one")
for gazer in stargazers:
    user_repos = GithubAPI.get_user_repositories(gazer, bot_github_token)
    for repo in user_repos:
        GithubAPI.star_repository(gazer, repo, bot_github_token)
        print(f"Starred {gazer}/{repo}")
print("")

print("5. Save the current stargazers for later use")
with open("stargazers_db.json", 'w') as json_file:
    json.dump({"users": stargazers}, json_file, indent=2)
