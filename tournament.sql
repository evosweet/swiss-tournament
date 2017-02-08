-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create schema
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\C tournament

-- Drop tables

DROP TABLE IF EXISTS tournament.players CASCADE;
DROP TABLE IF EXISTS tournament.tournament CASCADE;
DROP TABLE IF EXISTS tournament.match CASCADE;


-- create players tables 
CREATE TABLE players (
    id serial primary key, 
    name text 
);

-- create tournament tables 
CREATE TABLE tournament (
    id serial primary key,
    name text
);

-- create match table
CREATE TABLE match (
    id serial primary key, 
    winner INTEGER references players(id),
    loser INTEGER references players(id),    
    tour_id INTEGER references tournament(id) 
);

-- create standings view
CREATE VIEW standings as select p.id, p.name, count(m.winner) as wins from players as p left join match m on p.id = m.winner group by p.name, p.id order by count(m.winner);
