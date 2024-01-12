import json
import os
from typing import List

import requests


class GithubAPI:
    @staticmethod
    def get_repo_stargazers(owner: str, repo:str, token: str) -> List[str]:
        url = f'https://api.github.com/repos/{owner}/{repo}/stargazers'
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return [user['login'] for user in response.json()]
        else:
            print(f"Failed to get stargazers for {owner}/{repo}. Status code: {response.status_code}")
            print(response.text)
            return []

    @staticmethod
    def get_user_repositories(username: str, token: str) -> List[str]:
        url = f'https://api.github.com/users/{username}/repos'
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return [repo['name'] for repo in response.json()]
        else:
            print(f"Failed to get repositories for {username}. Status code: {response.status_code}")
            print(response.text)
            return []

    @staticmethod
    def star_repository(owner, repo, token) -> bool:
        url = f'https://api.github.com/user/starred/{owner}/{repo}'
        headers = {
            'Authorization': f'token {token}',
            'Content-Length': '0',
        }

        response = requests.put(url, headers=headers)

        if response.status_code == 204:
            print(f"Starred {owner}/{repo} successfully!")
            return True
        else:
            print(f"Failed to star {owner}/{repo}. Status code: {response.status_code}")
            print(response.text)
        return False

    @staticmethod
    def unstar_repository(owner, repo, token) -> bool:
        url = f'https://api.github.com/user/starred/{owner}/{repo}'
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Unstarred {owner}/{repo} successfully!")
            return True
        elif response.status_code == 404:
            print(f"{owner}/{repo} is not starred by the user.")
        else:
            print(f"Failed to unstar {owner}/{repo}. Status code: {response.status_code}")
            print(response.text)
        return False


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
            # GithubAPI.unstar_repository(gazer, repo, bot_github_token)
            print(f"Unstarred {gazer}/{repo}")
print("")

print("4. Star all users repos that starred this one")
for gazer in stargazers:
    user_repos = GithubAPI.get_user_repositories(gazer, bot_github_token)
    for repo in user_repos:
        # GithubAPI.star_repository(gazer, repo, bot_github_token)
        print(f"Starred {gazer}/{repo}")
print("")

print("5. Save the current stargazers for later use")
with open("stargazers_db.json", 'w') as json_file:
    json.dump({"users": stargazers}, json_file, indent=2)
