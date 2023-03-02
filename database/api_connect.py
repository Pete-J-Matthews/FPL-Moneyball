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

# Replace with your email and password
email = 'pete.j.matt@gmail.com'
password = 'FPLpassword123!'

session = requests.session()

# Log in to the Fantasy Premier League website to obtain a session cookie
login_url = "https://users.premierleague.com/accounts/login/"
data = {
    "login": email,
    "password": password,
    "app": "plfpl-web",
    "redirect_uri": "https://fantasy.premierleague.com/",
}
with requests.Session() as session:
    session.post(login_url, data=data, headers={"User-Agent": "Dalvik"})

    manager_id = 5538943
    my_team_url = f"https://fantasy.premierleague.com/api/my-team/{manager_id}/"
    my_team_data = session.get(my_team_url)
    print(my_team_data.headers)
    print(my_team_data.text)
