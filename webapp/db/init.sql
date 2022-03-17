CREATE DATABASE IF NOT EXISTS `MovieLensDB`;

USE `MovieLensDB`;

-- Table Movies
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Movies` (
  `movieId` INT NOT NULL,
  `title` VARCHAR(500) NOT NULL,
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
  `imdbId` TEXT NOT NULL,
  `tmdbId` TEXT NULL,
  PRIMARY KEY (`movieId`),
  CONSTRAINT `links.movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `MovieLensDB`.`Movies` (`movieId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- Table Metrics
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Metrics` (
  `metricId` INT NOT NULL,
  `metric` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`metricId`))
ENGINE = InnoDB;

-- Table Conditions
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Conditions` (
  `conditionId` INT NOT NULL,
  `Condition` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`conditionId`))
ENGINE = InnoDB;

-- Table Personality
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Personality` (
  `userId` VARCHAR(500) NOT NULL,
  `openness` FLOAT NOT NULL,
  `agreeableness` FLOAT NOT NULL,
  `emotional_stability` FLOAT NOT NULL,
  `conscientiousness` FLOAT NOT NULL,
  `extraversion` FLOAT NOT NULL,
  `assigned metric` INT NOT NULL,
  `assigned condition` INT NOT NULL,
  PRIMARY KEY (`userId`),
  INDEX `metricId_idx` (`assigned metric` ASC) VISIBLE,
  INDEX `conditionId_idx` (`assigned condition` ASC) VISIBLE,
  CONSTRAINT `metricId`
    FOREIGN KEY (`assigned metric`)
    REFERENCES `MovieLensDB`.`Metrics` (`metricId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `conditionId`
    FOREIGN KEY (`assigned condition`)
    REFERENCES `MovieLensDB`.`Conditions` (`conditionId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- Table Personality Predictions
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`Personality-Predictions` (
  `userId` VARCHAR(500) NOT NULL,
  `movie_1` INT NOT NULL,
  `predicted_rating_1` FLOAT NOT NULL,
  `movie_2` INT NOT NULL,
  `predicted_rating_2` FLOAT NOT NULL,
  `movie_3` INT NOT NULL,
  `predicted_rating_3` FLOAT NOT NULL,
  `movie_4` INT NOT NULL,
  `predicted_rating_4` FLOAT NOT NULL,
  `movie_5` INT NOT NULL,
  `predicted_rating_5` FLOAT NOT NULL,
  `movie_6` INT NOT NULL,
  `predicted_rating_6` FLOAT NOT NULL,
  `movie_7` INT NOT NULL,
  `predicted_rating_7` FLOAT NOT NULL,
  `movie_8` INT NOT NULL,
  `predicted_rating_8` FLOAT NOT NULL,
  `movie_9` INT NOT NULL,
  `predicted_rating_9` FLOAT NOT NULL,
  `movie_10` INT NOT NULL,
  `predicted_rating_10` FLOAT NOT NULL,
  `movie_11` INT NOT NULL,
  `predicted_rating_11` FLOAT NOT NULL,
  `movie_12` INT NOT NULL,
  `predicted_rating_12` FLOAT NOT NULL,
  `is_personalized` INT NOT NULL,
  `enjoy_watching` INT NOT NULL,
  PRIMARY KEY (`userId`),
  CONSTRAINT `Personality-Predictions.userId`
    FOREIGN KEY (`userId`)
    REFERENCES `MovieLensDB`.`Personality` (`userId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- Table Ratings-Personality
CREATE TABLE IF NOT EXISTS `MovieLensDB`.`RatingsForPersonality` (
  `userId` VARCHAR(500) NOT NULL,
  `movieId` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  PRIMARY KEY (`userId`, `movieId`),
  CONSTRAINT `RatingsForPersonality.userId`
    FOREIGN KEY (`userId`)
    REFERENCES `MovieLensDB`.`Personality` (`userId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

LOAD DATA INFILE '/data/movies.csv' INTO TABLE Movies FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/tags.csv' INTO TABLE Tags FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/ratings.csv' INTO TABLE Ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/links.csv' INTO TABLE Links FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/genres.csv' INTO TABLE Genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/movie_genres.csv' INTO TABLE Movie_Genres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA INFILE '/data/personality_data/metric.csv' INTO TABLE Metrics FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/condition.csv' INTO TABLE Conditions FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/personality-data.csv' INTO TABLE Personality FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/personality-predictions.csv' INTO TABLE `Personality-Predictions` FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/ratings.csv' INTO TABLE RatingsForPersonality FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- Create indexes for faster searching
-- CREATE INDEX title_idx
-- ON Movies (title);

-- CREATE INDEX tag_idx
-- ON Tags (tag);

-- CREATE INDEX genreId_idx
-- ON Movie_Genres (genreId);

-- CREATE INDEX metricId_idx
-- ON Personality (`assigned metric`);

-- CREATE INDEX conditionId_idx
-- ON Personality (`assigned condition`);

-- CREATE INDEX enjoy_watching_idx
-- ON `Personality-Predictions` (enjoy_watching);

-- CREATE INDEX is_personalised_idx
-- ON `Personality-Predictions` (is_personalized);

-- Setup permissions for safeuser
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'safebrowser';
FLUSH PRIVILEGES;
GRANT SELECT ON TABLE `MovieLensDB`.* TO 'safebrowser';
FLUSH PRIVILEGES;