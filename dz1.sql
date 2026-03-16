--Задание1
/*************************************************************/
-- 1. Таблица жанров
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO genres (genre_id, name) VALUES
(1, 'Русский рок'),
(2, 'Альтернативный рок'),
(3, 'Инди‑рок');
/*************************************************************/
-- 2. Таблица исполнителей
CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT null UNIQUE
);
INSERT INTO artists (artist_id, name) VALUES
(1, 'Земфира'),
(2, 'Би‑2'),
(3, 'ДДТ'),
(4, 'Сплин');
/*************************************************************/
-- 3. Таблица связи исполнителей и жанров
CREATE TABLE artist_genres (
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (artist_id, genre_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

INSERT INTO artist_genres (artist_id, genre_id) VALUES
(1, 1),  -- Земфира — Русский рок
(1, 2),  -- Земфира — Альтернативный рок
(2, 1),  -- Би‑2 — Русский рок
(3, 1),  -- ДДТ — Русский рок
(4, 3);  -- Сплин — Инди‑рок

/*************************************************************/
-- 4. Таблица альбомов
CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT null UNIQUE,
    release_year INT null
);

INSERT INTO albums (album_id, name, release_year) VALUES
(1, 'Прости меня моя любовь', 2000),
(2, 'Иномарки', 2004),
(3, 'Метель', 2014);
/*************************************************************/
-- 5. Таблица связи исполнителей и альбомов
CREATE TABLE artist_albums (
    artist_id INT NOT NULL,
    album_id INT NOT NULL,
    PRIMARY KEY (artist_id, album_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE CASCADE
);
INSERT INTO artist_albums (artist_id, album_id) VALUES
(1, 1),  -- Земфира — Прости меня моя любовь
(2, 2),  -- Би‑2 — Иномарки
(3, 3);  -- ДДТ — Метель

/*************************************************************/
-- 6. Таблица треков
CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    duration int NULL CHECK (duration > 0),
    album_id INT NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE CASCADE
);
INSERT INTO tracks (track_id, name, duration, album_id) VALUES
(1, 'Искала', 245, 1),
(2, 'Хочешь?', 228, 1),
(3, 'Небомореоблака', 270, 2),
(4, 'Мой рок‑н‑ролл', 295, 2),
(5, 'Метель', 312, 3),
(6, 'Романс', 288, 3),
(7, 'Орбит без сахара', 185, 1),
(8, 'Феллини', 260, 2);

/*************************************************************/
-- 7. Таблица сборников
CREATE TABLE collection (
    collection_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    release_year INT null
);
INSERT INTO collection (collection_id, name, release_year) VALUES
(1, 'Лучшие песни русского рока 2000-х', 2020),
(2, 'Хиты альтернативного рока', 2019),
(3, 'Зимний плейлист', 2021),
(4, 'Вечные хиты', 2022);

/*************************************************************/
-- 8. Таблица связи сборников и треков
CREATE TABLE collection_tracks (
    collection_id INT NOT NULL,
    track_id INT NOT NULL,
    PRIMARY KEY (collection_id, track_id),
    FOREIGN KEY (collection_id) REFERENCES collection(collection_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
);
INSERT INTO collection_tracks (collection_id, track_id) VALUES
-- Сборник 1: Лучшие песни русского рока 2000-х
(1, 1),  -- Искала
(1, 3),  -- Небомореоблака
(1, 5),  -- Метель
(1, 7),  -- Орбит без сахара

-- Сборник 2: Хиты альтернативного рока
(2, 2),  -- Хочешь?
(2, 4),  -- Мой рок‑н‑ролл
(2, 8),  -- Феллини

-- Сборник 3: Зимний плейлист
(3, 5),  -- Метель
(3, 6),  -- Романс

-- Сборник 4: Вечные хиты
(4, 1),  -- Искала
(4, 4),  -- Мой рок‑н‑ролл
(4, 7);  -- Орбит без сахара
/*************************************************************/






