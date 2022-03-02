CREATE DATABASE IF NOT EXISTS `MovieLensDB`;

USE `MovieLensDB`;

-- Table Movies
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Movies` (
  `movieId` INT NOT NULL,
  `title` VARCHAR(500) NOT NULL,
  `genres` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`movieId`))
ENGINE = InnoDB;


-- Table Tags
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Tags` (
  `userId` INT NOT NULL,
  `movieId` INT NOT NULL,
  `tag` VARCHAR(500) NOT NULL,
  `timestamp` INT NOT NULL,
  PRIMARY KEY (`userId`, `movieId`, `tag`),
  INDEX `movieId_idx` (`movieId` ASC) VISIBLE,
  CONSTRAINT `tags.movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `MovieLensDB`.`Movies` (`movieId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;      


-- Table Genres
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Genres` (
  `genreId` INT NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genreId`))
ENGINE = InnoDB;


-- Table Movie_Genres
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Movie_Genres` (
  `movieId` INT NOT NULL,
  `genreId` INT NOT NULL,
  PRIMARY KEY (`movieId`, `genreId`),
  INDEX `genreId_idx` (`genreId` ASC) VISIBLE,
  CONSTRAINT `genreId`
    FOREIGN KEY (`genreId`)
    REFERENCES `MovieLensDB`.`Genres` (`genreId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `MovieLensDB`.`Movies` (`movieId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- Table Ratings
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Ratings` (
  `userId` INT NOT NULL,
  `movieId` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  `timestamp` INT NOT NULL,
  PRIMARY KEY (`userId`, `movieId`),
  INDEX `moveId_idx` (`movieId` ASC) VISIBLE,
  CONSTRAINT `ratings.moveId`
    FOREIGN KEY (`movieId`)
    REFERENCES `MovieLensDB`.`Movies` (`movieId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- Table Links
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Links` (
  `movieId` INT NOT NULL,
  `imdbId` INT NOT NULL,
  `tmdbId` INT NOT NULL,
  PRIMARY KEY (`movieId`),
  CONSTRAINT `links.movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `MovieLensDB`.`Movies` (`movieId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- Table Personality
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Personality` (
  `userId` VARCHAR(500) NOT NULL,
  `openness` FLOAT NOT NULL,
  `agreeableness` FLOAT NOT NULL,
  `emotional_stability` FLOAT NOT NULL,
  ` conscientiousness` FLOAT NOT NULL,
  ` extraversion` FLOAT NOT NULL,
  `assigned metric` VARCHAR(45) NOT NULL,
  `assigned condition` VARCHAR(45) NOT NULL,
  `movie_1` INT NULL,
  `predicted_rating_1` FLOAT NULL,
  `movie_2` INT NULL,
  `predicted_rating_2` FLOAT NULL,
  `movie_3` INT NULL,
  `predicted_rating_3` FLOAT NULL,
  `movie_4` INT NULL,
  `predicted_rating_4` FLOAT NULL,
  `movie_5` INT NULL,
  `predicted_rating_5` FLOAT NULL,
  `movie_6` INT NULL,
  `predicted_rating_6` FLOAT NULL,
  `movie_7` INT NULL,
  `predicted_rating_7` FLOAT NULL,
  `movie_8` INT NULL,
  `predicted_rating_8` FLOAT NULL,
  `movie_9` INT NULL,
  `predicted_rating_9` FLOAT NULL,
  `movie_10` INT NULL,
  `predicted_rating_10` FLOAT NULL,
  `movie_11` INT NULL,
  `predicted_rating_11` FLOAT NULL,
  `movie_12` INT NULL,
  `predicted_rating_12` FLOAT NULL,
  `is_personalized` INT NULL,
  `enjoy_watching` INT NULL,
  PRIMARY KEY (`userId`, `movie_1`, `predicted_rating_1`, `movie_2`, `predicted_rating_2`, `movie_3`, `predicted_rating_3`, `movie_4`, `predicted_rating_4`, `movie_5`, `predicted_rating_5`, `movie_6`, `predicted_rating_6`, `movie_7`, `predicted_rating_7`, `movie_8`, `predicted_rating_8`, `movie_9`, `predicted_rating_9`, `movie_10`, `predicted_rating_10`, `movie_11`, `predicted_rating_11`, `movie_12`, `predicted_rating_12`))
ENGINE = InnoDB;

-- Table Ratings-Personality
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`RatingsForPersonality` (
  `userId` VARCHAR(500) NOT NULL,
  `movieId` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  PRIMARY KEY (`userId`, `movieId`))
ENGINE = InnoDB;

LOAD DATA INFILE '/data/movies.csv' INTO TABLE Movies FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/tags.csv' INTO TABLE Tags FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/ratings.csv' INTO TABLE Ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/links.csv' INTO TABLE Links FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/genres.csv' INTO TABLE Genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/movie_genres.csv' INTO TABLE Movies_Genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA INFILE '/data/personality_data/personality-data.csv' INTO TABLE Personality FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/ratings.csv' INTO TABLE RatingsForPersonality FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- Create indexes for faster searching
CREATE INDEX titleIndex
ON movies (title);

CREATE INDEX tagIndex
ON tags (tag);

CREATE INDEX genreIndex
ON movie_genres (genreId);

-- Create view for users to use
CREATE VIEW `movielens` AS
SELECT movies.movieId, movies.title, GROUP_CONCAT(DISTINCT tags.tag) as tag, AVG(ratings.rating) as rating, links.imdbId, GROUP_CONCAT(DISTINCT movie_genres.genreId) as genreId
FROM movies 
INNER JOIN tags ON movies.movieId = tags.movieId 
INNER JOIN ratings ON movies.movieId = ratings.movieId
INNER JOIN links ON movies.movieId = links.movieId
INNER JOIN movie_genres ON movies.movieId = movie_genres.movieId
GROUP BY title
ORDER BY movieId

-- Create safe user
CREATE USER 'safe_browser' IDENTIFIED BY 'pass123';
GRANT SELECT ON TABLE `MovieLensDB`.* TO 'safe_browser';