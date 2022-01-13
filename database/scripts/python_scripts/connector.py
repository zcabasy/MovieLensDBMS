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

mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Movies` (`movieId` INT NOT NULL, `title` VARCHAR(1000) NOT NULL, `genres` VARCHAR(1000) NOT NULL, PRIMARY KEY (`movieId`)) ENGINE = InnoDB")
mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Tags` (`userId` INT NOT NULL,`movieId` INT NOT NULL,`tag` VARCHAR(1000) NOT NULL,`timestamp` INT NOT NULL,PRIMARY KEY (`userId`, `movieId`, `tag`),INDEX `movieId_idx` (`movieId` ASC) VISIBLE,CONSTRAINT `movieId`FOREIGN KEY (`movieId`) REFERENCES `movies_schema`.`Movies` (`movieId`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB")
mycursor.execute("CREATE TABLE IF NOT EXISTS `movies_schema`.`Ratings` (`userId` INT NOT NULL, `movieId` INT NOT NULL, `rating` FLOAT NOT NULL, `timestamp` INT NOT NULL, PRIMARY KEY (`userId`, `movieId`), INDEX `moveId_idx` (`movieId` ASC) VISIBLE, CONSTRAINT `moveId` FOREIGN KEY (`movieId`) REFERENCES `movies_schema`.`Movies` (`movieId`) ON DELETE NO ACTION ON UPDATE NO ACTION) ENGINE = InnoDB")
#add links and the tables for personality schema


#Imports
import pandas as pd
import numpy as np

#Raw data paths
dirName = '../raw_data/'
movies_path = dirName + 'movies.csv'
tags_path = dirName + 'tags.csv'
ratings_path = dirName + 'ratings.csv'
links_path = dirName + 'links.csv'

#Read in raw data
movies = pd.read_csv(movies_path)
tags = pd.read_csv(tags_path)
ratings = pd.read_csv(ratings_path)
links = pd.read_csv(links_path)

for index, row in movies.iterrows():
    mycursor.execute("INSERT INTO Movies (movieId, title, genres) VALUES (%s, %s, %s)", (int(row[0]), row[1], row[2]))
    #db.commit()

#for index, row in tags.iterrows():
    #mycursor.execute("INSERT INTO Tags (userId, movieId, tag, timestamp) VALUES (%s, %s, %s, %s)", (int(row[0]), int(row[1]), row[2], int(row[3])))
    #db.commit()

#for index, row in ratings.iterrows():
    #mycursor.execute("INSERT INTO Ratings (userId, movieId, rating, timestamp) VALUES (%s, %s, %s, %s)", (int(row[0]), int(row[1]), row[2], int(row[3])))
    #db.commit()


mycursor.close()