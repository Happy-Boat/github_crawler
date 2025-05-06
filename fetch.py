import requests
import time
import json
import threading

GITHUB_TOKEN = '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'
headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}


class GitHubFollowRelationshipFetcher:
    def __init__(self, username, per_page=100):
        self.username = username
        self.per_page = per_page
        self.followers = []
        self.following = []
        self.relationship = {}

    def fetch_followers(self):
        page = 1
        while True:
            url = f"https://api.github.com/users/{self.username}/followers?per_page={self.per_page}&page={page}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                self.followers.extend([user['login'] for user in data])
                page += 1
            elif response.status_code == 403:
                retry_after = int(response.headers.get('Retry-After', 3600))
                print(f"Rate limited. Waiting for {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to retrieve followers: {response.status_code}, {response.text}")
                break

        with open('followers.json', 'w') as f:
            json.dump(self.followers, f, indent=4)
        print("Followers data saved successfully to followers.json")

    def fetch_following(self):
        page = 1
        while True:
            url = f"https://api.github.com/users/{self.username}/following?per_page={self.per_page}&page={page}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                self.following.extend([user['login'] for user in data])
                page += 1
            elif response.status_code == 403:
                retry_after = int(response.headers.get('Retry-After', 3600))
                print(f"Rate limited. Waiting for {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to retrieve following: {response.status_code}, {response.text}")
                break

        with open('following.json', 'w') as f:
            json.dump(self.following, f, indent=4)
        print("Following data saved successfully to following.json")

    def fetch_user_following(self, user, result_list):
        page = 1
        while True:
            url = f"https://api.github.com/users/{user}/following?per_page={self.per_page}&page={page}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                result_list.extend([u['login'] for u in data if u['login'] in set(self.followers + self.following)])
                page += 1
            elif response.status_code == 403:
                retry_after = int(response.headers.get('Retry-After', 3600))
                print(f"Rate limited while retrieving following of {user}. Waiting for {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to retrieve following of {user}: {response.status_code}, {response.text}")
                break

    def fetch_relationship(self):
        all_users = set(self.followers + self.following)
        for index, user in enumerate(all_users, start=1):
            self.relationship[user] = []
            if user in self.followers:
                user_type = 'follower'
            else:
                user_type = 'following'
            result = []
            thread = threading.Thread(target=self.fetch_user_following, args=(user, result))
            thread.start()
            start_time = time.time()
            while thread.is_alive():
                elapsed_time = time.time() - start_time
                if elapsed_time > 3600:
                    print(f"Fetching following of {user} ({user_type} #{index}) failed due to timeout. Skipping...")
                    break
                time.sleep(1)
            else:
                self.relationship[user] = result
                print(f"Successfully fetched following of {user} ({user_type} #{index})")

        with open('relationship.json', 'w') as f:
            json.dump(self.relationship, f, indent=4)
        print("Relationship data saved successfully to relationship.json")


if __name__ == "__main__":
    fetcher = GitHubFollowRelationshipFetcher("hwfan")
    fetcher.fetch_followers()
    fetcher.fetch_following()
    fetcher.fetch_relationship()
