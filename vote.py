
import json
import os

# Get the city from environment variable
city = os.getenv("CITY")
if not city:
    raise Exception("No city provided in CITY environment variable.")

# Determine the correct path for votes.json inside GitHub workspace
workspace = os.getenv("GITHUB_WORKSPACE", ".")
votes_path = os.path.join(workspace, "votes.json")

print(f"📍 GITHUB_WORKSPACE: {workspace}")
print(f"🗳️ Voting for city: {city}")
print(f"📄 votes.json path: {votes_path}")

# Load or initialize the votes data
try:
    with open(votes_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("📂 votes.json not found, creating a new one.")
    data = {}

# Update the vote count
data[city] = data.get(city, 0) + 1

# Write the updated data back
with open(votes_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Vote successfully recorded.")
