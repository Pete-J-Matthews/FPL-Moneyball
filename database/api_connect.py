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

# Call the FPL fixtures API
fixtures_url = "https://fantasy.premierleague.com/api/fixtures/?future=1"
fixtures_response = requests.get(fixtures_url)
fixtures_data = fixtures_response.json()

# Get the current gameweek
current_gw = max(fixture['event'] for fixture in fixtures_data)

# Iterate over the player data and insert into MySQL
for player in players_data['elements']:
    id = player['id']
    name = player['first_name'] + ' ' + player['second_name']
    team = player['team']
    position = player['element_type']
    form = player['form']
    value = player['now_cost'] / 10.0

    # Get the next fixture for the player's team
    next_fixture = next((fixture for fixture in fixtures_data if (fixture['event'] == current_gw) and (fixture['team_h'] == team or fixture['team_a'] == team)), None)
    if next_fixture:
        next_fixture_str = f"{next_fixture['team_h']} vs {next_fixture['team_a']}"
        home_or_away = 'H' if next_fixture['team_h'] == team else 'A'
        fixture_difficulty = next_fixture['team_h_difficulty'] if home_or_away == 'H' else next_fixture['team_a_difficulty']
    else:
        next_fixture_str = "N/A"
        home_or_away = "N/A"
        fixture_difficulty = -1

    # Check if player already exists in database
    sql = "SELECT id FROM players WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result:
        # Player already exists, update their information
        sql = "UPDATE players SET name = %s, team = %s, position = %s, form = %s, value = %s, next_fixture = %s, home_or_away = %s, fixture_difficulty = %s WHERE id = %s"
        val = (name, team, position, form, value, next_fixture_str, home_or_away, fixture_difficulty, id)
        mycursor.execute(sql, val)
    else:
        # Player does not exist, insert new row
        sql = "INSERT INTO players (id, name, team, position, form, value, next_fixture, home_or_away, fixture_difficulty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id, name, team, position, form, value, next_fixture_str, home_or_away, fixture_difficulty)
        mycursor.execute(sql, val)

mydb.commit()

# Call the FPL fixtures API
fixtures_url = "https://fantasy.premierleague.com/api/fixtures/?future=1"
fixtures_response = requests.get(fixtures_url)
fixtures_data = fixtures_response.json()

# Iterate over the fixtures data and insert into MySQL
for fixture in fixtures_data:
    fixture_id = fixture['id']
    gameweek = fixture['event']
    home_team = fixture['team_h']
    away_team = fixture['team_a']
    home_difficulty = fixture['team_h_difficulty']
    away_difficulty = fixture['team_a_difficulty']

    sql = "INSERT INTO fixtures (fixture_id, gameweek, home_team, away_team, home_difficulty, away_difficulty) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE gameweek=VALUES(gameweek), home_team=VALUES(home_team), away_team=VALUES(away_team), home_difficulty=VALUES(home_difficulty), away_difficulty=VALUES(away_difficulty)"
    mycursor.execute(sql, (fixture_id, gameweek, home_team, away_team, home_difficulty, away_difficulty))
    mydb.commit()


mydb.commit()

# Get the current gameweek
current_gw = max(fixture['event'] for fixture in fixtures_data)

# Get the user's team from the previous gameweek
user_id = 5538943
previous_gw = current_gw - 1
picks_url = f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{previous_gw}/picks/"
picks_response = requests.get(picks_url)
picks_data = picks_response.json()

# Create a dictionary of players for easy lookup
players_dict = {player['id']: player for player in players_data['elements']}

# Clear previous data for this user and gameweek
mycursor.execute("DELETE FROM user_team WHERE user_id = %s AND gameweek = %s", (user_id, previous_gw))

# Insert the user's team from the previous gameweek into the table
for pick in picks_data['picks']:
    player_id = pick['element']
    player = players_dict[player_id]

    position = pick['position']
    player_name = f"{player['first_name']} {player['second_name']}"
    team = player['team']
    form = player['form']

    # Get the next fixture for the player's team
    next_fixture = next((fixture for fixture in fixtures_data if (fixture['event'] == current_gw) and (fixture['team_h'] == team or fixture['team_a'] == team)), None)
    if next_fixture:
        next_fixture_str = f"{next_fixture['team_h']} vs {next_fixture['team_a']}"
        home_or_away = 'H' if next_fixture['team_h'] == team else 'A'
        fixture_difficulty = next_fixture['team_h_difficulty'] if home_or_away == 'H' else next_fixture['team_a_difficulty']
    else:
        next_fixture_str = "N/A"
        home_or_away = "N/A"
        fixture_difficulty = -1

    captain = pick['is_captain']
    vice_captain = pick['is_vice_captain']

    sql = """INSERT INTO user_team (user_id, gameweek, player_id, position, player_name, team, form, next_fixture, home_or_away, fixture_difficulty, captain, vice_captain) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    mycursor.execute(sql, (user_id, previous_gw, player_id, position, player_name, team, form, next_fixture_str, home_or_away, fixture_difficulty, captain, vice_captain))

mydb.commit()
