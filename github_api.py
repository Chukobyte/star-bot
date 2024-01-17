import random
from typing import List, Optional, Tuple

import requests


class GithubAPI:
    @staticmethod
    def get_public_repos() -> List[dict]:
        url = 'https://api.github.com/repositories'
        repositories = []
        # Send a GET request to the GitHub API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            repositories = response.json()
            random.shuffle(repositories)
        else:
            print("Error fetching random repository")
        return repositories

    @staticmethod
    def get_random_unstarred_repo(repo_owner: str, token: str) -> Optional[Tuple[str, str, str]]:
        for repo in GithubAPI.get_public_repos():
            repo_name = repo["name"]
            repo_url = repo["html_url"]
            repo_username = repo["owner"]["login"]
            if not GithubAPI.has_user_starred_repo(repo_owner, repo_name, token):
                return repo_name, repo_url, repo_username
        return None


    @staticmethod
    def get_repo_stargazers(repo_owner: str, repo_name: str, token: str) -> List[str]:
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers'
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return [user['login'] for user in response.json()]
        else:
            print(f"Failed to get stargazers for {repo_owner}/{repo_name}. Status code: {response.status_code}")
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
    def has_user_starred_repo(repo_owner: str, repo_name: str, token: str) -> bool:
        # GitHub API endpoint to check if a repository is starred by a user
        url = f'https://api.github.com/user/starred/{repo_owner}/{repo_name}'

        # Set up headers with the user's personal access token for authentication
        headers = {'Authorization': f'token {token}'}

        # Send a GET request to the GitHub API
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 204 means the repository is starred)
        if response.status_code == 204:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise Exception(f"Failed to check repository star status.\nurl = {url}\nStatus Code: {response.status_code} Message: {response.text}")

    @staticmethod
    def star_repository(repo_owner: str, repo_name: str, token: str) -> bool:
        url = f'https://api.github.com/user/starred/{repo_owner}/{repo_name}'
        headers = {
            'Authorization': f'token {token}',
            'Content-Length': '0',
        }

        response = requests.put(url, headers=headers)

        if response.status_code == 204:
            print(f"Starred {repo_owner}/{repo_name} successfully!")
            return True
        else:
            print(f"Failed to star {repo_owner}/{repo_name}. Status code: {response.status_code} Message: {response.text}")
            print(response.text)
        return False

    @staticmethod
    def unstar_repository(repo_owner: str, repo_name: str, token: str) -> bool:
        url = f'https://api.github.com/user/starred/{repo_owner}/{repo_name}'
        headers = {
            'Authorization': f'token {token}',
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Unstarred {repo_owner}/{repo_name} successfully!")
            return True
        elif response.status_code == 404:
            print(f"{repo_owner}/{repo_name} is not starred by the user.")
        else:
            print(f"Failed to unstar {repo_owner}/{repo_name}. Status code: {response.status_code}")
            print(response.text)
        return False
