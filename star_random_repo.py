import json
import os

from github_api import GithubAPI

bot_username = "star-repo-bot"
bot_github_token = os.getenv("STAR_BOT_GITHUB_TOKEN")
starred_repos_db_file_path = "starred_repos_db.json"
number_of_repos_to_star = os.getenv("STAR_BOT_NUM_OF_REPOS_TO_STAR", default=3)

print("1. Load star repos db file")
cached_starred_repos = []
try:
    with open(starred_repos_db_file_path, 'r') as json_file:
        data = json.load(json_file)
        cached_starred_repos = data.get("repos", [])
        print(f"starred repos db loaded!  Starred repos: {cached_starred_repos}")
except FileNotFoundError:
    print(f"{starred_repos_db_file_path} doesn't exist, skipping loading...")

print("2. Star random repos")
starred_repos = []
failed_starred_repos = []
for i in range(number_of_repos_to_star):
    random_repo_name, random_repo_url, random_repo_username = GithubAPI.get_random_unstarred_repo(bot_username, bot_github_token)
    if GithubAPI.star_repository(random_repo_username, random_repo_name, bot_github_token):
        print(f"Successfully starred {random_repo_url}")
        starred_repos.append(random_repo_url)
    else:
        failed_starred_repos.append(random_repo_url)
if failed_starred_repos:
    raise Exception(f"Failed to star repos: {failed_starred_repos}")

print("3. Save new starred repo")
cached_starred_repos.extend(starred_repos)
with open("starred_repos_db.json", 'w') as json_file:
    json.dump({"repos": cached_starred_repos}, json_file, indent=2)
