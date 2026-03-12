--1.Количество исполнителей в каждом жанре.
SELECT 
	g.name AS "жанр",
	count(ag.artist_id) AS "кол-во исполнителей"
FROM db.artist_genres AS ag
LEFT JOIN db.genres AS g on ag.genre_id = g.genre_id
GROUP BY g.name;

--2.Количество треков, вошедших в альбомы 2000–2014 годов.
SELECT 
	a."name" AS "альбом",
	COUNT(t.track_id) AS "кол-во треков"
FROM db.tracks AS t
LEFT JOIN db.albums AS a ON t.album_id = a.album_id 
WHERE a.release_year BETWEEN 2000 AND 2014
GROUP BY a."name";

--3.Средняя продолжительность треков по каждому альбому..
SELECT 
	a."name" AS "альбом",
	ROUND(AVG(t.duration/60.0)::numeric ,2) AS "ср.продол-сть треков"
FROM db.tracks AS t
LEFT JOIN db.albums AS a ON t.album_id = a.album_id 
GROUP BY a."name";

--4.Все исполнители, которые не выпустили альбомы в 2014 году.
SELECT DISTINCT art.name AS "исполнитель"
FROM db.artist_albums AS a
LEFT JOIN db.artists AS art ON a.artist_id = art.artist_id 
LEFT JOIN db.albums AS ab ON a.album_id = ab.album_id 
WHERE ab.release_year !=2014;