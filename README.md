# Swiss-Tournament

## Python Script that allows  for the management of swiss style Tournament

### Script Features

* count number of registered players
* register a new player
* check player standings
* record the outcome of a match


### Dependencies

* psycopg2
* postgres DB



### Extra credit

* multi Tournament support added 
 * Tournament table, delete `deleteTournaments`, create `createTournament` and standings by Tournament`playerStandingsWithTour` methods added.



 ## How to run a successful Tournament

 #### to configure the database from the pqsl command line run `\i` with the file path of the sql file `tournament.sql`.
* Example
    * `\i /vagrant/tournament/tournament.sql`

#### To execute all test cases, from your command line run  `python tournament_test.py`

