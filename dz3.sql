--1.Количество исполнителей в каждом жанре.
SELECT 
	g.name AS "жанр",
	count(ag.artist_id) AS "кол-во исполнителей"
FROM artist_genres AS ag
LEFT JOIN genres AS g on ag.genre_id = g.genre_id
GROUP BY g.name;

--2.Количество треков, вошедших в альбомы 2000–2014 годов.
SELECT COUNT(t.track_id) AS "кол-во треков"
FROM tracks AS t
INNER JOIN albums AS a ON t.album_id = a.album_id
WHERE a.release_year BETWEEN 2000 AND 2014;

--3.Средняя продолжительность треков по каждому альбому..
SELECT 
	a."name" AS "альбом",
	ROUND(AVG(t.duration/60.0)::numeric ,2) AS "ср.продол-сть треков"
FROM tracks AS t
LEFT JOIN albums AS a ON t.album_id = a.album_id 
GROUP BY a."name";

--4.Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT DISTINCT art.name AS "исполнитель"
FROM artists AS art
WHERE art.artist_id NOT IN (
    SELECT a.artist_id
    FROM artist_albums AS a
    JOIN albums AS ab ON a.album_id = ab.album_id
    WHERE ab.release_year = 2020
);

--5.Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT c.name AS "название сборника"
FROM collection c
INNER JOIN collection_tracks ct ON c.collection_id = ct.collection_id
INNER JOIN tracks t ON ct.track_id = t.track_id
INNER JOIN albums a ON t.album_id = a.album_id
INNER JOIN artist_albums aa ON a.album_id = aa.album_id
INNER JOIN artists ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'Земфира'