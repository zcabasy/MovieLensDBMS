-Table Movies
CREATE TABLE IF NOT EXISTS `movies_schema`.`Movies` (
  `movieId` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `genres` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`movieId`))
ENGINE = InnoDB;

-Table Tags
CREATE TABLE IF NOT EXISTS `movies_schema`.`Tags` (
  `userId` INT NOT NULL,
  `movieId` INT NOT NULL,
  `tag` VARCHAR(45) NOT NULL,
  `timestamp` INT NOT NULL,
  PRIMARY KEY (`userId`, `movieId`),
  INDEX `movieId_idx` (`movieId` ASC) VISIBLE,
  CONSTRAINT `movieId`
    FOREIGN KEY (`movieId`)
    REFERENCES `movies_schema`.`Movies` (`movieId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-Table Ratings
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


-Table Links
CREATE TABLE IF NOT EXISTS `movies_schema`.`Links` (
  `movieId` INT NOT NULL,
  `imdbId` INT NOT NULL,
  `tmdbId` INT NOT NULL,
  PRIMARY KEY (`movieId`))
ENGINE = InnoDB;
