import numpy as npy
import pandas as pds

# on peut choisir l'affichage verbeux ou non
""" set verb a True pour verbeux """
VERB = True

USER_COL = 'userId'
MOVIE_COL = 'movieId'
RATING_COL = 'rating'
TIMESTAMP_COL = 'timestamp'
TITLE_COL = 'title'
GENRES_COL = 'genres'

RATING_FILE_PATH = '100_first_user_ratings.csv'
MOVIES_FILE_PATH = 'ml-20m/movies.csv'


def prt(string):
    if (VERB):
        print(string)


from math import sqrt


def distance(user1, user2, mean_ratings_movies):
    square_user_1_2 = []
    for i in range(len(user1)):
        if user1[i] != 0 or user2[i] != 0:
            if user1[i] != 0:
                x = user1[i]
            else:
                x = mean_ratings_movies[i]
            if user2[i] != 0:
                y = user2[i]
            else:
                y = mean_ratings_movies[i]
            square_user_1_2.append((x - y) ** 2)

    return sqrt(sum(square_user_1_2))


def global_distances(matrix_ratings):
    matrix_len = len(matrix_ratings)
    mean_ratings_movies = npy.mean(matrix_ratings, axis=0)

    result = npy.zeros((matrix_len, matrix_len))
    for i in range(matrix_len):
        result[i][i] = 0.0
        for j in range(i + 1, matrix_len):
            result[i][j] = result[j][i] = distance(matrix_ratings[i], matrix_ratings[j], mean_ratings_movies)

    return result


def get_closest_users_ids(dataset_matrix, user_index_list, user_id, n=5):
    local_index = user_index_list.index(user_id)
    prt(user_index_list)
    user_distances = dataset_matrix[local_index].tolist()
    prt(user_distances)
    user_distances_sorted = sorted(user_distances)
    prt(user_distances_sorted)

    result = []
    for i in range(1, n + 1):
        result.append(user_index_list[
                          user_distances.index(
                              user_distances_sorted[i])])
    return result


def get_dataset_ratings():
    return pds.read_csv(RATING_FILE_PATH, sep=',', encoding='utf-8',
                        usecols=[USER_COL, MOVIE_COL, RATING_COL, TIMESTAMP_COL]).pivot(index=USER_COL,
                                                                                        columns=MOVIE_COL,
                                                                                        values=RATING_COL).fillna(0.0)


def get_dataset_movies():
    return pds.read_csv(MOVIES_FILE_PATH, sep=',', encoding='utf-8',
                        usecols=[MOVIE_COL, TITLE_COL, GENRES_COL])


from sklearn import model_selection as ms

dataframe_ratings = get_dataset_ratings()

train, test = ms.train_test_split(dataframe_ratings, test_size=0.2)

train_user_index_list = train.index.values.tolist()

dist_matrix = global_distances(train.values)

import random

closest_users = get_closest_users_ids(dist_matrix, train_user_index_list, random.choice(train_user_index_list), n=10)
print(closest_users)
