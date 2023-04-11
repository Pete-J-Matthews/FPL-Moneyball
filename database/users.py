import mysql.connector
import requests

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
  host="fpldb.c2nundnlfyfy.eu-west-2.rds.amazonaws.com",
  user="fplusername",
  password="fplpassword",
  database="fpldb"
)

# Function to insert user data into the "users" table
def insert_user_data(user_id, username, team_name, rank):
    cursor = mydb.cursor()
    query = "INSERT INTO users (user_id, username, team_name, rank) VALUES (%s, %s, %s, %s)"
    values = (user_id, username, team_name, rank)
    cursor.execute(query, values)
    mydb.commit()

# Function to fetch data from the FPL API with pagination
def fetch_data(page_number):
    url = f"https://fantasy.premierleague.com/api/leagues-classic/314/standings/?page={page_number}"
    response = requests.get(url)
    return response.json()

# Parse and insert data into the "users" table
page = 1
has_next = True

while has_next:
    data = fetch_data(page)
    has_next = data['standings']['has_next']

    for entry in data['standings']['results']:
        user_id = entry['entry']
        username = entry['player_name']
        team_name = entry['entry_name']
        rank = entry['rank']

        insert_user_data(user_id, username, team_name, rank)

    page += 1

# Close the database connection
mydb.close()