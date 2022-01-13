import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "my-secret-pw",
    database = "MovieLensDB"
)

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS `MovieLensDB`")
mycursor.execute("CREATE SCHEMA IF NOT EXISTS `movies_schema` DEFAULT CHARACTER SET utf8")
mycursor.execute("CREATE SCHEMA IF NOT EXISTS `user_personality_schema` DEFAULT CHARACTER SET utf8")
mycursor.execute("USE `movies_schema`")

mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Movies` (`movieId` INT NOT NULL, `title` VARCHAR(45) NOT NULL, `genres` VARCHAR(45) NOT NULL, PRIMARY KEY (`movieId`)) ENGINE = InnoDB")
mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Tags` (`userId` INT NOT NULL,`movieId` INT NOT NULL,`tag` VARCHAR(45) NOT NULL,`timestamp` INT NOT NULL,PRIMARY KEY (`userId`, `movieId`),INDEX `movieId_idx` (`movieId` ASC) VISIBLE,CONSTRAINT `movieId`FOREIGN KEY (`movieId`)REFERENCES `movies_schema`.`Movies` (`movieId`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB")
mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Ratings` (`userId` INT NOT NULL, `movieId` INT NOT NULL, `rating` FLOAT NOT NULL, `timestamp` INT NOT NULL, PRIMARY KEY (`userId`, `movieId`), INDEX `moveId_idx` (`movieId` ASC) VISIBLE, CONSTRAINT `moveId` FOREIGN KEY (`movieId`) REFERENCES `movies_schema`.`Movies` (`movieId`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB")
#add links and the tables for personality schema
mycursor.close()