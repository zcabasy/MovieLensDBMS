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

#Data validity check
def data_nullity(dataset):
    #return dataset.isna().any()
    return dataset.isnull().sum()


""" print(data_nullity(movies))
print(data_nullity(tags))
print(data_nullity(ratings))
print(data_nullity(links)) """

for index, row in movies.iterrows():
    print(type(row))



