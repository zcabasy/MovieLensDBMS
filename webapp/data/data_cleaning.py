import pandas as pd
import numpy as np

# movies = pd.read_csv('webapp/data/movies.csv')
# tags = pd.read_csv('webapp/data/tags.csv')
# ratings = pd.read_csv('webapp/data/ratings.csv')

links = pd.read_csv('links.csv', dtype=str)
# personality = pd.read_csv('personality_data/personality-data.csv', dtype=str)
# ratings_personality = pd.read_csv('webapp/data/personality_data/ratings.csv', dtype=str)
# personality_predictions = pd.read_csv('personality_data/personality-predictions.csv', dtype=str)

#Remove rows with NaN values
links['tmdbId'].replace(np.nan, 00000000000000, inplace=True)
# links = links.dropna()
links.to_csv('links.csv', index=False)

#Remove duplicates rows
# personality = personality.drop_duplicates()
# ratings_personality = ratings_personality.drop_duplicates()

# personality.to_csv('webapp/data/personality_data/personality-data.csv', index=False)
# ratings_personality.to_csv('webapp/data/personality_data/ratings.csv', index=False)

#Remove duplicate rows based on userId


# personality = personality.drop_duplicates(subset='userid', keep="first")
# personality.to_csv('personality_data/personality-data.csv', index=False)
# ratings_personality.to_csv('webapp/data/personality_data/ratings.csv', index=False)

# personality_predictions = personality_predictions.drop_duplicates(subset='userid', keep="first")
# personality_predictions.to_csv('personality_data/personality-predictions.csv', index=False)
