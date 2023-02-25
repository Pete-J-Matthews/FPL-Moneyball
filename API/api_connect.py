import requests
import mysql.connector

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
  host="fpldb.c2nundnlfyfy.eu-west-2.rds.amazonaws.com",
  user="fplusername",
  password="fplpassword",
  database="fpldb"
)

# Create a cursor object
mycursor = mydb.cursor()

# Call the FPL players API
players_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
players_response = requests.get(players_url)
players_data = players_response.json()

# Iterate over the player data and insert into MySQL
for player in players_data['elements']:
    id = player['id']
    name = player['first_name'] + ' ' + player['second_name']
    team = player['team']
    position = player['element_type']
    value = player['now_cost'] / 10.0

    sql = "INSERT INTO players (id, name, team, position, value) VALUES (%s, %s, %s, %s, %s)"
    val = (id, name, team, position, value)
    mycursor.execute(sql, val)

mydb.commit()

# Call the FPL fixtures API
fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"
fixtures_response = requests.get(fixtures_url)
fixtures_data = fixtures_response.json()

# Iterate over the fixtures data and insert into MySQL
for fixture in fixtures_data:
    fixture_id = fixture['id']
    event = fixture['event']
    home_team = fixture['team_h']
    away_team = fixture['team_a']
    home_score = fixture['team_h_score']
    away_score = fixture['team_a_score']

    sql = "INSERT INTO fixtures (fixture_id, event, home_team, away_team, home_score, away_score) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (fixture_id, event, home_team, away_team, home_score, away_score)
    mycursor.execute(sql, val)

mydb.commit()

# Close the database connection
mydb.close()
