from operator import index
import pandas as pd
import numpy as np

movies = pd.read_csv('webapp/data/movies.csv')
tags = pd.read_csv('webapp/data/tags.csv')
ratings = pd.read_csv('webapp/data/ratings.csv')
links = pd.read_csv('webapp/data/links.csv')
personality = pd.read_csv('webapp/data/personality_data/personality-data.csv')
ratings_personality = pd.read_csv('webapp/data/personality_data/ratings.csv')

links = links.dropna()
links.to_csv('webapp/data/links.csv', index=False)

personality = personality.drop_duplicates()
ratings_personality = ratings_personality.drop_duplicates()

personality.to_csv('webapp/data/personality_data/personality-data.csv', index=False)
ratings_personality.to_csv('webapp/data/personality_data/ratings.csv', index=False)