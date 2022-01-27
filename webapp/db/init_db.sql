SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_with_oids = false;

\c movielens

DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
  id integer NOT NULL,
  name varchar(255),
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS links;
CREATE TABLE links (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  movie_id integer NOT NULL,
  imdb_id text DEFAULT ''::text,
  tmdb_id text,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
  id integer NOT NULL,
  title varchar(255),
  release_date integer,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS movies_genres;
CREATE TABLE movies_genres (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  movie_id integer,
  genre_id integer,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
  user_id integer,
  movie_id integer,
  rating real,
  rated_at int,
  PRIMARY KEY (id)
);

ALTER TABLE genres OWNER TO postgres;
ALTER TABLE links OWNER TO postgres;
ALTER TABLE movies OWNER TO postgres;
ALTER TABLE movies_genres OWNER TO postgres;
ALTER TABLE ratings OWNER TO postgres;

COPY genres(
  id,
  name
) 
FROM '/data/genres.csv' DELIMITER '#' CSV;

COPY links(
  movie_id,
  imdb_id,
  tmdb_id
)
FROM '/data/links.csv' DELIMITER ',' CSV;

COPY movies(
  id,
  title,
  release_date
)
FROM '/data/movies.csv' DELIMITER '#' CSV;

copy movies_genres(
  movie_id,
  genre_id
)
FROM '/data/movie-genres.csv' DELIMITER '#' CSV;

copy ratings(
  user_id,
  movie_id,
  rating,
  rated_at
)
FROM '/data/ratings.csv' DELIMITER ',' CSV;