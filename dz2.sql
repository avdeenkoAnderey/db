--1.Название и продолжительность самого длительного трека.
SELECT name, duration FROM db.tracks WHERE duration = (SELECT MAX(duration) FROM db.tracks)

--2.Название треков, продолжительность которых не менее 3,5 минут.
SELECT name FROM db.tracks WHERE duration / 60 >= 3.5

--3.Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT name FROM db.collection WHERE release_year BETWEEN 2018 AND 2020

--4.Исполнители, чьё имя состоит из одного слова
SELECT name FROM db.artists WHERE name NOT LIKE '% %';

--5.Название треков, которые содержат слово «мой» или «my».
SELECT name FROM db.tracks WHERE name ILIKE '%мой%' OR LOWER(name) ILIKE '%my%';

