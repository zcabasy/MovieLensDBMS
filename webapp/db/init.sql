CREATE DATABASE IF NOT EXISTS `MovieLensDB`;

USE `MovieLensDB`;

CREATE SCHEMA IF NOT EXISTS `movies_schema` DEFAULT CHARACTER SET utf8;
CREATE SCHEMA IF NOT EXISTS `user_personality_schema` DEFAULT CHARACTER SET utf8;

USE `movies_schema`;


-- Table Movies


CREATE TABLE IF NOT EXISTS `movies_schema`.`Movies` (
  `movieId` INT NOT NULL,
  `title` VARCHAR(500) NOT NULL,
  `genres` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`movieId`))
ENGINE = InnoDB;


-- Table Tags


CREATE TABLE IF NOT EXISTS `movies_schema`.`Tags` (
  `userId` INT NOT NULL,
  `movieId` INT NOT NULL,
  `tag` VARCHAR(500) NOT NULL,
  `timestamp` INT NOT NULL,
  PRIMARY KEY (`userId`, `movieId`),
  INDEX `movieId_idx` (`movieId` ASC) VISIBLE,
  CONSTRAINT `movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `movies_schema`.`Movies` (`movieId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- Table Ratings


CREATE TABLE IF NOT EXISTS `movies_schema`.`Ratings` (
  `userId` INT NOT NULL,
  `movieId` INT NOT NULL,
  `rating` FLOAT NOT NULL,
  `timestamp` INT NOT NULL,
  PRIMARY KEY (`userId`, `movieId`),
  INDEX `moveId_idx` (`movieId` ASC) VISIBLE,
  CONSTRAINT `moveId`
    FOREIGN KEY (`movieId`)
    REFERENCES `movies_schema`.`Movies` (`movieId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- Table Links


CREATE TABLE IF NOT EXISTS `movies_schema`.`Links` (
  `movieId` INT NOT NULL,
  `imdbId` INT NOT NULL,
  `tmdbId` INT NOT NULL,
  PRIMARY KEY (`movieId`))
ENGINE = InnoDB;

USE `user_personality_schema`;


-- Personality table


-- Personality-Ratings


USE `movies_schema`;

LOAD DATA INFILE '/data/movies.csv' INTO TABLE Movies FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/tags.csv' INTO TABLE Tags FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/ratings.csv' INTO TABLE Ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/links.csv' INTO TABLE Links FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

USE `user_personality_schema`;

LOAD DATA INFILE '/data/personality_data/personality-data.csv' INTO TABLE Personality FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE '/data/personality_data/ratings.csv' INTO TABLE Personality-Ratings FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;