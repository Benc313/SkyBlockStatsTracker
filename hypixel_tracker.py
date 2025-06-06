# hypixel_tracker.py

import json
import sqlite3
import time
import os
import requests
from dotenv import load_dotenv
from skyblock_constants import SKILL_DATA, BESTIARY_THRESHOLDS, BESTIARY_FAMILIES
# NOTE: You must have skyblock_constants.py and collections.json in the same directory.

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("HYPIXEL_API_KEY")
DATABASE_FILE = 'skyblock_stats.db'
PLAYER_UUID = "46cd959156324f668005c96d432ddb56"
PROFILE_ID = "46cd9591-5632-4f66-8005-c96d432ddb56"

# --- Helper Functions ---

def load_collection_data():
    """Loads the collection thresholds from the collections.json file."""
    try:
        with open('collections.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: collections.json not found.")
        return {}

COLLECTION_THRESHOLDS = load_collection_data()

def calculate_level(skill_name, xp):
    """Calculates skill level based on its name and total XP."""
    thresholds = SKILL_DATA.get(skill_name, SKILL_DATA["standard"])
    max_level = len(thresholds)
    if xp >= thresholds[-1]: return max_level
    level = 0
    for i, threshold in enumerate(thresholds):
        if xp >= threshold: level = i + 1
        else: break
    return level

def calculate_tier(collection_name, amount):
    """Calculates collection tier based on its name and amount collected."""
    thresholds = COLLECTION_THRESHOLDS.get(collection_name.upper())
    if not thresholds: return 0
    max_tier = len(thresholds)
    if amount >= thresholds[-1]: return max_tier
    tier = 0
    for i, threshold in enumerate(thresholds):
        if amount >= threshold: tier = i + 1
        else: break
    return tier

def fetch_hypixel_data(api_key, profile_id):
    """Fetches Skyblock profile data from the Hypixel API."""
    if not api_key:
        print("Error: HYPIXEL_API_KEY not found in .env file.")
        return None
    url = f"https://api.hypixel.net/v2/skyblock/profile?profile={profile_id}"
    headers = {"API-Key": api_key}
    print(f"Fetching data from Hypixel API for profile: {profile_id}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("profile") if data.get("success") else None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def create_database_schema(cursor):
    """Creates all necessary tables in the SQLite database."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile_snapshots (
            profile_id TEXT NOT NULL, member_uuid TEXT NOT NULL, snapshot_timestamp INTEGER NOT NULL,
            cute_name TEXT, purse REAL, death_count INTEGER, kills INTEGER, bank_balance REAL,
            PRIMARY KEY (profile_id, member_uuid, snapshot_timestamp)
        )
    ''')
    try:
        cursor.execute('ALTER TABLE profile_snapshots ADD COLUMN bank_balance REAL')
    except sqlite3.OperationalError:
        pass # Column already exists

    cursor.execute('''CREATE TABLE IF NOT EXISTS skill_snapshots (snapshot_id INTEGER PRIMARY KEY, member_uuid TEXT, profile_id TEXT, snapshot_timestamp INTEGER, skill_name TEXT, total_xp REAL, level INTEGER, FOREIGN KEY (profile_id, member_uuid, snapshot_timestamp) REFERENCES profile_snapshots (profile_id, member_uuid, snapshot_timestamp))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS slayer_snapshots (snapshot_id INTEGER PRIMARY KEY, member_uuid TEXT, profile_id TEXT, snapshot_timestamp INTEGER, slayer_name TEXT, total_xp INTEGER, tier1_kills INTEGER, tier2_kills INTEGER, tier3_kills INTEGER, tier4_kills INTEGER, tier5_kills INTEGER, FOREIGN KEY (profile_id, member_uuid, snapshot_timestamp) REFERENCES profile_snapshots (profile_id, member_uuid, snapshot_timestamp))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS collection_snapshots (snapshot_id INTEGER PRIMARY KEY, member_uuid TEXT, profile_id TEXT, snapshot_timestamp INTEGER, collection_name TEXT, amount INTEGER, tier INTEGER, FOREIGN KEY (profile_id, member_uuid, snapshot_timestamp) REFERENCES profile_snapshots (profile_id, member_uuid, snapshot_timestamp))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bank_transactions (transaction_id INTEGER PRIMARY KEY, profile_id TEXT, timestamp INTEGER UNIQUE, action TEXT, amount REAL, initiator_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bestiary_snapshots (snapshot_id INTEGER PRIMARY KEY, member_uuid TEXT, profile_id TEXT, snapshot_timestamp INTEGER, mob_id TEXT, kills INTEGER, UNIQUE(profile_id, member_uuid, snapshot_timestamp, mob_id))''')
    print("Database schema created or verified successfully.")

def parse_and_insert_data(cursor, data, snapshot_timestamp):
    """Parses the JSON data and inserts it into the SQLite database tables."""
    if not data: return
    profile_id = data.get('profile_id')
    bank_balance = data.get('banking', {}).get('balance', 0)

    if 'banking' in data and 'transactions' in data['banking']:
        for tx in data['banking']['transactions']:
            cursor.execute('INSERT OR IGNORE INTO bank_transactions VALUES (NULL, ?, ?, ?, ?, ?)', (profile_id, tx.get('timestamp'), tx.get('action'), tx.get('amount'), tx.get('initiator_name')))
        print(f"Processed {len(data['banking']['transactions'])} bank transactions.")

    for member_uuid, member_data in data.get('members', {}).items():
        if member_uuid != PLAYER_UUID: continue
        print(f"\nProcessing member: {member_uuid}")
        player_data = member_data.get('player_data', {})
        player_stats_data = member_data.get('player_stats', {})
        death_count = player_data.get('death_count', 0)
        raw_kills = player_stats_data.get('kills', 0)
        kill_count = sum(raw_kills.values()) if isinstance(raw_kills, dict) else raw_kills
        purse_amount = member_data.get('currencies', {}).get('coin_purse', 0)
        
        cursor.execute('INSERT OR IGNORE INTO profile_snapshots VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                       (profile_id, member_uuid, snapshot_timestamp, data.get('cute_name', 'N/A'), purse_amount, death_count, kill_count, bank_balance))
        print(f"  - Added entry to profile_snapshots.")
        
        experience_data = player_data.get('experience', {})
        if experience_data:
            skills = {k.replace('SKILL_', '').lower(): v for k, v in experience_data.items()}
            for skill_name, xp in skills.items():
                current_level = calculate_level(skill_name, xp)
                cursor.execute('INSERT OR IGNORE INTO skill_snapshots VALUES (NULL, ?, ?, ?, ?, ?, ?)', (member_uuid, profile_id, snapshot_timestamp, skill_name, xp, current_level))
            print(f"  - Processed {len(skills)} skills.")

        slayers = member_data.get('slayer', {}).get('slayer_bosses', {})
        if slayers:
            for name, s_data in slayers.items():
                if 'xp' not in s_data: continue
                cursor.execute('INSERT OR IGNORE INTO slayer_snapshots VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (member_uuid, profile_id, snapshot_timestamp, name, s_data.get('xp', 0), s_data.get('boss_kills_tier_0', 0), s_data.get('boss_kills_tier_1', 0), s_data.get('boss_kills_tier_2', 0), s_data.get('boss_kills_tier_3', 0), s_data.get('boss_kills_tier_4', 0)))
            print(f"  - Processed {len(slayers)} slayers.")
        
        collections = member_data.get('collection', {})
        if collections:
            for name, amount in collections.items():
                current_tier = calculate_tier(name, amount)
                cursor.execute('INSERT OR IGNORE INTO collection_snapshots VALUES (NULL, ?, ?, ?, ?, ?, ?)', (member_uuid, profile_id, snapshot_timestamp, name.upper(), amount, current_tier))
            print(f"  - Processed {len(collections)} collections.")

        bestiary_data = member_data.get('bestiary', {})
        if bestiary_data:
            mob_kills = bestiary_data.get('kills', {})
            for mob_id, kill_count in mob_kills.items():
                cursor.execute('INSERT OR IGNORE INTO bestiary_snapshots VALUES (NULL, ?, ?, ?, ?, ?)', (member_uuid, profile_id, snapshot_timestamp, mob_id, kill_count))
            print(f"  - Processed {len(mob_kills)} bestiary entries.")

def main():
    """Main function to run the script."""
    profile_data = fetch_hypixel_data(API_KEY, PROFILE_ID)
    if not profile_data:
        print("Halting execution due to API fetch failure.")
        return
    snapshot_timestamp = int(time.time())
    print(f"\nUsing snapshot timestamp: {snapshot_timestamp}")

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        print(f"Successfully connected to database '{DATABASE_FILE}'.")
        create_database_schema(cursor)
        parse_and_insert_data(cursor, profile_data, snapshot_timestamp)
        conn.commit()
        print("\nAll data has been successfully committed to the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    main()
