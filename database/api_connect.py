import requests
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
  host="fpldb.c2nundnlfyfy.eu-west-2.rds.amazonaws.com",
  user="fplusername",
  password="fplpassword",
  database="-"
)

# Make a request to FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)

# Convert JSON to dictionary
data = response.json()

# Insert data into MySQL database
for player in data["elements"]:
    query = "INSERT INTO players (id, name, team_id) VALUES (%s, %s, %s)"
    values = (player["id"], player["first_name"] + " " + player["second_name"], player["team"])
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    db_connection.commit()

# Close the database connection
db_connection.close()
