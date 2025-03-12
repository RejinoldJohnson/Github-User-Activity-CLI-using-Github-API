import requests
from collections import defaultdict

def get_github_user_data(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print("No activty for this user")
            return None
        return data
    elif response.status_code == 404:
        print("There is no user with this username")
        return None
    else:
        print("An error occured while fetching data")
        return None
    
def extract_user_data(events):
    if not events:
        return None
    
    event_counts = defaultdict(lambda: defaultdict(int))
    
    for event in events:
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            event_counts[repo_name]["PushEvent"] += commit_count
        elif event_type == "IssuesEvent" and event["payload"]["action"] == "opened":
            event_counts[repo_name]["IssuesEvent"] += 1
        elif event_type == "WatchEvent" and event["payload"]["action"] == "started":
            event_counts[repo_name]["WatchEvent"] += 1
    
    return event_counts

def format_event_details(event_counts):
    event_details = []
    for repo_name, counts in event_counts.items():
        if "PushEvent" in counts:
            event_details.append(f"- Pushed {counts['PushEvent']} commits to {repo_name}")
        if "IssuesEvent" in counts:
            event_details.append(f"- Opened {counts['IssuesEvent']} issues in {repo_name}")
        if "WatchEvent" in counts:
            event_details.append(f"- Starred {repo_name} {counts['WatchEvent']} times")
    return event_details


def main():
    username = input("Enter your Github username: ")
    user_data = get_github_user_data(username)
    if user_data:
        event_counts = extract_user_data(user_data)
        if event_counts:
            event_details = format_event_details(event_counts)
            for detail in event_details:
                print(detail)
                
if __name__ == "__main__":
    main()