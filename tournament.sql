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


-- appliation selects
-- truncate match CASCADE
-- truncate players CASCADE
-- select count(id) from players
-- insert into players (name) values(%s)
-- select count(id) from match where player_one = %s or player_two = %s
-- insert into match (player_one, player_two, tour_id, winner) values(%s, %s, %s, %s)
-- select id,name from standings order by wins desc

