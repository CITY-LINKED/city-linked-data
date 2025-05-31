import json
from datetime import datetime

# Load votes
with open("votes.json", "r") as f:
    votes = json.load(f)

# Determine vote results
timestamp = datetime.utcnow().strftime("[%Y-%m-%d %H:%M]")
log_lines = []

# Log vote results
for city, count in votes.items():
    log_lines.append(f"{timestamp} Vote cast for: {city}")
    log_lines.append(f"Total votes for {city}: {count}\n")

# Append to log
with open("voting_log.md", "a") as f:
    for line in log_lines:
        f.write(line + "\n")