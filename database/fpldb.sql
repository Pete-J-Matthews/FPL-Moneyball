CREATE DATABASE IF NOT EXISTS fpldb;

USE fpldb;

CREATE TABLE IF NOT EXISTS players (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  team INT,
  position INT,
  form DECIMAL(4,2),
  value DECIMAL(4,1),
  selected_by DECIMAL(4,2)
);

CREATE TABLE IF NOT EXISTS fixtures (
  fixture_id INT PRIMARY KEY,
  gameweek INT,
  home_team INT,
  away_team INT,
  home_difficulty INT,
  away_difficulty INT
);

-- Table for my team players
CREATE TABLE IF NOT EXISTS my_team (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  team INT,
  position INT,
  form FLOAT,
  value FLOAT,
  is_captain BOOLEAN
);
