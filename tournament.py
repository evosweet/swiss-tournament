#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("truncate match CASCADE")
        con.commit()
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()


def deletePlayers():
    """Remove all the player records from the database."""
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("truncate players CASCADE")
        con.commit()
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()


def countPlayers():
    """Returns the number of players currently registered."""
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("select count(id) from players")
        return cur.fetchone()[0]
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("insert into players (name) values(%s)", (name,))
        con.commit()
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        con = connect()
        cur = con.cursor()
        sub_cur = con.cursor()
        cur.execute("select id,name,wins from standings")
        stand_list = []
        if cur:
            for stand in cur:
                sub_cur.execute(
                    "select count(id) from match where player_one = %s or player_two = %s",
                    (stand[0], stand[0]))
                match_count = sub_cur.fetchone()
                stand_list.append((stand[0], stand[1], stand[2], match_count[0]))
            return stand_list
        else:
            return []
    except psycopg2.DatabaseError as error:
        print error
    finally:
        if con:
            con.close()



def reportMatch(winner, loser, tournament_id): 
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    tournament id added to keep track of which tournament the player is playing in
    """

    try:
        con = connect()
        cur = con.cursor()
        cur.execute(
            "insert into match (player_one, player_two, tour_id, winner) values(%s, %s, %s, %s)",
            (winner, loser, tournament_id, winner))
        con.commit()
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("select id,name from standings order by wins desc")
        pair = ()
        count = 0
        pair_list = []
        for player in cur:
            count = count + 1
            if count == 2:
                pair = pair + player
                pair_list.append(pair)
                count = 0
                pair = ()
            else:
                pair = pair + player
        return pair_list
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()



#tournament methods
def deleteTournaments():
    """ delete all tournaments """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("truncate tournament CASCADE")
        con.commit()
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()

def createTournament(name):
    """ create new tournament """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("insert into tournament (name) values(%s) RETURNING id", (name,))
        con.commit()
        tour_id = cur.fetchone()[0]
        return tour_id
    except psycopg2.DatabaseError, error:
        print error
    finally:
        if con:
            con.close()


def playerStandingsWithTour():
    """ Get player standings Group by tournament"""
    try:
        con = connect()
        cur = con.cursor()
        sub_cur = con.cursor()
        cur.execute("select id,name,wins from standings")
        stand_list = []
        if cur:
            for stand in cur:
                sub_cur.execute(
                    "select count(id),tour_id from match where player_one = %s" \
                    "or player_two = %s group by tour_id",
                    (stand[0], stand[0]))
                match_count = sub_cur.fetchone()
                stand_list.append((stand[0], stand[1], stand[2], match_count[0], match_count[1]))
            return stand_list
        else:
            return []
    except psycopg2.DatabaseError as error:
        print error
    finally:
        if con:
            con.close()
            