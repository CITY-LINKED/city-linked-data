
import os
import json
import random

# Determine which action to perform
action = os.getenv("ADMIN_ACTION")
print(f"🔧 Running Admin Action: {action}")

base = os.getenv("GITHUB_WORKSPACE", ".")
votes_path = os.path.join(base, "votes.json")
weekly_path = os.path.join(base, "weekly_cities.json")
city_db_path = os.path.join(base, "City_Database.json")

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if action == "reset_all":
    print("♻️ Resetting everything...")
    write_json(votes_path, {})
    write_json(weekly_path, {"week": "init", "cities": []})

elif action == "add_100_votes":
    print("💯 Adding 100 votes to each city in weekly_cities.json...")
    weekly = read_json(weekly_path)
    votes = read_json(votes_path)
    for city in weekly.get("cities", []):
        votes[city] = votes.get(city, 0) + 100
    write_json(votes_path, votes)

elif action == "generate_new_cities":
    print("🔄 Generating 5 new cities from City_Database.json...")
    db = read_json(city_db_path)
    locked = [c for c in db if db[c].get("Status") == "locked"]

    def pick_by_tier(tier, count=1):
        return random.sample([c for c in locked if db[c]["Tier"] == tier], count)

    new_cities = pick_by_tier("1") + pick_by_tier("2") + pick_by_tier("3") + pick_by_tier("Minor", 2)
    write_json(weekly_path, {"week": "generated", "cities": new_cities})
    print("✅ New cities:", new_cities)

elif action == "announce_winner":
    print("🏆 Announcing winner and unlocking cities...")
    db = read_json(city_db_path)
    votes = read_json(votes_path)
    weekly = read_json(weekly_path)

    # Find winner city
    top_city = None
    top_votes = 0
    for city in weekly.get("cities", []):
        v = votes.get(city, 0)
        if v > top_votes:
            top_votes = v
            top_city = city

    # Unlock winner
    if top_city:
        db[top_city]["Status"] = "unlocked"
        votes[top_city] = 0
        print(f"🎉 Winner: {top_city}")

    # Unlock any city with 100+ votes
    for city, count in votes.items():
        if count >= 100:
            db[city]["Status"] = "unlocked"
            votes[city] = 0
            print(f"🔓 Auto-unlocked: {city}")

    write_json(city_db_path, db)
    write_json(votes_path, votes)

else:
    print("❌ Unknown action.")
