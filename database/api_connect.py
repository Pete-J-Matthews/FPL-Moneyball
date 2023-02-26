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
    form = player['form']
    value = player['now_cost'] / 10.0

    # Check if player already exists in database
    sql = "SELECT id FROM players WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result:
        # Player already exists, update their information
        sql = "UPDATE players SET name = %s, team = %s, position = %s, form = %s, value = %s WHERE id = %s"
        val = (name, team, position, form, value, id)
        mycursor.execute(sql, val)
    else:
        # Player does not exist, insert new row
        sql = "INSERT INTO players (id, name, team, position, form, value) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id, name, team, position, form, value)
        mycursor.execute(sql, val)

mydb.commit()

# Call the FPL fixtures API
fixtures_url = "https://fantasy.premierleague.com/api/fixtures?future=1)/"
fixtures_response = requests.get(fixtures_url)
fixtures_data = fixtures_response.json()

# Iterate over the fixtures data and insert into MySQL
for fixture in fixtures_data:
    fixture_id = fixture['id']
    event = fixture['event']
    home_team = fixture['team_h']
    away_team = fixture['team_a']
    team_h_difficulty = fixture['team_h_difficulty']
    team_a_difficulty = fixture['team_a_difficulty']

    sql = "INSERT INTO fixtures (fixture_id, event, home_team, away_team, team_h_difficulty, team_a_difficulty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (fixture_id, event, home_team, away_team, team_h_difficulty, team_a_difficulty)
    mycursor.execute(sql, val)

mydb.commit()

# Call the FPL my team API
manager_id = 5538943  # This my ID as a placeholder but will become a variable thats updated by a frontend input from the user.
my_team_url = f"https://fantasy.premierleague.com/api/my-team/{manager_id}/"
my_team_response = requests.get(my_team_url)
my_team_data = my_team_response.json()

# Iterate over the player data in my team and update the "selected_by" column in the players table
for player in my_team_data["picks"]:
    player_id = player['element']
    selected_by_percent = player['selected_by_percent']

    sql = "UPDATE players SET selected_by = %s WHERE id = %s"
    val = (selected_by_percent, player_id)
    mycursor.execute(sql, val)

mydb.commit()

# Close the database connection
mydb.close()
