
# Database

This subdirectory containts the python code that requests the data from the API and sends it to a table in MySQL.

### AWS RDS MySQL Database
For the database I am using an Amazon Web Services RDS instance. This will allow the database to exist in the cloud and wont rely on my local machine for the database to update. 

The database has been formatted for MySQL allowing me to create and run query files through MySQL workbench. The .sql file can be found in this folder.

### API Connection

The Python uses the request module to retrieve infromation from the **[FPL API](https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19)** and use the MySQL conenctor module to send the information to the database.
