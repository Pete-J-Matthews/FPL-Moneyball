CREATE DATABASE IF NOT EXISTS fpldb;

USE fpldb;

CREATE TABLE IF NOT EXISTS players (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  team INT,
  position INT,
  form DECIMAL(4,2),
  value DECIMAL(4,1),
  next_fixture VARCHAR(255),
  home_or_away CHAR(1),
  fixture_difficulty INT
);

CREATE TABLE IF NOT EXISTS fixtures (
  fixture_id INT PRIMARY KEY,
  gameweek INT,
  home_team INT,
  away_team INT,
  home_difficulty INT,
  away_difficulty INT
);

-- Table for user team
CREATE TABLE IF NOT EXISTS user_team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    gameweek INT NOT NULL,
    player_id INT NOT NULL,
    position INT NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    team INT NOT NULL,
    form DECIMAL(4,1) NOT NULL,
    value DECIMAL(4,1) NOT NULL,
    next_fixture VARCHAR(255) NOT NULL,
    home_or_away CHAR(1) NOT NULL,
    fixture_difficulty INT NOT NULL,
    captain BOOLEAN NOT NULL,
    vice_captain BOOLEAN NOT NULL
);

-- Sort the players table by fixture difficulty ascending, home/away descending, form descending, and value descending
SELECT *
FROM players
ORDER BY fixture_difficulty ASC, home_or_away DESC, form DESC, value DESC;

-- Sort the user_team table by fixture difficulty ascending, home/away descending, form descending, and value descending
SELECT *
FROM user_team
ORDER BY fixture_difficulty ASC, home_or_away DESC, form DESC, value DESC;
