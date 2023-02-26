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
  event INT,
  home_team INT,
  away_team INT,
  team_h_difficulty INT,
  team_a_difficulty INT
);
