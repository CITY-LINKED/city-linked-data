import json
import os
import random
import pandas as pd
from datetime import datetime
from smtplib import SMTP
from email.mime.text import MIMEText

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def unlock_city(database, city_name):
    for city in database:
        if city['City'] == city_name:
            city['Status'] = 'unlocked'
            city['Votes'] = 0
    return database

def pick_cities(city_db):
    tiers = {'1': [], '2': [], '3': [], '': []}
    for entry in city_db:
        if entry['Status'] == 'locked':
            tiers[str(entry['Tier']) if 'Tier' in entry and entry['Tier'] in [1,2,3] else ''].append(entry['City'])

    selected = [
        random.choice(tiers['1']),
        random.choice(tiers['2']),
        random.choice(tiers['3']),
    ] + random.sample(tiers[''], 2)
    return selected

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'citylinked@github'
    msg['To'] = to_email

    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(os.environ['EMAIL_SENDER'], os.environ['EMAIL_PASSWORD'])
        smtp.send_message(msg)

def main():
    now = datetime.utcnow()
    is_monday = now.weekday() == 0
    is_friday = now.weekday() == 4

    votes = load_json('votes.json')
    city_db = load_json('City_Database.json')
    weekly_cities = []

    if is_friday:
        vote_counts = votes.get('votes', {})
        voted_city = max(vote_counts, key=vote_counts.get) if vote_counts else None
        vote_total = vote_counts.get(voted_city, 0) if voted_city else 0

        unlocked = []
        if voted_city:
            city_db = unlock_city(city_db, voted_city)
            unlocked.append(voted_city)

        for city_name, count in vote_counts.items():
            if count >= 100 and city_name != voted_city:
                city_db = unlock_city(city_db, city_name)
                unlocked.append(city_name)

        votes = {'week': votes.get('week', 1) + 1, 'votes': {}}
        weekly_cities = pick_cities(city_db)

        summary = f"🏆 Voting Results - Week {votes['week'] - 1}\n\n"
        summary += f"Votes received: {vote_counts}\n"
        summary += f"Unlocked cities: {', '.join(unlocked) if unlocked else 'None'}\n\n"
        summary += f"Next week’s cities: {', '.join(weekly_cities)}\n"
        summary += "To do: send announcement + preview."

        with open('weekly_summary.txt', 'w') as report:
        report.write(summary)

        save_json(city_db, 'City_Database.json')
        save_json(weekly_cities, 'weekly_cities.json')
        save_json(votes, 'votes.json')

    elif is_monday:
        weekly_cities = pick_cities(city_db)
        votes = {'week': votes.get('week', 1), 'votes': {}}
        save_json(weekly_cities, 'weekly_cities.json')
        save_json(votes, 'votes.json')

if __name__ == "__main__":
    main()