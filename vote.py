
import json
from datetime import datetime

# Load vote request
with open("vote_request.json", "r") as f:
    request = json.load(f)

city = request.get("city")
user = request.get("user")
timestamp = request.get("timestamp")

if not city or not user:
    print("Invalid vote request.")
    exit(1)

# Load existing votes
try:
    with open("votes.json", "r") as f:
        votes = json.load(f)
except FileNotFoundError:
    votes = {}

# Update vote count
votes[city] = votes.get(city, 0) + 1

# Save updated votes
with open("votes.json", "w") as f:
    json.dump(votes, f, indent=2)

# Log the vote
log_entry = f"{timestamp} — {user} voted for {city}\n"
with open("Voting_Log.txt", "a") as log:
    log.write(log_entry)

# Reset vote_request.json
with open("vote_request.json", "w") as f:
    json.dump({}, f)
