import os
import psycopg2
import random
import requests
import time
from psycopg2 import sql
from datetime import datetime as dt

# Users enter the league at the start of the season therefore this script runs annually

def get_db_name():
    now = dt.now()
    year = now.year
    month = now.month

    if month >= 8:  # If it's August or later, the season is this year / next year
        season = f"{year}-{year+1}"
    else:  # Otherwise, the season is last year / this year
        season = f"{year-1}-{year}"

    return f"fpl-users-db-{season}"

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'yourusername')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'yourpassword')
DB_NAME = os.getenv('DB_NAME', 'yourdatabase')

# File to store the last processed page number
PAGE_FILE = 'last_page.txt'

# Function to establish a connection to the PostgreSQL database
def connect_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None
# Function to insert user data into the "users" table
def insert_user_data(conn, user_id, username, team_name, rank):
    with conn.cursor() as cursor:
        query = sql.SQL("INSERT INTO users (user_id, username, team_name, rank) VALUES (%s, %s, %s, %s)")
        values = (user_id, username, team_name, rank)
        cursor.execute(query, values)

# Function to fetch data from the FPL API with pagination
def fetch_data(page_number):
    url = f"https://fantasy.premierleague.com/api/leagues-classic/314/standings/?page_standings={page_number}"
    response = requests.get(url)
    return response.json()

# Function to get the last processed page number
def get_last_page():
    try:
        with open(PAGE_FILE, 'r') as f:
            return int(f.read().strip())
    except Exception:
        return 1  # Start from page 1 if the file doesn't exist or can't be read

# Function to update the last processed page number
def update_last_page(page):
    with open(PAGE_FILE, 'w') as f:
        f.write(str(page))

# Function to parse and insert data into the "users" table
def process_data():
    page = get_last_page()
    has_next = True

    conn = connect_db()
    if conn is None:
        print("Could not connect to the database. Exiting.")
        return

    while has_next:
        data = fetch_data(page)
        if data is None:
            print("Could not fetch data. Exiting.")
            break

        has_next = data['standings']['has_next']

        for entry in data['standings']['results']:
            user_id = entry['entry']
            username = entry['player_name']
            team_name = entry['entry_name']
            rank = entry['rank']

            insert_user_data(conn, user_id, username, team_name, rank)

        conn.commit()

        if has_next:
            page += 1
            update_last_page(page)
            sleep_time = random.uniform(5, 8)  # Generate random sleep time
            time.sleep(sleep_time)

    conn.close()

if __name__ == "__main__":
    process_data()
