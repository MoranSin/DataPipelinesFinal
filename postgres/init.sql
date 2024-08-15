\c postgres;
CREATE TABLE IF NOT EXIST Songs (
    song_id INT,
    artist_id INT,
    genre_id INT,
    song_name VARCHAR(50),
    song_link VARCHAR(50),
    song_lyrics VARCHAR(50),
    song_length INT,
    PRIMARY KEY (song_id),
    FOREIGN KEY(artist_id)
        REFERENCES Artists(artist_id),
    FOREIGN KEY(genre_id)
        REFERENCES Genres(genre_id),
);

CREATE TABLE ID NOT EXIST Artists (
    artist_id INT,
    artist_name VARCHAR(50),
    genre_id INT,
    country_code VARCHAR(50),
    artist_gender VARCHAR(50),
    PRIMARY KEY(artist_id),
    FOREIGN KEY(genre_id)
        REFERENCES Genres(genre_id),
);

CREATE TABLE ID NOT EXIST Genres (
    genre_id INT,
    genre_name VARCHAR(50),
    PRIMARY KEY(genre_id),
);

CREATE TABLE ID NOT EXIST Charts (
    rank_id INT,
    artist_id INT,
    song_id INT,
    rank_value INT,
    date DATETIME,
    source VARCHAR(50),
    country_code VARCHAR(50),
    PRIMARY KEY(rank_id),
    FOREIGN KEY(artist_id)
        REFERENCES Artists(artist_id),
    FOREIGN KEY(song_id)
        REFERENCES Songs(song_id),
);

