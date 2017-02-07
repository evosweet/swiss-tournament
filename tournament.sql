-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create schema
CREATE DATABASE tournament;


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
    player_one serial references players(id),
    player_two serial references players(id),    
    tour_id serial references tournament(id), 
    winner serial references players(id)
);

-- create standings view
CREATE VIEW standings  as  select p.id, p.name, count(m.winner) as wins from players as p left join match m on p.id = m.winner group by p.name, p.id order by count(m.winner);
