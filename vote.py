import json
import os

city = os.getenv("CITY")
if not city:
    raise Exception("No city provided.")

# Always operate from repo root
repo_dir = os.getenv("GITHUB_WORKSPACE", ".")
votes_file = os.path.join(repo_dir, "votes.json")

print(f"Voting for {city}")
print(f"Using file path: {votes_file}")

try:
    with open(votes_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

data[city] = data.get(city, 0) + 1

with open(votes_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Vote recorded.")
