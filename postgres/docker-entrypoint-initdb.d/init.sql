\c postgres;

CREATE EXTENSION IF NOT EXISTS dblink;

DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'music_charts') THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE music_charts');
   END IF;
END
$$;

\c music_charts;

CREATE TABLE IF NOT EXISTS Genres (
    genre_id UUID,
    genre_name VARCHAR(50),
    PRIMARY KEY (genre_id)
);

CREATE TABLE IF NOT EXISTS Artists (
    artist_id UUID,
    artist_name VARCHAR(100),
    genre_id UUID,
    country_code VARCHAR(10),
    artist_gender VARCHAR(50),
    PRIMARY KEY (artist_id),
    FOREIGN KEY (genre_id)
        REFERENCES Genres (genre_id)
);

CREATE TABLE IF NOT EXISTS Songs (
    song_id UUID,
    artist_id UUID,
    genre_id UUID,
    song_name VARCHAR(100),
    song_link VARCHAR(300),
    song_lyrics VARCHAR(5000),
    song_length VARCHAR(5), 
    song_language VARCHAR(30),
    PRIMARY KEY (song_id),
    FOREIGN KEY (artist_id)
        REFERENCES Artists (artist_id),
    FOREIGN KEY (genre_id)
        REFERENCES Genres (genre_id)
);


CREATE TABLE IF NOT EXISTS Charts (
    rank_id UUID,
    artist_id UUID,
    song_id UUID,
    rank_value INT NOT NULL,
    date DATE NOT NULL,
    source VARCHAR(50),
    country_code VARCHAR(10),
    chart_type VARCHAR(50),
    PRIMARY KEY (rank_id),
    FOREIGN KEY (artist_id)
        REFERENCES Artists (artist_id),
    FOREIGN KEY (song_id)
        REFERENCES Songs (song_id)
);