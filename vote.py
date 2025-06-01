import json
import os
from datetime import datetime

def load_votes():
    if os.path.exists("votes.json"):
        with open("votes.json", "r") as f:
            return json.load(f)
    return {}

def save_votes(votes):
    with open("votes.json", "w") as f:
        json.dump(votes, f, indent=2)

def append_log(entry):
    with open("Voting_Log.txt", "a") as f:
        f.write(entry + "\n")

with open("vote_request.json", "r") as f:
    vote_data = json.load(f)

votes = load_votes()
city = vote_data["city"]
user = vote_data["user"]

votes[city] = votes.get(city, 0) + 1
save_votes(votes)

log_entry = f"{datetime.utcnow().isoformat()} | VOTE | {user} -> {city}"
append_log(log_entry)
