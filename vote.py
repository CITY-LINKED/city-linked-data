
import json
import os

city = os.getenv("CITY")
if not city:
    raise Exception("No city provided.")

filename = "votes.json"

try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

data[city] = data.get(city, 0) + 1

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✅ Vote recorded for: {city}")
