import requests
import mysql.connector

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

# Fetch data from the FPL API
url = "https://fantasy.premierleague.com/api/leagues-classic/314/standings/"
response = requests.get(url)
data = response.json()

# Parse and insert data into the "users" table
for entry in data['standings']['results']:
    user_id = entry['entry']
    username = entry['player_name']
    team_name = entry['entry_name']
    rank = entry['rank']

    insert_user_data(user_id, username, team_name, rank)

# Close the database connection
mydb.close()
